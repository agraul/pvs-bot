# Role Management functions
import discord
import asyncio
from riot_api import RankInfo
from credentials import riot_api_key
import bot_logger
import purger

# GLOBAL VARIABLES
timeout_list = {}
tier_roles = ['verified', 'diamond +', 'platinum', 'gold', 'silver', 'bronze']


async def check_role_in_server(message, role):
    """Search for role in server and return role object"""

    # build list of roles on the server to check against
    server_roles = []
    for s_role in message.server.roles:
        server_roles.append(s_role.name)

    #if role.lower() == "diamond" or role.lower() == "diamond+":
    #    role = "Diamond +"

    # check role (different capitalisation) against server roles
    if role.lower() in server_roles:
        discord_role = discord.utils.get(message.server.roles,
                                         name=role.lower())
    elif role.upper() in server_roles:
        discord_role = discord.utils.get(message.server.roles,
                                         name=role.upper())
    elif role.title() in server_roles:
        discord_role = discord.utils.get(message.server.roles,
                                         name=role.title())
    # set discord_role to None if role can't be found on server
    else:
        discord_role = None
    return discord_role

async def assign_role(client, message, bot_log):
    """
    Assign a role to a user.

    :param client: bot instance of discord.Client()
    :param message: Trigger message: '!+ role' or '!+ role1 role2'
    :param bot_log: channel bot is logging to
    """

    assignable_roles = ['Diamond +', 'Platinum', 'Gold', 'Silver', 'Bronze',
                        'NA', 'EUW', 'EUNE', 'KR', 'TR', 'GARENA', 'NPVS',
                        'NLFG', 'Coach', 'Top', 'Jungle', 'Mid', 'ADC',
                        'Support', 'OCE', 'other games']

    assignment_channel = discord.utils.get(message.server.channels,
                                           name='role-assignment')
    if message.channel != assignment_channel:
        m = await client.send_message(message.channel,
                                      'This can only be done in {}'.format(
                                          assignment_channel
                                      ))
        await asyncio.sleep(5)
        await purger.remove_command_response(client, message, m)
        return None

    # strip trigger and split content
    wanted_roles = message.content[2:].lstrip().split(',')
    user = message.author

    if len(wanted_roles) == 1 and wanted_roles[0] == '':
        pass
    else:
        dis_roles = []
        for w_role in wanted_roles:
            discord_role = await check_role_in_server(message, w_role.lstrip())
            if discord_role is not None:
                dis_roles.append(discord_role)

        if len(dis_roles) == 0:
            m = await client.send_message(
                message.channel, "You need to provide at least one valid role.")
            await asyncio.sleep(5)
            await purger.remove_command_response(client, message, m)
            return None

        # check if discovered roles is allowed to be assigned
        tier_role = False
        got_added = False
        for discord_role in dis_roles:
            # check if discovered role is a tier role
            if discord_role.name.lower() in tier_roles:
                tier_role = True
                break
        # if no tier roles involved
        if tier_role is False:
            for discord_role in dis_roles:
                if discord_role.name in assignable_roles:
                    await client.add_roles(user, *dis_roles)
                    got_added = True
                else:
                    m = await client.send_message(
                        "{} can't be added this way!".format(discord_role))
            if got_added is True:
                m = await client.send_message(
                    message.channel, "{} got added to `".format(user)
                                     + ("{} " * len(dis_roles)).format(
                                        *dis_roles)
                                     + "`")
        # if tier roles involved
        else:
            # check for previous rank roles and replace them
            new_roles = []
            for r in user.roles:
                if r.name.lower() not in tier_roles:
                    new_roles.append(r)
            for discord_role in dis_roles:
                if discord_role.name in assignable_roles:
                    new_roles.append(discord_role)
                else:
                    m = await client.send_message(
                        "`{}` can't be added this way!".format(discord_role))
                    await asyncio.sleep(5)
                    await purger.remove_command_response(client, message, m)

            await client.replace_roles(user, *new_roles)
            m = await client.send_message(
                    message.channel, "{} got added to `".format(user)
                    + ("{} " * len(dis_roles)).format(*dis_roles)
                    + "`")

        await asyncio.sleep(5)
        await purger.remove_command_response(client, message, m)


async def remove_role(client, message, bot_log):
    """
    Remove a role from user.

    :param client: bot instance of discord.Client()
    :param message: Trigger message: '!- role'
    """
    if message.channel != discord.utils.get(message.server.channels,
                                            name='role-assignment'):
        return None
    role = message.content[2:].strip()
    user = message.author
    # TODO: ask for confirmation for some roles

    discord_role = await check_role_in_server(message, role)

    if discord_role is not None:
        await client.remove_roles(user, discord_role)
        m = await client.send_message(message.channel,
                                      "{} got removed from {}".format(
                                      user, discord_role))
    else:
        m = await client.send_message(message.channel,
                                      "{} is not a valid role.".format(role))

    await asyncio.sleep(5)
    await purger.remove_command_response(client, message, m)


