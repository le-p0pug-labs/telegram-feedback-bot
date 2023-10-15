FROM ubuntu:latest

RUN apt update && \
    apt install -y python3 python3-pip python3-venv python3-dev python3-build python3-setuptools python3-wheel

ARG VERSION
ENV TELEGRAM_FEEDBACK_BOT_VERSION="$VERSION"

ENV TELEGRAM_FEEDBACK_BOT_HOME="/telegram-feedback-bot"

RUN mkdir "$TELEGRAM_FEEDBACK_BOT_HOME" && \
    pip3 install --upgrade build

COPY LICENSE "$TELEGRAM_FEEDBACK_BOT_HOME"
COPY pyproject.toml "$TELEGRAM_FEEDBACK_BOT_HOME"
COPY README.md "$TELEGRAM_FEEDBACK_BOT_HOME"

COPY setup.py "$TELEGRAM_FEEDBACK_BOT_HOME"
COPY src "$TELEGRAM_FEEDBACK_BOT_HOME/src"

WORKDIR "$TELEGRAM_FEEDBACK_BOT_HOME"
RUN python3 -m build --sdist --wheel --outdir dist && \
    pip3 install ./dist/telegram*.whl

ENTRYPOINT ["telegram-feedback-bot"]

