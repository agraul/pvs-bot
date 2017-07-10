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

# global variables
assignable_roles = ['Gold', 'EUW']


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
    if message.content.startswith('+!'):
        await RoleManagement.assign_role(client, message, assignable_roles,
                                         bot_log)
    elif message.content.startswith('-!'):
        await RoleManagement.remove_role(client, message, bot_log)
    elif message.content.startswith('!reduce'):
        await RoleManagement.reduce_roles(client, message, bot_log)

client.run(token())
