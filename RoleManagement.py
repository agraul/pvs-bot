# Role Management functions
import discord
from riot_api_playground import RankInfo
from credentials import riot_api_key

async def check_role_in_server(message, role):
    """Search for role in server and return role object"""

    # build list of roles on the server to check against
    server_roles = []
    for s_role in message.server.roles:
        server_roles.append(s_role.name)

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

async def assign_role(client, message, bot_log, utcnow):
    """
    Assign a role to a user.

    :param client: bot instance of discord.Client()
    :param message: Trigger message: '+!role' or '+!role user'
    :param assignable_roles: list of allowed roles
    :param bot_log: channel bot is logging to
    """

    assignable_roles = ['Diamond +', 'Platinum', 'Gold', 'Silver', 'Bronze',
                        'NA', 'EUW', 'EUNE', 'KR', 'TR', 'GARENA', 'NPVS',
                        'NLFG']

    # strip trigger and split content
    message_contents = message.content[2:].lstrip().split(' ')

    # check if input is empty
    if len(message_contents) == 1 and message_contents[0] == '':
        pass
    else:
        # set role to first string
        role = message_contents[0]
        # set user to second string, defaulting to self if no second string
        try:
            user = discord.utils.get(message.server.members,
                                     name=message_contents[1])
            if user is None:
                user = discord.utils.get(message.server.members,
                                         display_name=message_contents[1])
        except IndexError:
            user = message.author
        print(user)

        discord_role = await check_role_in_server(message, role)

        # check if discovered role is allowed to be assigned
        try:
            if discord_role.name in assignable_roles:
                await client.send_message(message.channel, "{} got added to {}"
                                          .format(user, discord_role))
                await client.add_roles(user, discord_role)
                await client.send_message(bot_log, "{} got added to {}"
                                          .format(user, discord_role))
            else:
                await client.send_message(message.channel,
                                          "{} can't be added this way"
                                          .format(discord_role))
                await client.send_message(bot_log, "{}:{} tried to add {}"
                                          .format(utcnow, user, discord_role))
        # discord_role has no .name if None
        except AttributeError:
            await client.send_message(message.channel,
                                      "{} is not a valid role."
                                      .format(role))
            await client.send_message(bot_log, "{}: {} tried to add {}."
                                          .format(utcnow, user, role))
        # TODO: cleanup afterwards

async def remove_role(client, message, bot_log, utcnow):
    """
    Remove a role from user.

    :param client: bot instance of discord.Client()
    :param message: Trigger message: '-!role'
    :param bot_log: channel bot is logging to
    """
    role = message.content[2:].strip()
    user = message.author
    # TODO: ask for confirmation for some roles

    discord_role = await check_role_in_server(message, role)

    if discord_role is not None:
        await client.remove_roles(user, discord_role)
        await client.send_message(message.channel,
                                  "{} got removed from {}".format(
                                      user, discord_role))
        await client.send_message(bot_log, "`{}`: {} removed itself from {}."
                                  .format(utcnow, user, discord_role))
    else:
        await client.send_message(message.channel, "{} is not a valid role."
                                  .format(role))
        await client.send_message(bot_log, "`{}`: {} tried to remove {}."
                                  .format(utcnow, user, role))

        # TODO: cleanup afterwards

# TODO: strip roles (strip all roles except for those explicitly stated)
# TODO: restrict usage to admins
async def reduce_roles(client, message, bot_log, utcnow):
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
    await client.send_message(bot_log, "`{}`: {} Reduced {}'s roles to "
                              .format(utcnow, message.author, user)
                              + ("`{}` " * len(roles_to_keep))
                              .format(*roles_to_keep))


async def verify_rank(client, message ,bot_log, utcnow):

    rg = RankInfo(riot_api_key)
    message_contents = message.content[6:].lstrip().split(',')
    summoner = rg.get_summoner_by_name(message_contents[0],
                                       message_contents[1])
    summoner_id = summoner['id']
    summoner_rank = rg.get_rank(summoner_id, message_contents[1])
    summoner_first_rune_pg = rg.get_runes(
summoner_id, message_contents[1])['pages'][0]['name']
    if summoner_first_rune_pg == 'summonersplaza':
        user = message.author
        rank_role = await check_role_in_server(message, summoner_rank)
        verify_role = await check_role_in_server(message, 'verify')
        region_role = await check_role_in_server(message, message_contents[1])
        await client.add_roles(user, rank_role)
        await client.add_roles(user,verify_role)
        await client.add_roles(user, region_role)
        await client.send_message(
            message.channel, "Success! You have been verified ({} on {})".\
            format(rank_role, region_role))


async def timeout_user(client, message, timeout_list, bot_log, utcnow):

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

    timeout_role = discord.utils.get(message.server.roles, name='Timeout')
    for t in targets:
        t_roles = []
        for role in t.roles:
            t_roles.append(role)
        timeout_list[t] = t_roles
