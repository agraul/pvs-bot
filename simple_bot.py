#!/usr/bin/python3
# -*- coding: utf-8 -*-


import discord
client = discord.Client()


def assign_region(author, message):
    region = message.content.strip('!region')
    client.send_message(message.channel, "You chose: %s " % region)


@client.async_event
def on_message(message):
    author = message.author
    if message.content.startswith('!region'):
        assign_region(author, message)

client.run('MTk5NDY2MzA2ODc2MDgwMTI4.CmBsyg.pcJmTTObQn-cbDZcgGWRdXTjUq8')
