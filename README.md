# Telegram Feedback Bot: Your Telegram Feedback Companion
Gather invaluable feedback from your audience via Telegram with Telegram Feedback Bot.

## Setting Up

### Using Docker

#### Pull Pre-built Image
Download the pre-compiled Docker image with the following command:
```bash
docker pull lep0puglabs/telegram-feedback-bot:latest
```

#### Build Your Own
Alternatively, build the Docker image manually:
```bash
docker build -t telegram-feedback-bot -f ./Dockerfile .
```

#### Run the Container
Initiate the Docker container:
```bash
docker run --rm -it telegram-feedback-bot
```

### Using Python Package Manager
Install the bot directly using pip:
```bash
pip install telegram-feedback-bot
```

## Configuration

### Environment Variables
Duplicate the example environment file and fill in the required values:
```bash
cp .env.example .env
nano .env
```

### Run Telegram Feedback Bot
Start the bot either using the command-line interface:
```bash
telegram-feedback-bot
```
or using Docker:
```bash
docker run --rm -it telegram-feedback-bot
```

And there you go! Your Telegram feedback channel, powered by Telegram Feedback Bot, is now up and running. Feel free to share your thoughts!
