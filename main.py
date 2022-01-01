import discord

from musicbot import MusicCog
from eticog import KekCog
from dotenv import load_dotenv
from discord.ext import commands

import os


load_dotenv()

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")


if __name__ == "__main__" :
    
    intents = discord.Intents().all()
    client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix=[MusicCog.MUSIC_COMMAND_SYMBOL, KekCog.KEK_COMMAND_SYMBOL],intents=intents)
    bot.add_cog(MusicCog(bot))
    bot.add_cog(KekCog(bot))
    bot.run(DISCORD_TOKEN)

        
    @bot.event
    async def on_ready():
        print("ready")
