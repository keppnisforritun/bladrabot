from bladra.util import download, get_channels
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import random
import async_timeout
import asyncio
import urllib.parse
import aiohttp
import string
import os

class Kattis():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.lists = [ {} for _ in range(len(self.config['lists'])) ]
        self.info = [ None for _ in range(len(self.config['lists'])) ]

    async def monitor_lists(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed:
            try:
                for i, lst in enumerate(self.config['lists']):
                    try:
                        res = await download(self.bot.loop, lst['url'], verify_ssl=False)
                    except e:
                        print(e)
                        continue
                    doc = BeautifulSoup(res, "html5lib")
                    site = doc.select('.header-title')[0].text.strip()
                    new = {}
                    for row in doc.select('.table-kattis tbody')[-1].find_all('tr'):
                        cols = row.find_all('td')
                        rank = int(cols[0].text)
                        name = next(cols[1].children)
                        score = cols[-1].text.strip()
                        username = name.attrs['href'].split('/')[-1]
                        name = name.text.strip()
                        new[username] = (rank, name, score)

                    old = self.lists[i]
                    self.info[i] = (lst['url'], site)
                    self.lists[i] = new

                    for (username, (rank, name, score)) in sorted(new.items(), key=lambda x: -x[1][0]):
                        if username in old and rank < old[username][0]:
                            for channel in get_channels(self.bot, lst['channels']):
                                congrats = random.choice([ 'Til hamingju!', 'Svalt!', 'Næs!', 'Vel gert!', 'Hellað.' ])
                                msg = '%s hefur nú náð %s stigum á %s, og hoppar því upp í %d. sæti%s %s' % (name, score, site, rank, random.choice(['!', '.']), congrats)
                                msg += ' [%s]' % lst['url'] # TODO: Better way to display the link?
                                await self.bot.send_message(channel, msg)
            except e:
                print(e)

            await asyncio.sleep(self.config['interval'])

    @commands.command()
    async def kattis(self, *query : str):
        """Fletta upp íslenskum Kattis notendum"""

        def normalize(s):
            return s.lower().replace(' ', '')

        query = normalize(''.join(query))
        if len(query) < 4 or (len(query) < 6 and query.endswith('son')):
            return

        for (lst, (url, site)) in zip(self.lists, self.info):
            for (username, (rank, name, score)) in sorted(lst.items(), key=lambda x: -x[1][0]):
                if query in normalize(username) or query in normalize(name):

                    ranking = discord.Embed(
                        title=name,
                        description="{}. sæti á {}\nmeð {} stig".format(rank, site, score),
                        url=url,
                        color=discord.Colour.purple())

                    await self.bot.say(embed=ranking)

def setup(bot, config):
    katt = Kattis(bot, config)
    bot.loop.create_task(katt.monitor_lists())
    bot.add_cog(katt)

