import requests

URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'summoner_by_name': 'v{version}/summoner/by-name/{names}',
    'get_league': 'v{version}/league/by-summoner/{id}/entry',
    'get_runes': 'v{version}/summoner/{id}/runes'
}

API_VERSIONS = {
    'summoner_by_name':'1.4',
    'get_league':'2.5',
    'get_runes':'1.4'
}

class RankGetter(object):
    def __init__(self,api_key):
        self.api_key = api_key

    def _request(self, api_url, region, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            URL['base'].format(
                proxy=region,
                region=region,
                url=api_url
                ),
            params=args
            )
        return response.json()

    def _get_summoner_by_name(self,name,region):
        api_url = URL['summoner_by_name'].format(
            version=API_VERSIONS['summoner_by_name'],
            names=name
            )
        return self._request(api_url,region)

    def _get_rank(self,id,region):
        try:
            api_url = URL['get_league'].format(
                version=API_VERSIONS['get_league'],
                id=id
                )
            league = self._request(api_url,region)[str(id)][0]
            tier = league['tier']
            division = league['entries'][0]['division']
            return tier + " " + division
        except:
            return "Unranked"

    def _get_runes(self,id,region):
        api_url = URL['get_runes'].format(
            version=API_VERSIONS['get_runes'],
            id=id
            )
        return self._request(api_url,region)

    def _confirm_rank(self,name,region):
        self.name = name.replace(" ","").lower()
        r = self._get_summoner_by_name(self.name,region)[self.name]
        id = r['id']
        runes = self._get_runes(id,region)
        name = runes[str(id)]['pages'][0]['name']
        if name == "Plats vs Silvers":
            rank = self._get_rank(id,region)
            return rank
        else:
            return "Error. Your first rune page must be named 'Plats vs Silvers'. Instead it is '" + name + "'"

    def set_rank(self,name,region):
        try:
            return self._confirm_rank(name,region)
        except:
            return "An unexpected error has occured"