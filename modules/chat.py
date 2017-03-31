from discord.ext import commands
import discord

class Chat():
    """ Blöðrublaður """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def halló(self, ctx):
        await self.bot.say("Halló {0.mention}!".format(ctx.message.author))

def setup(bot):
    bot.add_cog(Chat(bot))
