from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
import asyncio

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
print(TOKEN)

# STEP 1 BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# STEP 2 MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return

    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 3 HANDLING STARTUP
@client.event
async def on_ready() -> None:
    print(f'Hello {client.user}, Astral Bot Timer is ready')

# STEP 4 HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
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