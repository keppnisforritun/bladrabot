from discord.ext import commands

class Basics():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def halló(self, ctx):
        await self.bot.say("Halló {0.mention}!".format(ctx.message.author))

def setup(bot, config):
    bot.add_cog(Basics(bot))
