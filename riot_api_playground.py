import requests
from credentials import riot_api_key

# pulling all champions
developer_key = riot_api_key()

URL = {
    'base': 'https://{proxy}.api.riotgames.com/lol/{api_url}',
    'summoner_by_name': 'summoner/v3/summoners/by-name/{name}',
    'get_league': 'league/v3/leagues/by-summoner/{summoner_id}',
    'get_runes': 'platform/v3/runes/by-summoner/{summoner_id}'
}

PROXY = {
    'BR': 'BR1',
    'EUNE': 'EUN1',
    'EUW': 'EUW1',
    'JP': 'JP1',
    'KR': 'KR',
    'LAN': 'LA1',
    'LAS': 'LA2',
    'NA': 'NA1',
    'OCE': 'OC1',
    'TR': 'TR1',
    'RU': 'RU'
}


class RankInfo:

    def __init__(self, api_key):
        self.api_key = api_key

    def api_request(self, api_url, region_id, paras={}):
        # build args to pass from params
        args = {'api_key': self.api_key}
        for k,v in paras.items():
            if k not in args:
                args[k] = v

        # destination URL from base with correct proxy + specific api url
        dest = URL['base'].format(proxy=PROXY[region_id.upper()],
                                  api_url=api_url)

        # get response from requests
        response = requests.get(dest, params=args)
        return response.json()

    # get summoner via name
    def get_summoner_by_name(self, name, region):
        # specific api url return summoner json object via api_request
        api_url = URL['summoner_by_name'].format(name=name)
        return self.api_request(api_url, region)

    # get rank from summoner id
    def get_rank(self, id, region):
        # pass summoner id via api_url to api_request
        api_url = URL['get_league'].format(summoner_id=id)
        league = self.api_request(api_url, region.rstrip())
        if len(league) == 0:
            return "Unranked"
        else:
            tier = league[0]['tier']
            return tier.title()

    # get all runes from summoner id
    def get_runes(self, id, region):
        # pass summoner id via api_url to api_request
        api_url = URL['get_runes'].format(summoner_id=id)
        return self.api_request(api_url, region)


def main():
    rank_getter = RankInfo(developer_key)
    summ_name, summ_region = input("Please insert name,region: ").split(',')


    def verify(summ_name, summ_region):
        summoner = rank_getter.get_summoner_by_name(summ_name, summ_region)
        summ_id = summoner['id']
        summ_rank = rank_getter.get_rank(summ_id, summ_region)
        summ_first_rune_name = rank_getter.get_runes(summ_id, summ_region)['pages'][0]['name']


    verify(summ_name, summ_region)
if __name__ == '__main__':
    main()
