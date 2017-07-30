import discord

async def test_embed(client, message, *args):
    em = discord.Embed()
    em.set_author(message.author)
    em.set_footer(text="TESTING")
    em.add_field(name='First', value='testing...')

    client.send_message()