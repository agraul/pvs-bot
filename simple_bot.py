#!/usr/bin/python3

import discord
client = discord.Client()

def region_assign(author, message):


@client.event
def on_message(message):
    authoer = message.author
    if message.content.startswith('!region'):
        region_assign()

client.accept_invites('')
client.run()
