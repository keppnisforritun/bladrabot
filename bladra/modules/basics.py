from discord.ext import commands
import urllib.parse

class Basics():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def halló(self, ctx):
        await self.bot.say("Halló {0.mention}!".format(ctx.message.author))

    @commands.command()
    async def wiki(self, *search : str):
        search = ' '.join(search)
        await self.bot.say("https://wiki.algo.is/_search?%s" % urllib.parse.urlencode({'patterns': search}))

def setup(bot, config):
    bot.add_cog(Basics(bot))

