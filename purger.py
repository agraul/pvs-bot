def not_first_message(message):
    return message.id != '292124920417091584'

async def purge_channel(client, message, *args):
    to_purge = 3
    num_in = int(message.content[6:].strip())
    if num_in != 0:
        to_purge += num_in
    else:
        to_purge += 1
    chan = message.channel
    await client.send_message(
        chan, "Do you really want to purge {} messages? (y/N)".format(num_in))
    check = await client.wait_for_message(
        timeout=10, author=message.author, content="y")

    if check is not None:
        if chan == role_channel:
            await client.purge_from(
                chan, check=not_first_message, limit=to_purge)

async def clear_role_channel(client, role_channel, two_weeks):
    await client.purge_from(role_channel, limit=2,  after=two_weeks,
                            check=not_first_message)