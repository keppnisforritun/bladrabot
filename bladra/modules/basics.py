from discord.ext import commands
import urllib.parse

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def halló(self, ctx):
        await ctx.send("Halló {0.mention}!".format(ctx.message.author))

    @commands.command()
    async def wiki(self, ctx, *search : str):
        search = ' '.join(search)
        await ctx.send("https://wiki.algo.is/_search?%s" % urllib.parse.urlencode({'patterns': search}))

async def setup(bot, config):
    await bot.add_cog(Basics(bot))

