from typing import Final, Dict, Optional
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, TextChannel, HTTPException, utils
from responses import get_response
from constants import INTRO_MESSAGE, LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT
import logging
from logging.handlers import RotatingFileHandler
import asyncio
from datetime import datetime
import pytz

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
#print(TOKEN)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger = logging.getLogger()
logger.addHandler(handler)

# Philippine timezone
ph_tz = pytz.timezone('Asia/Manila')

# Introduction message for RAGNAROK-HUNTER
#print(INTRO_MESSAGE)

# STEP 1 BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# Dictionary to store the last message sent for each command type
last_messages: Dict[str, Optional[Message]] = {
    "sched": None,
    "add": None,
    "delete": None
}

# Function to delete the previous message
async def delete_previous_message(command_type: str):
    if last_messages[command_type]:
        try:
            print(f"Deleting previous {command_type} message")
            await last_messages[command_type].delete()
        except HTTPException as e:
            print(f"Failed to delete {command_type} message: {e}")
        last_messages[command_type] = None

# Function to delete related messages
async def delete_related_messages(except_command: str):
    for command_type in ["sched", "add", "delete"]:
        if command_type != except_command and last_messages[command_type]:
            await delete_previous_message(command_type)

# STEP 2 MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    global last_messages
    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    command = user_message.split()[0]

    try:
        response: str = get_response(user_message)
        print(f"Generated response: {response}")

        # Determine the type of command
        if user_message.startswith("-mvp sched"):
            command_type = "sched"
        elif user_message.startswith("-mvp add"):
            command_type = "add"
        elif user_message.startswith("-mvp delete"):
            command_type = "delete"
        else:
            command_type = None

        # Delete related messages if command is add, delete, or sched
        if command_type in ["sched", "add", "delete"]:
            await delete_related_messages(command_type)

        # Delete the last message if it exists for the specific command type
        if command_type:
            await delete_previous_message(command_type)

        # Send the new message and store it
        if is_private:
            sent_message = await message.author.send(response)
        else:
            sent_message = await message.channel.send(response)
        
        # Store the message only for add, delete, and sched commands
        if command_type:
            last_messages[command_type] = sent_message

    except Exception as e:
        logger.exception("Error sending message")
        print(e)

# STEP 3 HANDLING STARTUP
@client.event
async def on_ready() -> None:
    print(f'Hello {client.user}, mvp-bot-timer is ready')
    for guild in client.guilds:
        channel: TextChannel = utils.get(guild.text_channels, name='mvp-bot-timer')
        if channel:
            await channel.send(INTRO_MESSAGE)

# STEP 4 HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content

    if not user_message.startswith('-mvp'):
        return

    username: str = str(message.author)
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# STEP 5 MAIN ENTRY POINT
def main() -> None:
    print('here')
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(client.start(TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
    finally:
        loop.close()

if __name__ == '__main__':
    main()
