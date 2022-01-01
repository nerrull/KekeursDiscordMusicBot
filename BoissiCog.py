import discord
from discord.ext import commands


class BoissiCog(commands.Cog):
    COMMAND_SYMBOL = "$"

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx) :
        return ctx.prefix == self.COMMAND_SYMBOL

    @commands.command(name='helloB', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from BoissiCog")

    @commands.command(name='keko', description="")
    async def keko_(self, ctx):
        await ctx.send("keko")