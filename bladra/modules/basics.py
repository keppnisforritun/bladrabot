from discord.ext import commands
import urllib.parse

# https://stackoverflow.com/a/55701877
class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# testað
    @commands.command(pass_context=True)
    async def halló(self, ctx):
        await ctx.send("Halló {0.mention}!".format(ctx.message.author))

# testað
    @commands.command()
    async def wiki(self, ctx, *search : str):
        search = ' '.join(search)
        await ctx.send("https://wiki.algo.is/_search?%s" % urllib.parse.urlencode({'patterns': search}))

# skv docs á setup(...) bara að taka inn bot
def setup(bot):
    bot.add_cog(Basics(bot))

