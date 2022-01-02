import discord
from discord.ext import commands


class LussiCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='helloL', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from LussiCog")

    @commands.command(name='tony2')
    async def kek_(self, ctx):
        await ctx.send(''':salty:''')
    
    
    tonySel = False
    @commands.command(name='sel')
    async def sel_(self, ctx):
        if (self.tonySel == True):
            self.tonySel = False
        elif (self.tonySel == False):
            self.tonySel = True
    
    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.author.id)
        if (message.author.id == 172835127016030208 and self.tonySel == True):
            await message.add_reaction("🧂")  
