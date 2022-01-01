import discord

from musicbot import MusicCog
from EtiCog import EtiCog
from LussiCog import LussiCog
from BoissiCog import BoissiCog
from dotenv import load_dotenv
from discord.ext import commands

import os


load_dotenv()

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")


if __name__ == "__main__" :
    
    intents = discord.Intents().all()
    client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix=[MusicCog.MUSIC_COMMAND_SYMBOL, EtiCog.COMMAND_SYMBOL, BoissiCog.COMMAND_SYMBOL, LussiCog.COMMAND_SYMBOL],intents=intents)
    bot.add_cog(MusicCog(bot))
    bot.add_cog(EtiCog(bot))
    bot.add_cog(LussiCog(bot))
    bot.add_cog(BoissiCog(bot))
    
    @bot.event
    async def on_ready():
        print("ready")

    bot.run(DISCORD_TOKEN)

        

