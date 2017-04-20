from bladra.util import get_channels, download
import asyncio
import os
import datetime
import json
import hashlib
import discord
import sys

def describe_datetime(dt):
    day = [
        'mánudag',
        'þriðjudag',
        'miðvikudag',
        'fimmtudag',
        'föstudag',
        'laugardag',
        'sunnudag',
    ]
    month = [
        'janúar',
        'febrúar',
        'mars',
        'apríl',
        'maí',
        'júní',
        'júlí',
        'ágúst',
        'september',
        'október',
        'nóvember',
        'desember',
    ]

    now = datetime.datetime.now()
    ad = now.toordinal()
    bd = dt.toordinal()

    assert ad <= bd, "Dagsetning of langt í fortíðina" # TODO: Do something sane here
    assert ad + 365 >= bd, "Dagsetning of langt í framtíðina" # TODO: Do something sane here

    if ad == bd:
        res = 'í dag'
    elif ad + 1 == bd:
        res = 'á morgun'
    elif bd - ad < 7:
        res = 'á ' + day[dt.weekday()]
    else:
        res = 'þann ' + dt.day + '. ' + month[dt.month - 1]
    res += ' kl. ' + dt.strftime('%H:%M')
    return res

def duration_to_string(minutes):
    hours = minutes // 60
    minutes %= 60
    days = hours // 24
    hours %= 24
    if days > 0:
        return '%d:%02d:%02d' % (days, hours, minutes)
    else:
        return '%d:%02d' % (hours, minutes)

async def event_calendar(bot, config):
    await bot.wait_until_ready()

    if not os.path.isdir(config['data_dir']):
        os.makedirs(config['data_dir'])

    data_path = os.path.join(config['data_dir'], 'events.json')
    data = {}
    if os.path.isfile(data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)

    dtform = '%Y-%m-%dT%H:%M:%S'

    while not bot.is_closed:
        try:
            for cal in config['calendars']:
                channels = sorted(cal.get('channels', config.get('default_channels', [])))
                reminders = sorted(cal.get('reminders', config.get('default_reminders', [])))

                key = hashlib.md5()
                key.update(str(cal['id']).encode('utf-8'))
                key.update(repr(channels).encode('utf-8'))
                key.update(repr(reminders).encode('utf-8'))
                key = key.hexdigest()

                last = data.get(key, [0] * len(reminders))
                lastid = 0
                for i, r in enumerate(reminders): # Note: reminders must be sorted
                    lastid = max(lastid, last[i])

                    t1 = datetime.datetime.now()
                    t2 = datetime.datetime.now() + datetime.timedelta(seconds=r)
                    try:
                        res = await download(bot.loop, 'http://clist.by/api/v1/contest/'
                                                        '?username=%(username)s'
                                                        '&api_key=%(api_key)s'
                                                        '&resource__id=%(resource_id)d'
                                                        '&start__gt=%(start_gt)s'
                                                        '&start__lt=%(start_lt)s'
                                                        '&id__gt=%(id_gt)d' % {
                                                            'username': config['username'],
                                                            'api_key': config['api_key'],
                                                            'resource_id': cal['id'],
                                                            'start_gt': t1.strftime(dtform),
                                                            'start_lt': t2.strftime(dtform),
                                                            'id_gt': lastid,
                                                        })
                    except:
                        import traceback
                        sys.stderr.write('%s\n' % traceback.format_exc())
                        continue
                    for ev in json.loads(res.decode('utf-8'))['objects']:
                        lastid = max(lastid, ev['id'])

                        if ev['duration'] > 0:
                            desc = 'Byrjar %s' % describe_datetime(datetime.datetime.strptime(ev['start'], dtform))
                            desc += '\nLengd: %s' % duration_to_string(ev['duration'] // 60)
                        else:
                            desc = 'Birt %s' % describe_datetime(datetime.datetime.strptime(ev['start'], dtform))

                        emb = discord.Embed(
                            url         = ev['href'],
                            title       = ev['event'],
                            description = desc,
                            color       = discord.Colour.purple())
                        for channel in get_channels(bot, channels):
                            await bot.send_message(channel, embed=emb)

                    last[i] = lastid
                data[key] = last

            with open(data_path, 'w') as f:
                json.dump(data, f)
        except:
            import traceback
            sys.stderr.write('%s\n' % traceback.format_exc())

        await asyncio.sleep(config['interval'])

def setup(bot, config):
    bot.loop.create_task(event_calendar(bot, config))

