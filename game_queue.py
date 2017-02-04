# queue game module for pvs bot
import discord
import asyncio

# TODO: reset registration after 30 minutes
# TODO: automatic response when enoungh players are found
"""
Create a dictionary with name:elo for participants, once there are
5 players for each elo (high/low) ping everyone in the dic and let them
know. Point out one guy (high) responsible to set the game up.
"""
na_pvs = {}
na_normal = {}
na_ranked = {}


async def queue_up(message):
    author = message.author
    queue, server = message.content.split(" ")
    async for role in author.roles:
        if discord.utils.get(author.roles, name=role) in ranks:
            elo = role
        if elo == 'Bronze' or elo == 'Silver' or elo == 'Gold':
            elo = 'low'
        else:
            elo = 'high'
    if server == " " or server == "na":
        if queue == 'pvs' or queue == 'PvS':
            na_pvs[author] = elo
        elif queue == 'ranked':
            na_ranked[author] = elo


async def queue_response(message):
    queue, server = message.content.split(" ")
    to_ping = []
    high_elo_count = 0
    low_elo_count = 0
    if queue == 'pvs' or queue == 'PvS':
        for key in na_pvs.keys:
            if na_pvs[key] == 'high':
                high_elo_count += 1
            else:
                low_elo_count += 1
        if high_elo_count >= 5 and low_elo_count >= 5:
            for key in na_pvs.keys:
               to_ping.append(key)
            client.send_message(message.channel, "players: @{} @{} @{} @{} @{} @{} @{} @{} @{} @{}" .format(*to_ping))
