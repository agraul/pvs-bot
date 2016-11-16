#!/usr/bin/python3
import discord
import asyncio
import requests
import datetime
import urllib.parse
import urllib.request
import id

client = discord.Client()

allowed_roles = []  # whitelist of roles for self management
coach_role = ['coach', 'Coach', 'COACH']    # check if role is coaching role
# function for generic role self-add
async def role_add(message):
    author = message.author
    user_input = message.content[2:]
    role = discord.utils.get(message.server.roles, name=user_input)
    roleLower = discord.utils.get(message.server.roles, name=user_input.lower())
    roleUpper = discord.utils.get(message.server.roles, name=user_input.upper())
    roleTitle = discord.utils.get(message.server.roles, name=user_input.title())

    if str(role) != "None":
        await client.add_roles(author, role)
        await client.send_message(message.channel, "You have been added to {}"
                                  .format(role))
    elif str(roleLower) != "None":
        await client.add_roles(author, roleLower)
        await client.send_message(message.channel, "You have been added to {}"
                                  .format(roleLower))
    elif str(roleUpper) != "None":
        await client.add_roles(author, roleUpper)
        await client.send_message(message.channel, "You have been added to {}"
                                  .format(roleUpper))
    elif str(roleTitle) != "None":
        await client.add_roles(author, roleTitle)
        await client.send_message(message.channel, "You have been added to {}"
                                  .format(roleTitle))
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


@client.event
async def on_message(message):
    content = message.content
    if content.startswith('+!'):
        if content[2:] in coach_role:
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
        elif content[2:] in allowed_roles:
            await role_add(message)
        else:
            await client.send_message(message.channel, "Your selected role "
                                      "can't be self-assigned by the bot. "
                                      "Please talk to an admin.")
    elif content.startswith('-!'):
        await role_strip(message)


client.run(id.token2())
