import discord
from discord import channel
from discord.ext import commands
from async_timeout import timeout
from functools import partial
import random
from UserData import NameID, StingerMap
import asyncio
from db.lines import tonymessage, mladies
from database import BotDB
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
gif_path = os.path.join(dir_path, "res", "gif")



class RichCog(commands.Cog):
    CUSTOM_COMMAND_SYMBOL = "~!"

    def __init__(self, bot):
        self.bot = bot
        self.database = BotDB()
        self.DEV_PREFIX = os.getenv("dev_prefix")


    @commands.command(name='helloE', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from EtiCog")

    @commands.command(name='list', description="list users")
    async def summon_(self, ctx, *, channel: discord.VoiceChannel=None):
        for member in ctx.guild.members:
           await ctx.send("{} : {}".format(member.name, member.id))

    @commands.command(name='addcomm', description="add command")
    async def addcomm_(self, ctx):
            parts = ctx.message.content.strip( self.DEV_PREFIX + "addcomm").split("|")
            if (len(parts) == 2 ):
                self.database.add_command(parts[0].strip(" "), parts[1])
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.CUSTOM_COMMAND_SYMBOL):
            key = message.content.strip(self.CUSTOM_COMMAND_SYMBOL)
            content = self.database.get_command(key)
            if (content):
                ctx = await self.bot.get_context(message)
                await ctx.send(content)
                #if (ctx.valid):

    @commands.command(name='mlady', aliases=['mlord'], description="A doff of the cap")
    async def mlady_(self, ctx):
        line = mladies[random.randrange(0, len(mladies))]
        await ctx.send(line, file=discord.File(os.path.join(gif_path, "mlady.gif" )))
                
    @commands.command(name='tony')
    async def tony_(self, ctx):
        await ctx.send(tonymessage)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        return
        # ctx = await self.bot.get_context()
        # await ctx.send("yo")

        # if message.content.startswith(self.CUSTOM_COMMAND_SYMBOL):
        #     key = message.content.strip(self.CUSTOM_COMMAND_SYMBOL)
        #     content = self.database.get_command(key)
        #     if (content):
        #         await ctx.send(content)
        #         #if (ctx.valid):

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == None and  after.channel!= None:
            try :
                player = StingerPlayer(self.bot, after.channel.guild)
                id = NameID(member.id)
                await player.play_sting(player.get_stinger_file(id))
            except:
                return

    # @commands.command(name='sting_test')
    # async def sting_test_(self, ctx):
    #     player = StingerPlayer(ctx)
    #     await player.play_sting("pp")

    @commands.command(name='sting_test')
    async def sting_test_(self, ctx):
        try :
            id = NameID(int(ctx.message.content.split(" ")[-1]))
            if (id in StingerMap.keys()):
                player = StingerPlayer(self.bot, ctx.channel.guild) 
                await player.play_sting(player.get_stinger_file(id))
        except:
            return

class StingerPlayer :
    __slots__ = ('bot', '_guild', '_channel', 'over')

    def __init__(self, bot, guild):
        self.bot = bot
        self._guild = guild
        self.over = asyncio.Event()

    def get_stinger_file(self, id):
         file_path = os.path.join(dir_path, "stingers", StingerMap[id])
         return file_path

    async def play_sting(self, sting_file):
        self.over.clear()
        await self.bot.wait_until_ready()
        self._guild.voice_client.play(discord.FFmpegPCMAudio(source=sting_file), after=lambda _: self.bot.loop.call_soon_threadsafe(self.over.set))
        await self.over.wait()
