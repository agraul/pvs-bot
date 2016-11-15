#!/usr/bin/python3
import asyncio
import discord
import requests
import id
import urllib.parse
import urllib.request

# TODO: update everything to python3.5
# TODO: general add_roles (only triggered for whitelisted roles)
# TODO: add logging / pastebin
# TODO: restrict bot to bot-channels

client = discord.Client()

URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'summoner_by_name': 'v{version}/summoner/by-name/{names}',
    'get_league': 'v{version}/league/by-summoner/{id}/entry',
    'get_runes': 'v{version}/summoner/{id}/runes'
}

API_VERSIONS = {
    'summoner_by_name': '1.4',
    'get_league': '2.5',
    'get_runes': '1.4'
}


class RankGetter(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def _request(self, api_url, region, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        destination = URL['base'].format(
            proxy=region,
            region=region,
            url=api_url
            )
        response = requests.get(
            destination,
            params=args
            )
        return response.json()

    # Based on Summoner name, get their info
    def _get_summoner_by_name(self, name, region):
        api_url = URL['summoner_by_name'].format(
            version=API_VERSIONS['summoner_by_name'],
            names=name
            )
        return self._request(api_url, region)

    # Based on Summoner name, get ID
    def _get_summoner_id(self, name, region):
        self.name = name.replace(" ", "").lower()
        r = self._get_summoner_by_name(self.name, region)[self.name]
        return r['id']

    # Based on Summoner ID, get their rank
    def _get_rank(self, id, region):
        try:
            api_url = URL['get_league'].format(
             version=API_VERSIONS['get_league'],
             id=id)
            league = self._request(api_url, region.rstrip())[str(id)][0]
            tier = league['tier']
            division = league['entries'][0]['division']
            return tier.title()  # + " " + division
        except:
            return "Unranked"

    # Get information based on rune page
    def _get_runes(self, id, region):
        api_url = URL['get_runes'].format(
            version=API_VERSIONS['get_runes'],
            id=id
            )
        return self._request(api_url, region)

    # Get first rune page name
    def _get_rune_name(self, id, region):
        runes = self._get_runes(id, region)
        return runes[str(id)]['pages'][0]['name']

    # Returns account info that was saved (author'sName,summoner'sName,region)
    def _get_linked_account(self, name, author, region):
        id = self._get_summoner_id(name, region)
        accountLink = [[i for i in line.split(',')] for line in
                       open('linkedAccounts.txt', 'r')]
        for x in accountLink:
            if x[1] == str(id):
                if x[0].lower() == author.lower():
                    if x[2].rstrip() == region.lower():
                        return x

    def verify_rank(self, name, region):
        id = self._get_summoner_id(name, region)
        if self._get_rune_name(id, region) == "Plats vs Silvers":
            return self._get_rank(id, region)
        else:
            return "Error"

ranks = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Masters",
         "Challenger"]
rg = RankGetter('070e0d5e-c950-47f5-8a6c-fb3a5861f70c')


@asyncio.coroutine
# manual role management for abbreviations
def verify(message):
    try:
        author = message.author
        content = message.content[8:].split(',')
        rank = rg.verify_rank(content[0], content[1].lower().strip(" "))
        rank2 = discord.utils.get(message.server.roles, name=rank)
        region = discord.utils.get(message.server.roles,
                                   name=content[1].upper().strip(" "))
        if rank == "Error":
            yield from client.send_message(message.channel, "To verify rank, "
                                           "please set the name of your first "
                                           "rune page to 'Plats vs Silvers'. "
                                           "Make sure you typed the name of "
                                           "your account correctly too.")
        elif rank == "Unranked":
            yield from client.send_message(message.channel, "You are currently "
                                           "not ranked in dynamic queue "
                                           "this season")
        else:
            roles = message.author.roles
            l = [discord.utils.get(message.server.roles, name='Verified'),
                 rank2, region]
            for r in roles:
                if r.name not in ranks:
                    l.append(discord.utils.get(message.server.roles,
                                               name=r.name))
            yield from client.replace_roles(message.author, *l)
            yield from client.send_message(message.channel,
                                           "You have been added to {}"
                                           .format(rank2))
    except:
        yield from client.send_message(message.channel,
                                       "Invalid format. Please type '!verify "
                                       "Summoner Name,Region ID'")


def add_role(message):
    author = messag.author
    if message.content[2:].lower().startswith('na'):
        role = discord.utils.get(message.server.roles, name='NA')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('eune'):
        role = discord.utils.get(message.server.roles, name='EUNE')
    elif message.content[2:].lower().startswith('oce'):
        role = discord.utils.get(message.server.roles, name='OCE')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('euw'):
        role = discord.utils.get(message.server.roles, name='EUW')
    elif message.content[2:].lower().startswith('support'):
        role = discord.utils.get(message.server.roles, name='Support')
    elif message.content[2:].lower().startswith('adc'):
        role = discord.utils.get(message.server.roles, name='ADC')
    elif message.content[2:].lower().startswith('mid'):
        role = discord.utils.get(message.server.roles, name='Mid')
    elif message.content[2:].lower().startswith('top'):
        role = discord.utils.get(message.server.roles, name='Top')
    elif message.content[2:].lower().startswith('jungle'):
        role = discord.utils.get(message.server.roles, name='Jungle')
    elif message.content[2:].lower().startswith('bronze'):
        role = discord.utils.get(message.server.roles, name='Bronze')
        roles = author.roles
        l = [role]
        vflag = True
    elif message.content[2:].lower().startswith('silver'):
        role = discord.utils.get(message.server.roles, name='Silver')
        roles = author.roles
        l = [role]
        vlfag = True
    elif message.content[2:].lower().startswith('gold'):
        role = discord.utils.get(message.server.roles, name='Gold')
        roles = author.roles
        l = [role]
        vlfag = True
    elif message.content[2:].lower().startswith('platinum'):
        role = discord.utils.get(message.server.roles, name='Platinum')
        roles = author.roles
        l = [role]
        vlfag = True
    elif message.content[2:].lower().startswith('diamond'):
        role = discord.utils.get(message.server.roles, name='Diamond')
        roles = author.roles
        l = [role]
        vlfag = True
    elif message.content[2:].lower().startswith('masters'):
        role = discord.utils.get(message.server.roles, name='Masters')
        roles = author.roles
        l = [role]
        vlfag = True
    elif message.content[2:].lower().startswith('challenger'):
        role = discord.utils.get(message.server.roles, name='Challenger')
        roles = author.roles
        l = [role]
        vlfag = True

    if vflag:
        for r in roles:
            if r.name != "Verified":
                l.append(discord.utils.get(message.server.roles, name=r.name))
        yield from client.replace_roles(author, *l)
    else:
        yield from client.add_roles(author, role)

    yield from client.send_message(message.channel,
                                   "You have been added to {}".format(role))


def del_role(message):
    author = message.author
    if message.content[2:].lower().startswith('support'):
        role = discord.utils.get(message.server.roles, name='Support')
    elif message.content[2:].lower().startswith('adc'):
        role = discord.utils.get(message.server.roles, name='ADC')
    elif message.content[2:].lower().startswith('mid'):
        role = discord.utils.get(message.server.roles, name='Mid')
    elif message.content[2:].lower().startswith('top'):
        role = discord.utils.get(message.server.roles, name='Top')
    elif message.content[2:].lower().startswith('jungle'):
        role = discord.utils.get(message.server.roles, name='Jungle')
    elif message.content[2:].lower().startswith('bronze'):
        role = discord.utils.get(message.server.roles, name='Bronze')
    elif message.content[2:].lower().startswith('silver'):
        role = discord.utils.get(message.server.roles, name='Silver')
    elif message.content[2:].lower().startswith('gold'):
        role = discord.utils.get(message.server.roles, name='Gold')
    elif message.content[2:].lower().startswith('platinum'):
        role = discord.utils.get(message.server.roles, name='Platinum')
    elif message.content[2:].lower().startswith('diamond'):
        role = discord.utils.get(message.server.roles, name='Diamond')
    elif message.content[2:].lower().startswith('masters'):
        role = discord.utils.get(message.server.roles, name='Masters')
    elif message.content[2:].lower().startswith('challenger'):
        role = discord.utils.get(message.server.roles, name='Challenger')
    elif message.content[2:].lower().startswith('coach'):
        role = discord.utils.get(message.server.roles, name='Coach')

    yield from client.send_message(message.channel,
                                   "You have been removed from {}".format(role))
    yield from client.remove_roles(author, role)


def add_coach(message):
    author = message.author
    required_roles = ['Diamond', 'Platinum', 'Masters', 'Challenger']
    role = discord.utils.get(message.server.roles, name='Coach')
    x = 0
    for r in author.roles:
        if r.name in required_roles:
                    x = 1
    if x == 1:
        for r in author.roles:
            if r.name == 'Verified':
                x = 2
    if x == 2:
        yield from client.send_message(message.channel,
                                       "You have been added to {}".format(role))
        yield from client.add_roles(author, role)
    elif x == 1:
        yield from client.send_message(message.channel,
                                       "You need to be verified!")
    else:
        yield from client.send_message(message.channel,
                                       "You need to be at least Platinum "
                                       "to become a coach.")


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('?!roles'):
        yield from client.send_message(message.channel,
                                       "Here is a list of available roles:\n"
                                       "Regions: NA, EUW, EUNE, BR, OCE, CHINA,"
                                       " LAN\nRanks: Bronze, Silver, Gold, "
                                       "Platinum, Diamond. (Masters and "
                                       "Challenger must be obtained through the"
                                       " verify method)\nRoles: ADC, Support,"
                                       " Mid, Top, Jungle\nType '?!verify' to "
                                       "learn ow to get the verified tag for "
                                       "your rank")
    elif message.content.startswith('?!help'):
        yield from client.send_message(message.channel, "You can add / remove "
                                       "roles by typig +!role or -!role and "
                                       "substituting 'role' with the desired "
                                       "role. See ?!roles for a list of "
                                       "available roles.")
    elif message.content.startswith('?!verify'):
        yield from client.send_message(message.channel, "To verify your "
                                       "account, follow these steps:\n1.) Set "
                                       "the name of your first rune page to "
                                       "'Plats vs Silvers'\n2.) Find your "
                                       "regionID by typing '?!regions'\n3.) "
                                       "Type '!verify SummonerName,RegionID' "
                                       "substituting in your name and region")
    elif message.content.startswith('?!regions'):
        yield from client.send_message(message.channel, "North America = na, "
                                       "EU West = euw, EU North East = eune "
                                       "Latin America North = lan, Latin "
                                       "America South = las, Oceania = oce, "
                                       "Japan = jp, Korea = kr, Brazil = br, "
                                       "Russia = ru, Turkey = tr")
    elif message.content.lower().startswith('+!coach'):
        yield from add_coach(message)
    elif message.content.lower().startswith('-!coach'):
        yield from del_coach(message)

# Roles
    elif message.content.lower().startswith('+!support'):
        yield from add_support(message)
    elif message.content.lower().startswith('+!adc'):
        yield from add_adc(message)
    elif message.content.lower().startswith('+!mid'):
        yield from add_mid(message)
    elif message.content.lower().startswith('+!top'):
        yield from add_top(message)
    elif message.content.lower().startswith('+!jungle'):
        yield from add_jungle(message)
    elif message.content.lower().startswith('-!support'):
        yield from del_support(message)
    elif message.content.lower().startswith('-!adc'):
        yield from del_adc(message)
    elif message.content.lower().startswith('-!mid'):
        yield from del_mid(message)
    elif message.content.lower().startswith('-!top'):
        yield from del_top(message)
    elif message.content.lower().startswith('-!jungle'):
        yield from del_jungle(message)

# Non-verified ranks
    elif message.content.lower().startswith('+!bronze'):
        yield from add_bronze(message)
    elif message.content.lower().startswith('-!bronze'):
        yield from del_bronze(message)
    elif message.content.lower().startswith('+!silver'):
        yield from add_silver(message)
    elif message.content.lower().startswith('-!silver'):
        yield from del_silver(message)
    elif message.content.lower().startswith('+!gold'):
        yield from add_gold(message)
    elif message.content.lower().startswith('-!gold'):
        yield from del_gold(message)
    elif message.content.lower().startswith('+!platinum'):
        yield from add_platinum(message)
    elif message.content.lower().startswith('-!platinum'):
        yield from del_platinum(message)
    elif message.content.lower().startswith('+!diamond'):
        yield from add_diamond(message)
    elif message.content.lower().startswith('-!diamond'):
        yield from del_diamond(message)
    elif message.content.lower().startswith('-!masters'):
        yield from del_masters(message)
    elif message.content.lower().startswith('-!challenger'):
        yield from del_challenger(message)

# Servers
    elif message.content.lower().startswith('+!euw'):
        yield from add_euw(message)
    elif message.content.lower().startswith('-!euw'):
        yield from del_euw(message)
    elif message.content.lower().startswith('+!na'):
        yield from add_na(message)
    elif message.content.lower().startswith('-!na'):
        yield from del_na(message)
    elif message.content.lower().startswith('+!oce'):
        yield from add_oce(message)
    elif message.content.lower().startswith('-!oce'):
        yield from del_oce(message)
    elif message.content.lower().startswith('+!eune'):
        yield from add_eune(message)
    elif message.content.lower().startswith('-!eune'):
        yield from del_eune(message)
    elif message.content.lower().startswith('+!lan'):
        yield from add_lan(message)
    elif message.content.lower().startswith('-!lan'):
        yield from del_lan(message)
    elif message.content.lower().startswith('+!br'):
        yield from add_brazil(message)
    elif message.content.lower().startswith('-!br'):
        yield from del_brazil(message)
    elif message.content.lower().startswith('+!china'):
        yield from add_china(message)
    elif message.content.lower().startswith('-!china'):
        yield from del_china(message)
# Update/link account
    # elif message.content.startswith('!update'):
        #  yield from update_account(message)
    # elif message.content.startswith('!link'):
        # yield from link_account(message)
    elif message.content.startswith('!verify'):
        yield from verify(message)

client.run(id.token1())
