#!/usr/bin/python3
# -*- coding: utf-8 -*-
import asyncio
import discord
client = discord.Client()

@asyncio.coroutine
# exeptions for abbreviations
def add_dia(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Diamond +')
    yield from client.send_message(message.channel, "You have been added to {}" .format(role))
    yield from client.add_roles(author, role)

def remove_dia(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Diamond +')
    yield from client.send_message(message.channel, "You have been removed from {}" .format(role))
    yield from client.remove_roles(author, role)

def add_plat(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Platinum')
    yield from client.send_message(message.channel, "You have been added to {}" .format(role))
    yield from client.add_roles(author, role)

def remove_plat(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Platinum')
    yield from client.send_message(message.channel, "You have been removed from {}" .format(role))
    yield from client.remove_roles(author, role)

def add_supp(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Support')
    yield from client.send_message(message.channel, "You have been added to {}" .format(role))
    yield from client.add_roles(author, role)

def remove_supp(message):
    author = message.author
    role = discord.utils.get(message.server.roles, name='Support')
    yield from client.send_message(message.channel, "You have been removed from {}" .format(role))
    yield from client.remove_roles(author, role)

# general role adding / removing
def add_role(message):
    author = message.author
    content = message.content.strip('+!')
    role = discord.utils.get(message.server.roles, name=content)
    roleLower = discord.utils.get(message.server.roles, name=content.lower())
    roleUpper = discord.utils.get(message.server.roles, name=content.upper())
    roleTitle = discord.utils.get(message.server.roles, name=content.title())

    if str(role) != "None":
        yield from client.send_message(message.channel, "You have been added to {}" .format(role))
        yield from client.add_roles(author, role)

    elif str(roleLower) != "None":
        yield from client.send_message(message.channel, "You have been added to {}" .format(roleLower))
        yield from client.add_roles(author, roleLower)

    elif str(roleUpper) != "None":
        yield from client.send_message(message.channel, "You have been added to {}" .format(roleUpper))
        yield from client.add_roles(author, roleUpper)

    elif str(roleTitle) != "None":
        yield from client.send_message(message.channel, "You have been added to {}" .format(roleTitle))
        yield from client.add_roles(author, roleTitle)

    else:
        yield from client.send_message(message.channel, "Please enter a valid role. See ?!roles for a list of available options.")

def remove_role(message):
    author = message.author
    content = message.content.strip('-!')
    role = discord.utils.get(message.server.roles, name=content)
    roleLower = discord.utils.get(message.server.roles, name=content.lower())
    roleUpper = discord.utils.get(message.server.roles, name=content.upper())
    roleTitle = discord.utils.get(message.server.roles, name=content.title())

    if str(role) != "None":
        yield from client.send_message(message.channel, "You have been removed from {}" .format(role))
        yield from client.remove_roles(author, role)

    elif str(roleLower) != "None":
        yield from client.send_message(message.channel, "You have been removed from {}" .format(roleLower))
        yield from client.remove_roles(author, roleLower)

    elif str(roleUpper) != "None":
        yield from client.send_message(message.channel, "You have been removed from {}" .format(roleUpper))
        yield from client.remove_roles(author, roleUpper)

    elif str(roleTitle) != "None":
        yield from client.send_message(message.channel, "You have been removed from {}" .format(roleTitle))
        yield from client.remove_roles(author, roleTitle)

    else:
        yield from client.send_message(message.channel, "Please enter a valid role. See ?!roles for a list of available options.")

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('?!roles'):
        yield from client.send_message(message.channel, "Here is a list of available roles: 'NA', 'EUW' , 'EUNE', 'OCE', 'LAS', 'LAN', 'BR', 'Diamond +', 'Platinum', 'Gold', 'Silver', 'Bronze', 'Top', 'Jungle', 'Mid', 'ADC', 'Support'.")
    elif message.content.startswith('?!help'):
        yield from client.send_message(message.channel, "You can add / remove roles by typig +!role or -!role and substituting 'role' with the desired role. See ?!roles for a list of available roles.")
# special role manipulation calls
    elif message.content.startswith('+!dia'):
        yield from add_dia(message)
    elif message.content.startswith('+!Diamond +'):
        yield from add_dia(message)
    elif message.content.startswith('+!plat'):
        yield from add_plat(message)
    elif message.content.startswith('+!supp'):
        yield from add_supp(message)

    elif message.content.startswith('-!dia'):
        yield from remove_dia(message)
    elif message.content.startswith('-!Diamond +'):
        yield from remove_dia(message)
    elif message.content.startswith('-!plat'):
        yield from remove_plat(message)
    elif message.content.startswith('-!supp'):
        yield from remove_supp(message)

# general role manipulation calls
    elif message.content.startswith('+!'):
        yield from add_role(message)
    elif message.content.startswith('-!'):
        yield from remove_role(message)

client.run('MTk5NDY2MzA2ODc2MDgwMTI4.Cm7m3A.esoojhdM2CvZ4Gb8AynGKSLnlJQ')
