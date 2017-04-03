import async_timeout
import aiohttp

def get_channel(bot, name):
    for server in bot.servers:
        for channel in server.channels:
            if channel.name == name:
                return channel
    return None

def get_channels(bot, names):
    names = set(names)
    res = []
    for server in bot.servers:
        for channel in server.channels:
            if channel.name in names:
                res.append(channel)
    return res

async def download(loop, url, parameters={}, verify_ssl=True):
    # A semi-generic download function, might need some tweaking later on
    async with aiohttp.ClientSession(loop=loop, connector=aiohttp.TCPConnector(verify_ssl=verify_ssl)) as session:
        with async_timeout.timeout(10):
            async with session.get(url, params=parameters) as resp:
                return await resp.read()

