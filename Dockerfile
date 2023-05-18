FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app/gpt-discord-bot

RUN pip install --no-cache-dir -r /app/gpt-discord-bot/requirements.txt

CMD [ "python3", "-m", "gpt-discord-bot" ]
