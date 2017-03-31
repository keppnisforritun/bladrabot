from discord.ext import commands
import asyncio
import discord
import secret

description = "Hæ! Ég heiti Blaðra!"
prefix = "!"

bot = commands.Bot(command_prefix=prefix, description=description, pm_help=True)
client = discord.Client()

init = [
    "modules.chat",
    "modules.scrape"
]

@bot.event
async def on_ready():
    print("Tengdur! Jei!")
    print("User: {}".format(bot.user.name))
    print("ID: {}\n".format(bot.user.id))

if __name__ == "__main__":
    for extension in init:
        try:
            bot.load_extension(extension)
        except (AttributeError, ImportError) as ex:
            print("Úps, náði ekki að hlaða {}\n{}".format(extension, str(ex)))

bot.run(secret.token)
