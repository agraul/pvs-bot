import discord
import asyncio

def not_instructions(message):
    return message.id != '292124920417091584'

async def purge_channel(client, message, bot_log):
    role_channel = discord.utils.get(message.server.channels,
                                     name='role-assignment')

    # try parse number from input
    try:
        num_in = int(message.content[6:].strip())
    except ValueError:
        num_in = 0

    # if input is 0 or invalid, purge 1 message
    if num_in != 0:
        to_purge = num_in
    else:
        to_purge = 1

    confirmed = ['y', 'yes']
    chan = message.channel
    # ask for confirmation
    m = await client.send_message(
        chan, "Do you really want to purge {} messages? (yes/no)"
            .format(num_in))
    check = await client.wait_for_message(timeout=10, author=message.author)

    if check.content.lower() in confirmed:
        if chan == role_channel:
            await client.purge_from(
                chan, check=not_instructions, limit=to_purge)
        else:
            await client.purge_from(chan, limit=to_purge)

    await asyncio.sleep(5)
    await remove_command_response(client, message, m, check)

async def remove_command_response(client, *messages):
    passed_messages = []
    for message in messages:
        passed_messages.append(message.id)

    def check_correct_id(message):
        return message.id in passed_messages

    await client.purge_from(messages[0].channel,
                            check=check_correct_id)