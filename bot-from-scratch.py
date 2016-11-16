#!/usr/bin/python3
import discord
import asyncio
import requests
import datetime
import urllib.parse
import urllib.request
import id

client = discord.Client()
# TODO: !verify

# lists of roles to check against
assignable_roles = ['NA', 'EUW', 'EUNE', 'OCE', 'BR', 'LAN', 'LAS', 'CHINA',
                    'KR', 'RU', 'JP', , 'TR', 'Top', 'Mid', 'Jungle', 'ADC',
                    'Support']
privileged_roles = ['admin', 'moderator']   # TODO: update to real names
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
chatlog = discord.utils.get(member.server.channels, name='chatlog')
timestamp = message.timestamp.strftime('%b %d: %H:%M')  # ('%a %b %d: %H:%M:%S')

async def on_member_join(member):
    await client.send_message(chatlog, "{} UTC: `JOINED` {}".format(timestamp,
                                                                    member))

async def on_member_remove:
    await client.send_message(chatlog, "{} UTC: `LEFT` {}".format(timestamp,
                                                                  member))
async def on_member_update(before, after):
    name_before = before.display_name
    name_after = after.display_name
    if name_after is not None and name_before is not None and \
            name_before != name_after:
        await client.send_message(chatlog, "{} UTC: `NICKNAME CHANGED` ({}) "
                                  "from {} to {}".format(timestamp, before,
                                                         name_before,
                                                         name_after))

async def on_message_delete(message):
    if str(message.channel) != 'chatlog':
        await client.send_message(chatlog, "{} UTC: `DELETED` **{}:** {}: {}"
                                  .format(timestamp, message.channel,
                                          message.author,
                                          message.content.replace('@', '@ ')))

async def on_message_edit(before, after):
    channel = before.channel
    author = before.author
    content_before = before.content.replace('@', '@ ')
    content_after = after.content.replace('@', '@ ')
    if str(message.channel) != 'chatlog':
        await client.send_message(chatlog, "{} UTC: `EDITED`\n\t `BEFORE`"
                                  "**{}:** {}: {}\n\t`AFTER` **{}:** {}: {}"
                                  .format(timestamp, channel, author,
                                          content_before, channel, author,
                                          content_after))

async def on_message(message):
    content = message.content
    channel = message.channel
    if str(channel) != 'chatlog':   # bot reposts everything not in chatlog
        await client.send_message(chatlog, "{} UTC: `SENT` **{}:** {}: {}"
                                  .format(timestamp, channel, message.author,
                                          content.replace('@', '@ ')))
    if content.startswith('+!'):
        if content[2:] == 'Coach':  # check if elo is met for self assignment
            async for r in message.author.roles:
                if r.name == 'Diamond +' or if r.name == 'Platinum':
                    high_elo = True
                else:
                    await client.send_message(message.channel, "You don't meet "
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
        elif content[2:] in assignable_roles:     # keep self assignment to
            await role_add(message)               # specific roles
        else:
            await client.send_message(message.channel, "Your selected role "
                                      "can't be self-assigned by the bot. "
                                      "Please talk to an admin.")
    elif content.startswith('-!'):
        await role_strip(message)

    elif content.startswith('!savelogs'):
        async for r in message.author.roles:
            if r.name in privileged_roles:  # only works for whitelisted roles
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
