from discord.ext import commands
import discord
import config
import os
import importlib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

bot = commands.Bot(command_prefix = commands.when_mentioned_or(*config.prefixes),
                   description    = "Hæ! Ég heiti Blaðra!",
                   pm_help        = True)

@bot.event
async def on_ready():
    print("Tengdur! Jei!")
    print("User: {}".format(bot.user.name))
    print("ID: {}\n".format(bot.user.id))

# this function is only for the kattis/events module until the setup(...) is fixed
def old_load_extension(bot, name, conf):
    if name in bot.extensions:
        return

    lib = importlib.import_module('bladra.' + name)
    if not hasattr(lib, 'setup'):
        del lib
        del sys.modules[name]
        raise discord.ClientException('extension does not have a setup function')

    lib.setup(bot, conf)
# https://stackoverflow.com/a/20019382
    #setattr(bot.extensions, name, lib)

def load_extension(bot, name):
    if name in bot.extensions:
        return

    lib = importlib.import_module('bladra.' + name)
    if not hasattr(lib, 'setup'):
        del lib
        del sys.modules[name]
        raise discord.ClientException('extension does not have a setup function')

    lib.setup(bot)
# https://stackoverflow.com/a/20019382
    #setattr(bot.extensions, name, lib)
    #bot.extensions[name] = lib

def main():
    for mod, conf in config.modules.items():
        if conf['enabled']:
            conf['data_dir'] = os.path.join(config.data_dir, mod)
            try:
                # þetta if/else er bara þangað til það er búið að laga setup(...) fyrir kattis/events module
                if mod == 'kattis' or mod == 'events': old_load_extension(bot, 'modules.' + mod, conf)
                else: load_extension(bot, 'modules.' + mod)
            except (AttributeError, ImportError) as ex:
                print("Úps, náði ekki að hlaða {}\n{}".format(mod, str(ex)))

    bot.run(config.discord_secret_token)

if __name__ == "__main__":
    main()

