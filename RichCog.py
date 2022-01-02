import discord
from discord import channel
from discord.ext import commands
from async_timeout import timeout
from functools import partial

from UserData import NameID, StingerMap
import asyncio

import db
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

tonymessage = '''
Voici mes joueurs sur le marché des échanges. Je suis principalement intéressé par un goaler, mais toute offre raisonnable sera acceptée:

Evgeny Kuznetsov (Attaquant des Capitals): 7,200M // 30 pts en 28 games, joue sur la ligne d'Ovy

Nicklas Backstrom (Attaquant des Capitals): 9,200M // revient d'une blessure et n'a joué qu'un match (1A 1PPP 5SOG 2Hit)

Chandler Stephenson (Attaquant de Vegas): 2,750M // 11pts dans ses 10 dernières games, 4PPP. Lent début de saison mais il se réchauffe

Ivan Barbashev (Attaquant des Blues) 2,250M // Poor man's Tarasenko, mais a 12pts à ses 10 dernières games


Shea Theodore (Défenseur de Vegas): 5,200M // 11pts à ses 10 dernières games, 5PPP. Surement l'offre la plus alléchante de la gang

Devon Toews (Défenseur du Colorado): 4,100M // 20pts en 16 games, dans l'ombre de Cale Makar, mais il produit autant


Anthony Stolarz (Goaler d'Anaheim): 0,950M // Backup de John Gibson, mais a 2 shutouts en 10 games pis des pas pires stats
'''

class RichCog(commands.Cog):
    CUSTOM_COMMAND_SYMBOL = "~!"

    def __init__(self, bot):
        self.bot = bot
        self.database = db.BotDB()
    @commands.command(name='helloE', description="")
    async def hello_(self, ctx):
        await ctx.send("Hello from EtiCog")

    @commands.command(name='list', description="list users")
    async def summon_(self, ctx, *, channel: discord.VoiceChannel=None):
        for member in ctx.guild.members:
           await ctx.send("{} : {}".format(member.name, member.id))

    @commands.command(name='addcomm', description="add command")
    async def addcomm_(self, ctx):
            parts = ctx.message.content.strip("~addcomm").split("|")
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
            player = StingerPlayer(self.bot, after.channel.guild)
            await player.play_sting(player.get_stinger_file(member))

    # @commands.command(name='sting_test')
    # async def sting_test_(self, ctx):
    #     player = StingerPlayer(ctx)
    #     await player.play_sting("pp")

    @commands.command(name='sting_test')
    async def sting_test_(self, ctx):
        id = NameID(int(ctx.message.content.split[" "][-1]))
        if (id in StingerMap.keys):
            player = StingerPlayer(self.bot, ctx.channel.guild)
            await player.play_sting(id)

class StingerPlayer :
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'over', 'current', 'np', 'volume')


    def __init__(self, bot, guild):
        self.bot = bot
        self._guild = guild
        self.over = asyncio.Event()

    def get_stinger_file(self, member):
         file_path = os.path.join(dir_path, "stingers", StingerMap[NameID(member.id)])
         return file_path

    async def play_sting(self, sting_file):
        self.over.clear()
        await self.bot.wait_until_ready()
        self._guild.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=sting_file), after=lambda _: self.bot.loop.call_soon_threadsafe(self.over.set))
        self.over.wait()
