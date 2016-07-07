#!/usr/bin/python3
# -*- coding: utf-8 -*-


import discord
client = discord.Client()

# def assign_region (author, message):


@client.event
def on_message(message):
    author = message.author
    # if message.content.startswith('!region'):
    # assign_region ()
    if message.content.startswith('!tetst'):
        client.send_message(message.channel,
                            "%s, How are you doing ?" % author)

client.run('MTk5NDY2MzA2ODc2MDgwMTI4.CmBsyg.pcJmTTObQn-cbDZcgGWRdXTjUq8')
