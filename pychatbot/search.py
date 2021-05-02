import requests

api_key = "api-key"

def search_rotation():
    url = "https://kr.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=" + api_key
    res = requests.get(url)
    if res.status_code != 200:
        return False
    return res.json()['freeChampionIds']

def search_version():
    res = requests.get("https://ddragon.leagueoflegends.com/realms/kr.json")
    if res.status_code != 200:
        return
    return res.json()['n']['champion']

def search_rotation_champion():
    version = search_version()
    url = "http://ddragon.leagueoflegends.com/cdn/{}/data/ko_KR/champion.json".format(version)
    res = requests.get(url)

    if res.status_code != 200:
        return False

    champion_rotation = search_rotation()
    if not champion_rotation:
        return False
    champion_list = []

    for key, val in res.json()['data'].items():
        if int(val["key"]) in champion_rotation:
            img_url = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(key)
            champion_list.append((val["name"], img_url))

    return champion_list

def search_summoner(user_id):
    url = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key=".format(user_id) + api_key
    res = requests.get(url)

    if res.status_code != 200:
        return False

    return res.json()

def search_summoner_info(account_id):
    url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key=".format(account_id) + api_key
    res = requests.get(url)

    if res.status_code != 200:
        return False
    summoner_info = {"RANKED_FLEX_SR":{}, "RANKED_SOLO_5x5":{}}
    for elem in res.json():
        if "queueType" in elem:
            summoner_info[elem["queueType"]]['name'] = elem['summonerName']
            summoner_info[elem["queueType"]]['tier'] = elem['tier'] + " " + elem['rank'] + " " + str(elem['leaguePoints'])
            summoner_info[elem["queueType"]]['wins'] = elem['wins']
            summoner_info[elem["queueType"]]['losses'] = elem['losses']
    return summoner_info

def search_summoner_icon(icon_num):
    version = search_version()
    url = "http://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png".format(version, icon_num)

    return url

def search_top_summoners():
    url_c = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    res_c = requests.get(url_c)

    if res_c.status_code != 200:
        return False

    ranking = {"challenger":[], "grandmaster":[], 'master':[]}

    challenger_ranking = []
    for user in res_c.json()['entries']:
        user_info = [user['leaguePoints'], user['rank'], user['summonerName'], user['wins'], user["losses"]]
        challenger_ranking.append(user_info)
    challenger_ranking.sort(key = lambda x:x[0], reverse=True)
    ranking['challenger'] = challenger_ranking


    url_g = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    res_g = requests.get(url_g)

    if res_g.status_code != 200:
        return False

    grandmaster_ranking = []
    for user in res_g.json()['entries']:
        user_info = [user['leaguePoints'], user['rank'], user['summonerName'], user['wins'], user["losses"]]
        grandmaster_ranking.append(user_info)
    grandmaster_ranking.sort(key = lambda x:x[0], reverse=True)
    ranking['grandmaster'] = grandmaster_ranking

    url_m = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
    res_m = requests.get(url_m)

    if res_m.status_code != 200:
        return False

    master_ranking = []
    for user in res_m.json()['entries']:
        user_info = [user['leaguePoints'], user['rank'], user['summonerName'], user['wins'], user["losses"]]
        master_ranking.append(user_info)
    master_ranking.sort(key=lambda x: x[0], reverse=True)
    ranking['master'] = master_ranking

    return ranking
