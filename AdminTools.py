# Library for admin functions
import discord
import RoleManagement


# TODO: kick

# TODO: undo_rename

# TODO: ban

# TODO: announce

# log
async def log_message(client, message, chatlog, utc, forbidden):
    if message.channel not in forbidden:
        await client.send_message(
            chatlog, "**{}UTC: {}:{}** `MESSAGE` - {}".format(
                utc, message.channel, message.author, message.content))


async def log_message_edit(client, old, new, chatlog, utc, forbidden):
    if message.channel not in forbidden:
        await client.send_message(
            chatlog, "**{}UTC: {}:{}** `EDIT` - {} `TO` {}".format(
               utc, old.channel, old.author, old.content, new.content))


async def log_message_delete(client, message, chatlog, utc, forbidden):
    if message.channel not in forbidden:
        await client.send_message(
            chatlog, "**{}UTC: {}:{}** `DELETED` - {}".format(
                utc, message.channel, message.author, message.content))

# TODO: welcome_private

# TODO: welcome_public

# TODO: change_settings
async def purge_channel(client, message, *args):
    number = int(message.content[6:].strip())
    chan = message.channel
    await client.send_message(
        chan, "Do you really want to purge {} messages? (y/N)".format(number))
    check = await client.wait_for_message(
        timeout=10, author=message.author, content="y")

    if check is not None:
        await client.purge_from(chan, limit=number)


async def clear_role_channel(client, role_channel, two_weeks):
    await client.purge_from(
            role_channel, check=not_first_message, after=two_weeks)


def not_first_message(message):
    return message.id != '292124920417091584'


async def run_op(client, message, bot_log, utc):
    levels = {'high': ['admin'],
              'medium': ['moderator', 'admin'],
              'low': ['@everyone']
             }

    ops = {'+': [RoleManagement.assign_role, 'low'],
           '-': [RoleManagement.remove_role, 'low'],
           'reduce': [RoleManagement.reduce_roles, 'high'],
           'timein': [RoleManagement.timein_user, 'medium'],
           'timeout': [RoleManagement.timeout_user, 'medium'],
           'verify': [RoleManagement.verify_rank, 'low'],
           'purge': [purge_channel, 'high'],
          }
    # unwrap message into operation and arguments
    try:
        operation, _ = message.content[1:].split(maxsplit=1)
    except ValueError:
        await client.send_message(message.channel, "I need more information")

    # check if operation exists
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
