from bladra.util import download, get_channels, get_channel
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import random
import async_timeout
import asyncio
import urllib.parse
import aiohttp
import string
import sys
import os

class Account():
    def __init__(self, username, name, rank, score):
        self.username = username
        self.name = name
        self.rank = rank
        self.score = score
        self.thousand_reached = 0
        self.last_score = 0

class Kattis():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.lists = [ {} for _ in range(len(self.config['lists'])) ]
        self.info = [ None for _ in range(len(self.config['lists'])) ]
        self.new_problems = set()

    async def monitor_lists(self):
        await self.bot.wait_until_ready()

        first = True
        while not self.bot.is_closed:

            if first:
                first = False
            else:
                await asyncio.sleep(self.config['interval'])

            try:
                # TODO: Make configurable?
                res = await download(self.bot.loop, 'https://open.kattis.com/problems?order=added&dir=desc')
                doc = BeautifulSoup(res, "html5lib")

                kattis_channel = get_channel(self.bot, 'kattis')

                new = set()
                for row in doc.select('.problem_list .name_column a'):
                    pid = row.attrs['href'].split('/')[-1]
                    title = row.text
                    if self.new_problems and pid not in self.new_problems:
                        await self.bot.send_message(kattis_channel,
                                'Nýtt dæmi: %s [https://open.kattis.com/problems/%s]' % (title, pid))
                    new.add(pid)

                self.new_problems = new
            except:
                import traceback
                sys.stderr.write('%s\n' % traceback.format_exc())

            try:
                for i, lst in enumerate(self.config['lists']):
                    try:
                        res = await download(self.bot.loop, lst['url'], verify_ssl=False)
                    except:
                        import traceback
                        sys.stderr.write('%s\n' % traceback.format_exc())
                        continue
                    doc = BeautifulSoup(res, "html5lib")
                    site = doc.select('.header-title')[0].text.strip()
                    new = {}
                    for row in doc.select('.table-kattis tbody')[-1].find_all('tr'):
                        cols = row.find_all('td')
                        rank = int(cols[0].text)
                        name = next(cols[1].children)
                        score = float(cols[-1].text.strip())
                        username = name.attrs['href'].split('/')[-1]
                        name = name.text.strip()
                        acc = Account(username, name, rank, score)
                        if username in self.lists[i]:
                            old = self.lists[i][username]
                            acc.thousand_reached = old.thousand_reached
                            acc.last_score = old.last_score
                        new[username] = acc

                    for (username, acc) in sorted(new.items(), key=lambda x: -x[1].rank):
                        if username not in self.lists[i]:
                            continue
                        old = self.lists[i][username]
                        if acc.rank < old.rank and acc.score > acc.last_score + 10:
                            acc.last_score = acc.score
                            for channel in get_channels(self.bot, lst['channels']):
                                congrats = random.choice([ 'Til hamingju!', 'Svalt!', 'Næs!', 'Vel gert!', 'Hellað.', 'Sææælll', 'Magnað.', 'Legendary.' ])
                                msg = '%s hefur nú náð %s stigum á %s, og hoppar því upp í %d. sæti%s %s' % (acc.name, acc.score, site, acc.rank, random.choice(['!', '.']), congrats)
                                msg += ' [%s]' % lst['url'] # TODO: Better way to display the link?
                                await self.bot.send_message(channel, msg)
                        if int(acc.score / 1000) > max(int(old.score / 1000), acc.thousand_reached):
                            acc.thousand_reached = int(acc.score / 1000)
                            arr = ['Núll', 'Ein', 'Tvö', 'Þre', 'Fjór', 'Fimm', 'Sex', 'Sjö', 'Átt', 'Ní', 'Tí']
                            hurr = min(int(acc.score / 1000), len(arr)-1)
                            msg = '%s var að komast yfir %s stig á %s! %sfalt húrra!' % (acc.name, int(acc.score / 1000) * 1000, site, arr[hurr])
                            msg += ' [%s]' % lst['url'] # TODO: Better way to display the link?
                            for channel in get_channels(self.bot, lst['channels']):
                                await self.bot.send_message(channel, msg)
                            for _ in range(hurr):
                                await asyncio.sleep(1)
                                for channel in get_channels(self.bot, lst['channels']):
                                    await self.bot.send_message(channel, 'Hipp, hipp, húrra!')

                    old = self.lists[i]
                    self.info[i] = (lst['url'], site)
                    self.lists[i] = new
            except:
                import traceback
                sys.stderr.write('%s\n' % traceback.format_exc())

    @commands.command()
    async def kattis(self, *query : str):
        """Fletta upp íslenskum Kattis notendum"""

        def normalize(s):
            return s.lower().replace(' ', '')

        query = normalize(''.join(query))
        if len(query) < 4 or (len(query) < 6 and query.endswith('son')):
            return

        for (lst, site) in zip(self.lists, self.info):
            if not site:
                # No info about site yet
                continue
            (url, site) = site
            for (username, acc) in sorted(lst.items(), key=lambda x: -x[1].rank):
                if query in normalize(acc.username) or query in normalize(acc.name):

                    ranking = discord.Embed(
                        title=acc.name,
                        description="{}. sæti á {}\nmeð {} stig".format(acc.rank, site, acc.score),
                        url=url,
                        color=discord.Colour.purple())

                    await self.bot.say(embed=ranking)

def setup(bot, config):
    katt = Kattis(bot, config)
    bot.loop.create_task(katt.monitor_lists())
    bot.add_cog(katt)

