from discord.ext import commands
from bladra.util import download
from bs4 import BeautifulSoup
from random import randint
import urllib.parse
import string
import os

async def latex_get(loop, equation):
    s = urllib.parse.quote_plus(equation)
    url = "https://chart.googleapis.com/chart?"
    parameters = {
        "cht": "tx", 
        "chl": equation,
        "chf": "bg,s,36393E",
        "chco": "EEEEEE"
    }
    return await download(loop, url, parameters)

def generate_filename(extension=".png"):
    s = ""
    l = len(string.hexdigits) - 1
    for _ in range(12):
        s += string.hexdigits[randint(0, l)]
    return s + extension

class LaTeX():
    def __init__(self, bot):
        self.bot = bot
        self.math = []

    @commands.command()
    async def latex(self, *equation : str):
        """ Parses LaTeX markup into a png via Google Charts 
            \\displaystyle is forced for nicer and bigger equations """
        equation = " ".join(equation)
        if equation == "":
            return
        if len(equation) >= 200:
            return
        if equation[0] == "`":
            try:
                if equation[0:3] == "```":
                    equation = equation[3:-3]
                else:
                    equation = equation[1:-1]
            except IndexError:
                equation = equation[1:-1]
        try:
            if equation[0:3].lower() == "tex":
                equation = equation[3:]
        except IndexError: pass

        equation = "\\displaystyle " + equation

        res = await latex_get(self.bot.loop, equation)
        filename = generate_filename()
        with open(filename, "wb") as f:
            f.write(res)
        try:
            # self.math.append(await self.bot.upload(filename))
            await self.bot.upload(filename)
        finally:
            os.remove(filename)

    # @commands.command()
    # async def remove(self):
    #     """ Removes LaTeX images previously posted in the chat """
    #     while self.math:
    #         message = self.math.pop()
    #         await self.bot.delete_message(message)

def setup(bot, config):
    bot.add_cog(LaTeX(bot))