async def reduce_roles(client, message, bot_log):
    """
    Remove all (but explicitly stated) roles from another user.

    :param client: bot instance of discord.Client()
    :param message: Trigger message: '!reduce user role1 role2 [...]'
    :param bot_log: channel bot is logging to
    """

    message_contents = message.content[7:].lstrip().split(' ')
    user = discord.utils.get(message.server.members,
                             name=message_contents[0])
    if user is None:
        user = discord.utils.get(message.server.members,
                                 display_name=message_contents[0])
        if user is None:
            return await client.send_message(message.channel,
                                             "{} not found.".format(
                                                 message_contents[0]))
    user_roles = []
    for u_role in user.roles:
        user_roles.append(u_role)
    roles_to_remove= []
    roles_to_keep = []
    # check if enough arguments are passed in the message
    if len(message_contents) <= 1:
        # TODO: confirm reduce to @everyone
        roles_to_remove = user_roles
        roles_to_keep.append('@ everyone')
    else:
        # check for every role a user has if it is in list of roles to keep
        for user_role in user_roles:
            if str(user_role) in message_contents[1:]:
                roles_to_keep.append(str(user_role))
            else:
                roles_to_remove.append(user_role)
    await client.remove_roles(user, *roles_to_remove)



async def verify_rank(client, message, bot_log):

    rg = RankInfo(riot_api_key())
    message_contents = message.content[7:].lstrip().split(',')
    summoner = rg.get_summoner_by_name(message_contents[0],
                                       message_contents[1])
    summoner_id = summoner['id']
    summoner_rank = rg.get_rank(summoner_id, message_contents[1])
    summoner_first_rune_pg = rg.get_runes(
            summoner_id, message_contents[1])['pages'][0]['name']
    if summoner_first_rune_pg == 'Plats vs Silvers':
        user = message.author
        rank_role = await check_role_in_server(message, summoner_rank)
        verify_role = await check_role_in_server(message, 'verified')
        region_role = await check_role_in_server(message, message_contents[1])
        kept_roles = []
        for r in user.roles:
            if r.name.lower() not in tier_roles:
                kept_roles.append(r)

        kept_roles.append(verify_role)
        kept_roles.append(region_role)
        kept_roles.append(rank_role)
        await client.replace_roles(user, *kept_roles)
        await client.send_message(
            message.channel, "Success! You have been verified ({} on {})".\
            format(rank_role, region_role))


async def timeout_user(client, message, b_log):

    message_content = message.content[8:].lstrip()
    targets = []

    if len(message.mentions) > 0:
        for mention in message.mentions:
            targets.append(mention)
    #TODO use regex to parse message targets
    elif '#' in message_content:
        message_content_l = message_content.split('#')
        user = discord.utils.get(message.server.members,
                                 name=message_content_l[0],
                                 discriminator=message_content_l[1])
        if user is None:
            user = discord.utils.get(message.server.members,
                                 display_name=message_content_l[0],
                                 discriminator=message_content_l[1])
        targets.append(user)
    else:
        user = discord.utils.get(message.server.members,
                                 name=message_content)
        if user is None:
            user = discord.utils.get(message.server.members,
                                     display_name=message_content)

        targets.append(user)
    timeout_role = discord.utils.get(message.server.roles, name='Timeout')
    for t in targets:
        t_roles = []
        for role in t.roles:
            t_roles.append(role)
        timeout_list[t] = t_roles
        await client.replace_roles(t, timeout_role)
        await client.send_message(
            message.channel, "{} got timed out by {}".format(
                t, message.author))

        await bot_logger.send_timeout_embed(client, t, message.author, b_log)

async def timein_user(client, message, b_log):

    message_content = message.content[8:].lstrip()
    targets = []

    if len(message.mentions) > 0:
        for mention in message.mentions:
            targets.append(mention)
    #TODO use regex to parse message targets
    elif '#' in message_content:
        message_content_l = message_content.split('#')
        user = discord.utils.get(message.server.members,
                                 name=message_content_l[0],
                                 discriminator=message_content_l[1])
        if user is None:
            user = discord.utils.get(message.server.members,
                                 display_name=message_content_l[0],
                                 discriminator=message_content_l[1])
        targets.append(user)
    else:
        user = discord.utils.get(message.server.members,
                                 name=message_content)
        if user is None:
            user = discord.utils.get(message.server.members,
                                     display_name=message_content)
        targets.append(user)
    for t in targets:
        t_roles = timeout_list[t]
        await client.replace_roles(t, *t_roles)
        await client.send_message(
            message.channel, "{}'s timeout was ended by {}".format(
                t.name, message.author))

        await bot_logger.send_timein_embed(client, t, message.author, b_log)


async def count_users(client, message, *args):
    x = 0
    try:
        y = int(message.content[6:])
    except ValueError:
        y = 'all'

    if type(y) == int:
        for user in message.server.members:
            if len(user.roles) > y:
                x += 1
    else:
        for user in message.server.members:
            if len(user.roles) > 1:
                x += 1
    await client.send_message(message.channel, "There are {} users.".format(x))