# GPT-Discord-Bot

A simple and easy implementation of [OpenAI API](https://openai.com/blog/openai-api) into a [Discord bot](https://discordpy.readthedocs.io/en/stable/) as Python module.
Model `gpt-3.5-turbo` is used and will generate a chat per Discord user based on their ID. ChatGPT is also informed about the username to speak more directly to them. 

## Install
Be sure to create an `.env` file in the directory that contains all necessary environment variables:

- `DISCORD_TOKEN` - Token from the used Discord Bot 
- `OPENAI_API_KEY` - API key for using OpenAI
- `OPENAI_GPT_SYSTEM_PROMPT` - The initial system prompt that is used to individualize the response of ChatGPT.


Setup a virtual environment or just install all packages:
```python
pip install -r requirements.txt
```


Run the module to start the service locally:
```python
python3 -m gpt-discord-bot
```

Run the `testprompt.py` to check if your API key works correctly.


## Using Docker
You can also run the `Dockerfile` or `docker-compose.yml` to containerize the module:
```
docker compose up -d
```
