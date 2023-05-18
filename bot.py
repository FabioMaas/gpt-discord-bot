import os
import json
import threading
import openai
import discord

script_dir = os.path.dirname(os.path.realpath(__file__))
json_path = os.path.join(script_dir, 'prompts', '')

#Discord intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

#env
openai.api_key = os.getenv('OPENAI_API_KEY')
token = os.getenv('DISCORD_TOKEN')
system_prompt = os.getenv('OPENAI_GPT_SYSTEM_PROMPT')

#Discord commands
discord_bot_prefix = "$"
discord_bot_ask_command = discord_bot_prefix + "ask"
discord_bot_stats_command = discord_bot_prefix + "stats"

#OpenAI parameters
openai_u_model = "gpt-3.5-turbo"
openai_u_temperature= 0.5
openai_u_max_tokens=300
openai_u_frequency_penalty=0.2
openai_u_presence_penalty=0

openai.Model.list()

lock = threading.Lock()

client = discord.Client(intents=intents)

def serve():
    client.run(token)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(discord_bot_stats_command):
        await send_bot_summarize(message)
        return

    if message.content.startswith(discord_bot_ask_command):
        result = message.content.replace(discord_bot_ask_command, '', 1).strip()
        await send_bot_prompt(message, result)
        return

async def send_bot_prompt(message, text_input):

    messages = load_user_chat(message)
    new_message = {"role": "user", "content": text_input}
    messages.append(new_message)

    response = openai.ChatCompletion.create(
        model=openai_u_model,
        messages=messages,
        temperature=openai_u_temperature,
        max_tokens=openai_u_max_tokens,
        frequency_penalty=openai_u_frequency_penalty,
        presence_penalty=openai_u_presence_penalty
    )
    answered_message = response['choices'][0].message
    print(f"[To user {message.author}]:\n{answered_message['content']}")
    messages.append(answered_message)
    update_usercount_content(messages, message.author.name)
    save_user_chat(message, messages)
    await message.channel.send(answered_message['content'])

async def send_bot_summarize(message):
    
    directory = os.path.join(script_dir, 'prompts', 'users')
    result = ""

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                messages = json.load(file)
                # Summarize
                result += messages[2]['content'] + "\n"

    summarize_messages = [
            {"role": "system", "content": "Summarize the names and repeat them in a list with times."},
            {"role": "user", "content": result}
     ]

    response = openai.ChatCompletion.create(
        model=openai_u_model,
        messages=summarize_messages,
        temperature=openai_u_temperature,
        max_tokens=openai_u_max_tokens,
        frequency_penalty=openai_u_frequency_penalty,
        presence_penalty=openai_u_presence_penalty
    )
    print(f"[User {message.author} asked for stats]")
    await message.channel.send(response['choices'][0].message['content'])

def load_base_message(message):
    username = message.author.name
    loaded_messages = [ 
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "The user who is writing to you has the name " + username + "."},
        {"role": "assistant", "content": username + " has not talked to you yet."}
    ]    

    return loaded_messages

def load_user_chat(message):
    user_id = message.author.id
    filename = os.path.join(script_dir, 'prompts', 'users', f'{user_id}.json')

    with lock:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                loaded_messages = json.load(file)
                return loaded_messages
        else:
            return load_base_message(message)

def save_user_chat(message, messages):
    user_id = message.author.id
    filename = os.path.join(script_dir, 'prompts', 'users', f'{user_id}.json')
    with lock:
        with open(filename, 'w') as file:
            json.dump(messages, file, indent=4)

def update_usercount_content(messages, username):
    user_count = 0
    for message in messages:
        if message['role'] == 'user':
            user_count += 1
    messages[2]['content'] = username + " has talked to you " + str(user_count) + " times."

if __name__ == "__main__":
    serve()