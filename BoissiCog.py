import discord
from discord.ext import commands
import UserData
import asyncio
import os
import random as rand
import sqlite3 as db
import requests as req
import json

KEK_SWITCH = True
DEV_PREFIX = "$"
dir_path = os.path.dirname(os.path.realpath(__file__))

#GB API
GB_KEY = "c9e27565a39842757c0797c900b06c5e4916c042"
GB_SRCH_URL = "https://www.giantbomb.com/api/search/?api_key=%s" % GB_KEY
GB_GAME_URL = "https://www.giantbomb.com/api/game/[guid]/?api_key=%s" % GB_KEY

#MESSAGES
NOS_OPTIONS = "Voici nos options:"
PAS_OPTIONS = "On a pas d'options!"
TIMEOUT_MSG = "Ah pis laisse faire..."

#ERROR MESSAGES
ERR_GENERIC = "Oops! Ç'a pas marché!"
ERR_OOB_VALUE = "C'est pas compliqué! Un chiffre en 1 pis 10! Come on!"

#HELP MESSAGES
HELP_ADDGAME = "Usage: !addgame [Game Name] [Max. Players]"

#PATHS
PIZZA_IMG = dir_path + "/res/pizza/img/"
PIZZA_SND = dir_path + "/res/pizza/snd/"
DB = dir_path + "/res/bot.db"

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
            srch = ' '.join(parts)

            params={
                ('field_list', 'id,guid,name,image,deck,genres,platforms,site_detail_url'),
                ('format', 'json')
            }
            guid = await self.find_game(ctx, srch)
            r = req.get(GB_GAME_URL.replace('[guid]', guid), params=params, headers={'User-Agent': 'MyDiscordApp'})
            data = r.json()['results']
            game = Game(data, maxp)
            await game.write()
            await ctx.send("%s was added to the game list." % data['name'])
            await ctx.send(embed=game.embed())

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
            self.games = []
            await ctx.send(NOS_OPTIONS)
            if q:
                for game in q:
                    data = {
                        'id': game[0],
                        'guid': game[1],
                        'name': game[2],
                        'image': json.loads(game[3]),
                        'deck': game[4], # desc in Obj
                        'genres': json.loads(game[5]),
                        'platforms': json.loads(game[6]),
                        'site_detail_url': game[7] # link in Obj
                    }
                    maxp = game[8]
                    self.games.append(Game(data, maxp))
                for game in self.games:
                    await ctx.send(embed=game.embed())
            else:
                await ctx.send(PAS_OPTIONS)
        except:
            await ctx.send(ERR_GENERIC)

    async def find_game(self, ctx, srch):
        try:
            params = [
                ('query', srch),
                ('resources', 'game'),
                ('field_list', 'name,guid'),
                ('format', 'json')
            ]
            r = req.get(GB_SRCH_URL, params=params, headers={'User-Agent': 'MyDiscordApp'})
            data = r.json()
            i = 0
            msg = "Multiple results. Choose one:\n"
            for game in data['results']:
                i += 1
                msg += "%i. %s\n" % (i, game['name'])
            await ctx.send(msg)

            def check(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                ans = await self.bot.wait_for('message', timeout=30, check=check) # Wait for answer
                num = int(ans.content)
                if num > 0 and num <= 10:
                    await ctx.send("You chose %i: %s" % (num, data['results'][num-1]['name']))
                    gameid = data['results'][num-1]['guid']
                    return gameid
                else:
                    raise ValueError

            except asyncio.TimeoutError:
                await ctx.send(TIMEOUT_MSG)

            except ValueError:
                await ctx.send(ERR_OOB_VALUE)

            except:
                await ctx.send(ERR_GENERIC)

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


class Game :
    
    def __init__(self, data, maxp):
        self.maxp = maxp
        self.id = data['id'] # Used as primary key in db
        self.guid = data['guid'] # Used for querying single game
        self.name = data['name']
        self.image = data['image']
        self.desc = data['deck']
        self.genres = data['genres']
        self.platforms = data['platforms']
        self.link = data['site_detail_url']

    async def write(self):
        con = db.connect(DB)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Games(
            id INTEGER PRIMARY KEY,
            guid STRING,
            name STRING,
            image STRING,
            desc STRING,
            genres STRING,
            platforms STRING,
            link STRING,
            max_players INTEGER)
            ''')
        cur.execute("REPLACE INTO Games VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            self.id,
            self.guid,
            self.name,
            json.dumps(self.image),
            self.desc,
            json.dumps(self.genres),
            json.dumps(self.platforms),
            self.link,
            self.maxp
            ])
        con.commit()
        con.close()

    def embed(self):
        embed = discord.Embed(
            title = self.name,
            color = 0xff8000,
            description = "*%s*" % self.desc,
            url = self.link)
        embed.set_image(url=self.image['small_url'])
        embed.add_field(name='Kekeurs', value=self.maxp)
        s = ""
        for genre in self.genres:
            s += "%s\n" % genre['name']
        embed.add_field(name='Genre', value=s)
        embed.set_footer(text="Merci à Giant Bomb pour l'API")
        return embed
        
