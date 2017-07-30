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
    if old.channel not in forbidden:
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






