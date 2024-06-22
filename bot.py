import discord
from discord.ext import commands
import responses

# Define the intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events (e.g., on_message)

# Create the bot with the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTI1NDAyMzA0NzcyNDE0MjY0NQ.GhlNVs.O08a-Az-mLhXPDL-b6AEkVSdckypv4kP1RsvaA'
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        #to prevent infinite loops 
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print (f"{username}: said ]{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:] #read the first and process the rest
            await send_message(message, user_message, is_private=True)
        else: 
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)