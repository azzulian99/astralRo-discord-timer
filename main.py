from typing import Final, Dict, Optional
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, TextChannel, HTTPException, utils
from responses import get_response
from constants import INTRO_MESSAGE, LOG_LEVEL, LOG_FILE, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT
import logging
from logging.handlers import RotatingFileHandler
import asyncio

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger = logging.getLogger()
logger.addHandler(handler)

# Introduction message for RAGNAROK-HUNTER
print(INTRO_MESSAGE)

# STEP 1 BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# Dictionary to store the last message sent for each command type
last_messages: Dict[str, Dict[str, Optional[Message]]] = {}

# STEP 2 MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    global last_messages
    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    command = user_message.split()[0] + " " + " ".join(user_message.split()[1:])  # Use the whole command string

    try:
        response: str = get_response(user_message)
        print(f"Generated response: {response}")

        # Initialize command in last_messages if not present
        if command not in last_messages:
            last_messages[command] = {"public": None, "private": None}

        # Delete the last sent message if it exists for the specific command type
        if is_private:
            if last_messages[command]["private"]:
                try:
                    print(f"Deleting previous private message for command {command}")
                    await last_messages[command]["private"].delete()
                except HTTPException as e:
                    print(f"Failed to delete private message: {e}")
            last_messages[command]["private"] = await message.author.send(response)
        else:
            if last_messages[command]["public"]:
                try:
                    print(f"Deleting previous public message for command {command}")
                    await last_messages[command]["public"].delete()
                except HTTPException as e:
                    print(f"Failed to delete public message: {e}")
            last_messages[command]["public"] = await message.channel.send(response)
    except Exception as e:
        logger.exception("Error sending message")
        print(e)

# STEP 3 HANDLING STARTUP
@client.event
async def on_ready() -> None:
    print(f'Hello {client.user}, RAGNAROK-HUNTER is ready')
    for guild in client.guilds:
        channel: TextChannel = utils.get(guild.text_channels, name='luitest')
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
