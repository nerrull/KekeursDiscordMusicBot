import discord
from discord.ext import commands
import UserData
import asyncio
import os
import random as rand
import sqlite3 as db
from enum import Enum, auto

#MESSAGES
NOS_OPTIONS = "Voici nos options:"
PAS_OPTIONS = "On a pas d'options!"
ERR_GENERIC = "Oops! Ç'a pas marché!"

#HELP MESSAGES
HELP_ADDGAME = "Usage: !addgame [Game Name] [Max. Players]"

#PATHS
PIZZA_IMG = os.path.abspath("res/pizza/img/")
PIZZA_SND = os.path.abspath("res/pizza/snd/")
DB = "res/bot.db"

class BoissiCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    def get_rand_file(self, base_uri):
        flist = list(os.scandir(base_uri))
        r = rand.randrange(0, len(flist))
        return flist[r].path

    async def temp_mute(self, member, time):
        await member.edit(mute=True)
        await asyncio.sleep(time)
        await member.edit(mute=False)

    @commands.command(name='pizzatime', aliases=['pizza', 'dominos'], description="It's pizza time!")
    async def pizza_(self, ctx):
        player = AudioPlayer(self.bot, ctx.channel.guild)
        await ctx.send("It's pizza time!", file=discord.File(self.get_rand_file(PIZZA_IMG)))
        await player.play(self.get_rand_file(PIZZA_SND))

    @commands.command(name='addgame', description='Add a game to the database')
    async def add_game_(self, ctx, *, arg=None):
        try:
            parts = arg.split(" ")
            l = len(parts)
            maxp = parts.pop(l-1)
            name = ' '.join(parts)

            if maxp and name:
                con = db.connect(DB)
                cur = con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS Games (name text, max_players integer)")
                cur.execute("INSERT INTO Games VALUES (?,?)", (name, maxp))
                con.commit()
                con.close()
                await ctx.send("'%s' was added to the game list" % name)
            else:
                await ctx.send(HELP_ADDGAME)
        except:
            await ctx.send(HELP_ADDGAME)

    @commands.command(name='gamelist', aliases=['options', 'jeux', 'games'], description='List of games to play with the bois')
    async def list_games_(self, ctx, numpl=0):
        try:
            con = db.connect(DB)
            cur = con.cursor()
            if numpl:
                q = cur.execute("SELECT * FROM Games WHERE max_players >= ?", (numpl,)).fetchall()
            else:
                q = cur.execute("SELECT * FROM Games").fetchall()
            await ctx.send(NOS_OPTIONS)
            if q:
                i = 0
                for game in q:
                    i += 1
                    await ctx.send("%i. %s pour %i kekeurs" % (i, game[0], game[1]))
            else:
                await ctx.send(PAS_OPTIONS)
        except:
            await ctx.send(ERR_GENERIC)


class AudioPlayer :
    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'over', 'current', 'np', 'volume')

    def __init__(self, bot, guild):
        self.bot = bot
        self._guild = guild
        self.over = asyncio.Event()

    async def play(self, file):
        self.over.clear()
        await self.bot.wait_until_ready()
        self._guild.voice_client.play(discord.FFmpegPCMAudio(source=file), after=lambda _: self.bot.loop.call_soon_threadsafe(self.over.set))
        await self.over.wait()

