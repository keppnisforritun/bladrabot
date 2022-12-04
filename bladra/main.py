from discord.ext import commands
import discord
import config
import os
import importlib
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = commands.when_mentioned_or(*config.prefixes),
                   description    = "Hæ! Ég heiti Blaðra!",
                   pm_help        = True,
                   intents        = intents)

@bot.event
async def on_ready():
    print("Tengdur! Jei!")
    print("User: {}".format(bot.user.name))
    print("ID: {}\n".format(bot.user.id))

async def load_extension(bot, name, conf):
    if name in bot.extensions:
        return

    lib = importlib.import_module('bladra.' + name)
    if not hasattr(lib, 'setup'):
        del lib
        del sys.modules[name]
        raise discord.ClientException('extension does not have a setup function')

    await lib.setup(bot, conf)

async def main():

    async with bot:
        for mod, conf in config.modules.items():
            if conf['enabled']:
                conf['data_dir'] = os.path.join(config.data_dir, mod)
                try:
                    await load_extension(bot, 'modules.' + mod, conf)
                except (AttributeError, ImportError) as ex:
                    print("Úps, náði ekki að hlaða {}\n{}".format(mod, str(ex)))

        await bot.start(config.discord_secret_token)

if __name__ == "__main__":
    asyncio.run(main())

