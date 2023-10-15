#!/usr/bin/env python3
import logging
import os
from functools import wraps

# from telegram.ext import Updater
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format=" * %(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

global_users_whitelist = []
global_admin_chat_id = 0

DEFAULT_DIRECTORY = os.getcwd()

TELEGRAM_BOT_TOKEN_PARAMETER_NAME = "TELEGRAM_BOT_TOKEN"
TELEGRAM_WHITELIST_PARAMETER_NAME = "TELEGRAM_BOT_WHITELIST"
ADMIN_CHAT_ID_PARAMETER_NAME = "ADMIN_CHAT_ID"


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Telegram feedback bot')
    parser.add_argument('--telegram-bot-token',
                        dest='telegram_bot_token',
                        required=False,
                        type=str,
                        help="Specify an access token for the Squire telegram bot. "
                             f"The environment variable {TELEGRAM_BOT_TOKEN_PARAMETER_NAME} "
                             f"always has the priority over this argument.")
    parser.add_argument('--telegram-users-whitelist',
                        dest='telegram_users_whitelist',
                        required=False,
                        type=str,
                        help="Specify a comma-separated list of telegram usernames allowed to use the bot. "
                             "This argument has to be specified "
                             "if you're enabling the squire bot by giving the --telegram-bot-token argument."
                             f"The environment variable {TELEGRAM_WHITELIST_PARAMETER_NAME} "
                             f"always has the priority over this argument.")
    parser.add_argument('--admin-chat-id',
                        dest='admin_chat_id',
                        required=False,
                        type=int,
                        help='Specify the chat id to forward the feedback to.'
                             f"The environment variable {ADMIN_CHAT_ID_PARAMETER_NAME} "
                             f"always has the priority over this argument.")
    options = parser.parse_args()
    if os.getenv(TELEGRAM_BOT_TOKEN_PARAMETER_NAME):
        options.telegram_bot_token = os.getenv(TELEGRAM_BOT_TOKEN_PARAMETER_NAME)
    if os.getenv(TELEGRAM_WHITELIST_PARAMETER_NAME):
        options.telegram_users_whitelist = os.getenv(TELEGRAM_WHITELIST_PARAMETER_NAME)
    if os.getenv(ADMIN_CHAT_ID_PARAMETER_NAME):
        options.admin_chat_id = os.getenv(ADMIN_CHAT_ID_PARAMETER_NAME)
    if options.telegram_bot_token and not options.telegram_users_whitelist:
        parser.error("--telegram-users-whitelist must be specified if you're using --telegram-bot-token")
    if not options.telegram_bot_token and options.telegram_users_whitelist:
        parser.error("--telegram-bot-token must be specified if you're using --telegram-users-whitelist")
    if not options.admin_chat_id:
        parser.error("--admin-chat-id has to be specified")
    return options


def whitelist_only(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user = update.effective_user
        logger.info(
            f"@{user.username} ({user.id}) is trying to access a privileged command"
        )
        if user.username not in global_users_whitelist:
            logger.warning(f"Unauthorized access denied for {user.username}.")
            text = (
                "🚫 *ACCESS DENIED*\n"
                "Sorry, you are *not authorized* to use this command.\n"
                "This incident will be reported."
            )
            update.message.reply_text(text)
            return
        return func(update, context, *args, **kwargs)

    return wrapped


FEEDBACK = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi! Tell us what you think about cyberschmutz.")
    return FEEDBACK


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_feedback = update.message.text
    await update.message.reply_text("Thank you for your feedback!")
    # Forward the message to the admin
    global global_admin_chat_id

    await context.bot.forward_message(chat_id=global_admin_chat_id,
                                      from_chat_id=update.message.chat_id,
                                      message_id=update.message.message_id)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"▪ Send us your feedback directly, and it will be forwarded to the admin.")


class TelegramFeedbackBot:
    def __init__(self, token: str, admin_chat_id: int):
        self.token = token
        self.admin_chat_id = admin_chat_id

        self.app = ApplicationBuilder().token(self.token).build()
        # self.app.add_handler(CommandHandler("start", start))
        # self.app.add_handler(CommandHandler("help", show_help))

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, feedback)]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        self.app.add_handler(conv_handler)  # Add the conversation handler
        self.app.run_polling()

    def forward_feedback(self, update, context: CallbackContext):
        feedback = update.message.text
        context.bot.send_message(chat_id=self.admin_chat_id,
                                 text=f"Feedback from {update.message.chat_id}: {feedback}")

    def error(self, update, context: CallbackContext):
        error = context.error
        logger.warning(f"Update {update} caused error '{type(error)}': {error}")


def main():
    options = get_arguments()
    telegram_bot_token = options.telegram_bot_token
    telegram_users_whitelist = options.telegram_users_whitelist
    admin_chat_id = options.admin_chat_id

    global global_admin_chat_id
    global_admin_chat_id = admin_chat_id

    global global_users_whitelist

    global_users_whitelist = [line.strip() for line in telegram_users_whitelist.split(",") if line.strip()]
    print(f" * Starting the feedback telegram bot")
    print(f" * Access allowed to: {global_users_whitelist}")
    TelegramFeedbackBot(token=telegram_bot_token,
                        admin_chat_id=int(admin_chat_id))


if __name__ == '__main__':
    main()
