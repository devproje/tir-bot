FROM python:3.12-alpine3.18

WORKDIR /opt/bot

COPY . .
RUN ./configure

ENTRYPOINT [ "/opt/bot/.venv/bin/python", "/opt/bot/bot.py" ]
