# Library for admin functions
import discord
import RoleManagement


# TODO: kick

# TODO: undo_rename

# TODO: ban

# TODO: announce

# TODO: log

# TODO: welcome_private

# TODO: welcome_public

# TODO: change_settings

# TODO: check_rights
async def run_op(client, message, bot_log, utc):
    levels = {'high': ['admin'],
              'medium': ['moderator', 'admin']
              'low': ['everyone']
             }

    ops = {'+': [RoleManagement.assign_role, 'low'],
           '-': [RoleManagement.remove_role, 'low'],
           'reduce': [RoleManagement.reduce_roles, 'high'],
           'timeout': [RoleManagement.timeout_user, 'medium'],
          }
    operation = message.content[1:]
    if ops.has_key(operation):
        op = ops[operation]
    else:
        await client.send_message(message.channel,
                                  "Operation `{}` not found".format(operation))
        return None

    SUCCESS = False
    for r in message.author.roles:
        if r in levels[op[1]]:
            op[0](client, message, bot_log, utcnow)
            SUCCESS = True
            break
    if SUCCESS is not True:
        client.send_message(message.channel,
                            "Failed running `{}`".format(operation)
    return None

