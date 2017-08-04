import discord
import datetime

utcnow = datetime.datetime.utcnow().strftime('%H:%M:%S %Y-%m-%d')

async def send_timeout_embed(client, user, moderator, log_chan):
    em = discord.Embed(title='Timeout')
    em.add_field(name="User", value=user)
    em.add_field(name="Moderator", value=moderator)
    em.set_footer(text="Time: {}".format(utcnow))
    await client.send_message(log_chan, embed=em)


async def send_timein_embed(client, user, moderator, log_chan):
    em = discord.Embed(title='Timeout ended')
    em.add_field(name="User", value=user)
    em.add_field(name="Moderator", value=moderator)
    em.set_footer(text="//{}".format(utcnow))
    await client.send_message(log_chan, embed=em)
