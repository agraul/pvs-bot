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
        required_roles = ['admin']
    elif level == 'medium':
        required_roles = ['admin', 'moderator']

    if len(required_roles) > 0:
        for role in required_roles:
            d_role = discord.utils.get(client.server.roles, name=role)
            if d_role in user.roles:
                return True
        return False
    return True

