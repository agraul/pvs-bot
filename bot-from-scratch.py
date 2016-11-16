#!/usr/bin/python3
import discord
import asyncio
import requests
import datetime
import urllib.parse
import urllib.request
import id

client = discord.Client()

assignable_roles = ['NA', 'EUW', 'EUNE', 'OCE', 'BR', 'LAN', 'LAS', 'CHINA',
                    'KR', 'Top', 'Mid', 'Junle', 'ADC', 'Support']  # whitelist of roles for self management
privileged_roles = ['admin', 'moderator']
# function for generic role self-add
async def role_add(message):
    author = message.author
    user_input = message.content[2:]
    role = discord.utils.get(message.server.roles, name=user_input)

    if str(role) != "None":
        await client.add_roles(author, role)
        await client.send_message(message.channel, "You have been added to {}"
                                  .format(role))
    else:
        await client.send_message(message.channel, "Please enter a valid role.")

# function for generic role self-removal
async def role_strip(message):
    author = message.author
    user_input = message.content[2:]
    role = discord.utils.get(message.server.roles, name=user_input)
    roleLower = discord.utils.get(message.server.roles, name=user_input.lower())
    roleUpper = discord.utils.get(message.server.roles, name=user_input.upper())
    roleTitle = discord.utils.get(message.server.roles, name=user_input.title())

    if str(role) != "None":
        await client.remove_roles(author, role)
        await client.send_message(message.channel, "You have been removed from"
                                  "{}".format(role))
    elif str(roleLower) != "None":
        await client.remove_roles(author, roleLower)
        await client.send_message(message.channel, "You have been removed from"
                                  "{}".format(roleLower))
    elif str(roleUpper) != "None":
        await client.remove_roles(author, roleUpper)
        await client.send_message(message.channel, "You have been removed from"
                                  "{}".format(roleUpper))
    elif str(roleTitle) != "None":
        await client.remove_roles(author, roleTitle)
        await client.send_message(message.channel, "You have been removed from"
                                  "{}".format(roleTitle))
    else:
        await client.send_message(message.channel, "Please enter a valid role.")


async def savelogs(message):
    logs = []
    command, channel, numberString = message.content.split(' ')
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    s = ""
    channel = channel.lower()
    try:
        number = int(numberString)
        async for log in client.logs_from(chatlog, limit=number):
            if ("**" + channel + "**") in log.content:
                logs.append(log)
        for l in reversed(logs):
            s += l.content + "\n"
        return channel, s
    except:
        return channel, s

async def savelogs2(message):
    logs = []
    command, channel, numberString = message.content.split(' ')
    chatlog = discord.utils.get(message.server.channels, name='chatlog')
    s = ""
    channel = channel.lower()
    try:
        number = int(numberString)
        async for log in client.logs_from(chatlog, limit=number):
            if ("**" + channel + "**") in log.content:
                logs.append(log)
        return channel, reversed(logs)
    except:
        return channel, logs


async def pastbin(title, content):
    pastebin_vars = dict(
        api_option='paste'
        api_dev_key='2e15e96203dacd86c46417862c41f10f'
        api_paste_name=title
        api_paste_code=content
    )
    return urllib.request.urlopen('http://pastebin.com/api/api_post.php',
                                  urllib.parse.urlencode(pastebin_vars).encode(
                                      'utf-8')).read()



@client.event
async def on_message(message):
    content = message.content
    if content.startswith('+!'):
        if content[2:] == 'Coach':
            for r in message.author.roles:
                if r.name == 'Diamond +' or if r.name == 'Platinum':
                    high_elo = True
                else:
                    await client.send_message(message.channel, "You don't meed "
                                              "our elo requirement to self "
                                              "assign the coach role. Please "
                                              "talk to an admin.")
                if high_elo:
                    for r in message.author.roles:
                        if r.name == 'Verified':
                            await role_add(message)
                        else:
                            await client.send_message(message.channel,
                                                      "Please verify your rank "
                                                      "first.")
        elif content[2:] in assignable_roles:
            await role_add(message)
        else:
            await client.send_message(message.channel, "Your selected role "
                                      "can't be self-assigned by the bot. "
                                      "Please talk to an admin.")
    elif content.startswith('-!'):
        await role_strip(message)

    elif content.startswith('!savelogs'):
        for r in message.author.roles:
            if r.name in privileged_roles:
                channel, logs = await savelogs(message)
                if logs == '':
                    await client.send_message(message.channel, "An error "
                                              "occured. Please make sure you "
                                              "are using the correct syntax"
                                              "`!savelogs channel number`")
                else:
                    title = "Chatlog for {}".format(channel)
                    paste_link = await pastebin(title, logs)
                    paste_link.decode('utf-8')
                    await client.send_message(message.channel, "Here is the "
                                              "chatlog: {}".format(paste_link))
            else:
                await client.send_message(message.channel, "You don't have "
                                          "permission to request chatlogs.")
client.run(id.token2())
