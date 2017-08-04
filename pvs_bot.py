#!/home/deploy/bots/pvs-bot/discord/bin/python
import datetime
import logging

import discord

import credentials
import launcher

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
async def on_ready():
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print(datetime.datetime.now())
    print('------')


@client.event
async def on_message(message):
    bot_log = discord.utils.get(message.server.channels,
                                name='bot-log')

    try:
        if message.content[0] == '!':
            await launcher.run_op(client, message, bot_log)
    except IndexError:
         pass

client.run(credentials.token1())
