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
    chatlog = client.get_channel('245725379250225152')
    admin_chat = client.get_channel('182519378682576896')
    forbidden = [admin_chat, bot_log]

    try:
        if message.content[0] == '!':
            await AdminTools.run_op(client, message, bot_log, utc)
    except IndexError:
         pass

    if message.channel == role_assignment:
        await asyncio.sleep(10)
        await AdminTools.clear_role_channel(client, role_assignment, two_weeks)

    await AdminTools.log_message(client, message, chatlog, utc)


@client.event
async def on_message_delete(message):
    chatlog = client.get_channel('245725379250225152')
    await AdminTools.log_message_delete(client, message,
                                        chatlog, utc, forbidden)


@client.event
async def on_message_edit(before, after):
    chatlog = client.get_channel('245725379250225152')
    await AdminTools.log_message_edit(client, before, after,
                                      chatlog, utc, forbidden)

client.run(token1())
