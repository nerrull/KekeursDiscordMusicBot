import discord
from discord.ext import commands


class LussiCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='helloL', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from LussiCog")
