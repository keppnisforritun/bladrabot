from discord.ext import commands
import discord
import config
import os
import importlib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bot = commands.Bot(command_prefix = "!", # TODO: Make this configurable? (With the possibility of using mentions)
                   description    = "Hæ! Ég heiti Blaðra!",
                   pm_help        = True)

@bot.event
async def on_ready():
    print("Tengdur! Jei!")
    print("User: {}".format(bot.user.name))
    print("ID: {}\n".format(bot.user.id))

def load_extension(bot, name, conf):
    if name in bot.extensions:
        return

    lib = importlib.import_module('bladra.' + name)
    if not hasattr(lib, 'setup'):
        del lib
        del sys.modules[name]
        raise discord.ClientException('extension does not have a setup function')

    lib.setup(bot, conf)
    bot.extensions[name] = lib

def main():
    for mod, conf in config.modules.items():
        if conf['enabled']:
            conf['data_dir'] = os.path.join(config.data_dir, mod)
            try:
                load_extension(bot, 'modules.' + mod, conf)
            except (AttributeError, ImportError) as ex:
                print("Úps, náði ekki að hlaða {}\n{}".format(mod, str(ex)))

    bot.run(config.discord_secret_token)

if __name__ == "__main__":
    main()

