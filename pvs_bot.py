#!/home/deploy/bots/pvs-bot/discord/bin/python
import datetime
import logging
import asyncio

import discord

from credentials import token1
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
    role_assignment = client.get_channel('292124021628338197')
    # role_assignment = client.get_channel('248569093651693568') # test
    bot_log = client.get_channel('340225451257495553')
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    two_weeks = datetime.datetime.utcnow() - datetime.timedelta(days=14)

    try:
        if message.content[0] == '!':
            await AdminTools.run_op(client, message, bot_log, utc)
    except IndexError:
         pass

    if message.channel == role_assignment:
        await asyncio.sleep(10)
        await AdminTools.clear_role_channel(client, role_assignment, two_weeks)

client.run(token1())
