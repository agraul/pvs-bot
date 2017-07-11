import datetime
import logging

import discord

from credentials import token
import RoleManagement
import AdminTools

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
    bot_log = client.get_channel('302353252698161153')
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    if message.content[0] == '!':
        await AdminTools.run_op(client, message, bot_log, utc)
client.run(token())
