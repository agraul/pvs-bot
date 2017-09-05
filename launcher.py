import RoleManagement
import bot_logger
import purger


async def run_op(client, message, bot_log):
    levels = {
             'admin': ['admin'],
             'high': ['admin', 'moderator', 'panda bat'],
             'medium': ['trial moderator', 'moderator', 'admin', 'panda bat'],
             'low': ['@everyone']
             }

    ops = {'+': [RoleManagement.assign_role, 'low'],
           '-': [RoleManagement.remove_role, 'low'],
           'reduce': [RoleManagement.reduce_roles, 'high'],
           'timein': [RoleManagement.timein_user, 'medium'],
           'timeout': [RoleManagement.timeout_user, 'medium'],
           'verify': [RoleManagement.verify_rank, 'low'],
           'purge': [purger.purge_channel, 'high'],
           'count': [RoleManagement.count_users, 'medium'],
          }
    # unwrap message into operation and arguments
    operation = message.content[1:]
    try:
        operation, _ = operation.split(maxsplit=1)
    except ValueError:
        if operation == 'purge':
            pass
        else:
            return None

    # check if operation exists
    if operation in ops.keys():
        op = ops[operation]
    else:
        return None

    success = False
    required_roles = levels[op[1]]

    for r in message.author.roles:
        if r.name.lower() in required_roles:
            await op[0](client, message, bot_log)
            success = True
            break
    if success is not True:
        client.send_message(message.channel,
                            "Failed running `{}`".format(operation))
