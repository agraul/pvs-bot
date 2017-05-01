# Library for admin functions
import discord
import datetime

utcnow = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# TODO: kick

# TODO: undo_rename

# TODO: ban

# TODO: announce

# TODO: log

# TODO: welcome_private

# TODO: welcome_public

# TODO: change_settings

# TODO: check_rights
async def check_permissions(client, level, user, bot_log):
    if level == 'high':
        required_roles = []
        required_roles.append(discord.utils.get(client.server.roles,
                                               name='admin'))
    elif level == 'medium':
        required_roles = []
        required_roles.append(discord.utils.get(client.server.roles,
                                               name='admin'))
        required_roles.append(discord.utils.get(client.server.roles,
                                               name='moderator'))
    elif level == 'low':
        required_roles = user.roles
