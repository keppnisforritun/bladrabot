from discord.ext import commands
from bs4 import BeautifulSoup
from random import randint
import async_timeout
import urllib.parse
import discord
import aiohttp
import string
import os

async def download(loop, url, parameters={}):
    # A semi-generic download function, might need some tweaking later on
    async with aiohttp.ClientSession(loop=loop) as session:
        with async_timeout.timeout(10):
            async with session.get(url, params=parameters) as resp:
                return await resp.read()

class Kattis():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command()
    async def kattis(self, *name : str):
        """ Skilar stigafjölda íslenskum notanda á open.kattis.com """
        name = " ".join(name)
        if name == "":
            return
        doc = await download(self.bot.loop, "https://open.kattis.com/countries/ISL")
        soup = BeautifulSoup(doc, "html5lib")
        f = soup.find("td", string=name)
        if f is None:
            f = soup.find("a", string="href=\"/users/{}\"".format(name))
            print(soup.find("a", string=name))
            if f is None:
                return

        prev = list(f.previous_siblings)
        rank = prev[1].text.replace(" ", "").strip()
        siblings = list(f.next_siblings)
        score = siblings[-2].text

        ranking = discord.Embed(
            title="Kattis ranklist",
            description="Rank: {}\nScore: {}".format(rank, score),
            color=discord.Colour.purple())

        await self.bot.say(embed=ranking)

def setup(bot, config):
    bot.add_cog(Kattis(bot, config))

