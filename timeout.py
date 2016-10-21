#!/usr/bin/python3
# put users in timeout
import discord
import asyncio
import id

old_roles = {}
client = discord.Client()

# TODO: test both functions


@asyncio.coroutine
def send_to_timeout(message):
    roles_to_keep = ['EUW', 'timeout']
    target = message.content[8:].strip()
    target_member = discord.utils.get(message.server.members, name=target)
    old_roles[target_member] = target_member.roles
    yield from client.replace_roles(target_member, *roles_to_keep)


def release_from_timeout(message):
    target = message.content[7:].strip()
    target_member = discord.utils.get(message.server.members, name=target)
    yield from client.replace_roles(target_member,
                                    *old_roles[target_member])


@asyncio.coroutine
@client.event
def on_message(message):
    if message.content.startswith('!timeout'):
        yield from send_to_timeout(message)
    elif message.content.startswith('!timein'):
        yield from release_from_timeout(message)

client.run(id.token2())
