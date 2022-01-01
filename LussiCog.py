import discord
from discord.ext import commands


class LussiCog(commands.Cog):
    COMMAND_SYMBOL = "*"

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx) :
        return ctx.prefix == self.COMMAND_SYMBOL

    @commands.command(name='helloL', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from LussiCog")
