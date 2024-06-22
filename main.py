import bot
import discord
from discord.ext import commands
import os
import logging

if __name__ == '__main__':
    #run the bot
    bot.run_discord_bot()

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing arguments. Please check your input.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Use !help to see available commands.')
    else:
        await ctx.send(f'An error occurred: {str(error)}')


# Start bot
#bot.run(TOKEN)