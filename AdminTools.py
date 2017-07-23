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
              'medium': ['moderator', 'admin'],
              'low': ['@everyone']
             }

    ops = {'+': [RoleManagement.assign_role, 'low'],
           '-': [RoleManagement.remove_role, 'low'],
           'reduce': [RoleManagement.reduce_roles, 'high'],
           'timeout': [RoleManagement.timeout_user, 'medium'],
           'verify': [RoleManagement.verify_rank, 'low'],
          }
    operation, _ = message.content[1:].split(maxsplit=1)
    if operation in ops.keys():
        op = ops[operation]
    else:
        await client.send_message(message.channel,
                                  "Operation `{}` not found".format(operation))
        return None

    SUCCESS = False
    required_roles = levels[op[1]]
    for r in message.author.roles:
        if r.name in required_roles:
            await op[0](client, message, bot_log, utc)
            SUCCESS = True
            break
    if SUCCESS is not True:
        client.send_message(message.channel,
                            "Failed running `{}`".format(operation))
