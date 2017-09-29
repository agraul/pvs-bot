#!/home/deploy/bots/pvs-bot/discord/bin/python
import asyncio
import discord
import datetime
import credentials

def log_message(client, message, chatlog, utc, forbidden):
    if message.channel not in forbidden:
        yield from client.send_message(
            chatlog, "**{}UTC: {}:{}** `MESSAGE` - {}".format(
                utc, message.channel, message.author, message.clean_content))


def log_message_edit(client, old, new, chatlog, utc, forbidden):
    if old.channel not in forbidden:
        yield from client.send_message(
            chatlog, "**{}UTC: {}:{}** `EDIT` - {} `TO` {}".format(
               utc, old.channel, old.author, old.clean_content,
                new.clean_content))


def log_message_delete(client, message, chatlog, utc, forbidden):
    if message.channel not in forbidden:
        yield from client.send_message(
            chatlog, "**{}UTC: {}:{}** `DELETED` - {}".format(
                utc, message.channel, message.author, message.clean_content))

# client instance
client = discord.Client()


@asyncio.coroutine
@client.event
def on_ready():
    print('Logged in as ')
    print(client.user.name)
    print(client.user.id)
    print(datetime.datetime.now())
    print('------')


@asyncio.coroutine
@client.event
def on_message(message):
    bot_log = discord.utils.get(message.server.channels,
                                name='bot-log')
    chatlog = discord.utils.get(message.server.channels,
                                name='chatlog')
    admin_chat = discord.utils.get(message.server.channels,
                                name='admin')
    forbidden = [admin_chat, bot_log, chatlog]
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    yield from log_message(client, message, chatlog, utc, forbidden)


@asyncio.coroutine
@client.event
def on_message_edit(before, after):
    bot_log = discord.utils.get(before.server.channels,
                                name='bot-log')
    chatlog = discord.utils.get(before.server.channels,
                                name='chatlog')
    admin_chat = discord.utils.get(before.server.channels,
                                   name='admin')
    forbidden = [admin_chat, bot_log, chatlog]
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    yield from log_message_edit(client, before, after, chatlog, utc, forbidden)

@asyncio.coroutine
@client.event
def on_message_delete(message):
    bot_log = discord.utils.get(message.server.channels,
                                name='bot-log')
    chatlog = discord.utils.get(message.server.channels,
                                name='chatlog')
    admin_chat = discord.utils.get(message.server.channels,
                                   name='admin')
    forbidden = [admin_chat, bot_log, chatlog]
    utc = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    yield from log_message_delete(client, message, chatlog, utc, forbidden)

client.run(credentials.token4())



