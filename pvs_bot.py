#!/home/deploy/bots/pvs-bot/discord/bin/python
import asyncio
import datetime
import logging

import discord

import credentials
import launcher
import purger

# logging (copied from discord.py documentation)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)

# client instance
client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print(datetime.datetime.now())
    print('------')


@client.event
@asyncio.coroutine
def on_message(message):
    bot_log = discord.utils.get(message.server.channels,
                                name='bot-log')
    role_channel = discord.utils.get(message.server.channels,
                                     name='role-assignment')

    try:
        if message.content[0] == '!':
            yield from launcher.run_op(client, message, bot_log)
    except IndexError:
         pass

    if message.channel == role_channel:
        yield from purger.cleanup_role_channel(client, message)

client.run(credentials.token2())
