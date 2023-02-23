import discord

from musicbot_dlp import MusicCog
from RichCog import RichCog
from LussiCog import LussiCog
from BoissiCog import BoissiCog
from dotenv import load_dotenv
from discord.ext import commands

import os

load_dotenv()

# Get the API token from the .env file.
DISCORD_TOKEN = os.getenv("discord_token")
DEV_PREFIX = os.getenv("dev_prefix")

if __name__ == "__main__" :
    
    intents = discord.Intents().all()
    client = discord.Client(intents=intents)

    bot = commands.Bot(command_prefix=[DEV_PREFIX],intents=intents)
    bot.add_cog(MusicCog(bot))
    bot.add_cog(RichCog(bot))
    bot.add_cog(LussiCog(bot))
    bot.add_cog(BoissiCog(bot))
    
    @bot.event
    async def on_ready():
        print("ready")

    bot.run(DISCORD_TOKEN)

        

