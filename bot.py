import discord
from discord.ext import commands
import responses

# Define the intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events (e.g., on_message)

# Create the bot with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTI1NDAyMzA0NzcyNDE0MjY0NQ.GhlNVs.O08a-Az-mLhXPDL-b6AEkVSdckypv4kP1RsvaA'
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    client.run(TOKEN)