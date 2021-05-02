from flask import Blueprint, jsonify, request
from ..search import *

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route("/lol_main", methods = ("POST",))
def view_main():
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "원하시는 버튼을 눌러주세요 .\n입력이 안될시 /s나 /시작을 입력해주세요.",
                    },
                }
            ],
            "quickReplies": [
                {
                    "label": "전적 검색",
                    "action": "block",
                    "blockId": "608eb5cdca885a01fa7eb28c"
                },
                {
                    "label": "랭킹",
                    "action": "block",
                    "blockId": "608ec64dc87b900e56c64c1e"
                },
                {
                    "label": "로테이션",
                    "action": "block",
                    "blockId": "6088370b51bb5918f5981217",
                },
            ]
        }
    }
    return jsonify(res)

@bp.route("/user_tier", methods = ("POST", ))
def view_tier():
    content = request.get_json()
    user_id = content['action']['params']['유저 아이디']
    summoner = search_summoner(user_id)
    if not summoner:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "아이디를 다시 확인해주세요.",
                        },
                    }
                ],
                "quickReplies": [
                    {
                        "label": "전적 검색",
                        "action": "block",
                        "blockId": "608eb5cdca885a01fa7eb28c"
                    },
                ]
            }
        }
        return jsonify(res)

    user_tier = search_summoner_info(summoner['id'])

    if user_tier['RANKED_FLEX_SR'] and user_tier['RANKED_SOLO_5x5']:
        answer = '■ 솔로랭크 ■ \n티어 : {}\nwins : {}\nlosses : {}\n■ 자유랭크 ■\n티어 : {}\nwins : {}\nlosses : {}'\
        .format(user_tier['RANKED_SOLO_5x5']['tier'], user_tier['RANKED_SOLO_5x5']['wins'], user_tier['RANKED_SOLO_5x5']['losses'],\
            user_tier['RANKED_FLEX_SR']['tier'], user_tier['RANKED_FLEX_SR']['wins'], user_tier['RANKED_FLEX_SR']['losses'])
    elif user_tier['RANKED_FLEX_SR']:
        answer = "■ 자유랭크 ■\n티어 : {}\nwins : {}\nlosses : {}".\
            format(user_tier['RANKED_FLEX_SR']['tier'], user_tier['RANKED_FLEX_SR']['wins'], user_tier['RANKED_FLEX_SR']['losses'])
    elif user_tier['RANKED_SOLO_5x5']:
        answer = '■ 솔로랭크 ■ \n티어 : {}\nwins : {}\nlosses : {}\n'.\
            format(user_tier['RANKED_SOLO_5x5']['tier'], user_tier['RANKED_SOLO_5x5']['wins'], user_tier['RANKED_SOLO_5x5']['losses'])
    else:
        answer = "기록이 없습니다.."

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "ID : {}\nLv : {}".format(summoner['name'], summoner['summonerLevel']),
                                "description": answer,
                                "thumbnail": {
                                    "imageUrl": search_summoner_icon(summoner['profileIconId']),
                                },
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(res)

@bp.route("/ranking", methods = ("POST", ))
def view_ranking():
    ranking = search_top_summoners()
    if ranking == False:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "서버가 불안정합니다. 잠시후 다시 시도해주세요.",
                        },
                    }
                ],
            }
        }
        return jsonify(res)

    if not ranking['master'] and not ranking['grandmaster'] and not ranking['challenger']:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "아직 마스터 티어에 아무도 도달하지 못했습니다.",
                        },
                    }
                ],
            }
        }
        return jsonify(res)

    ranking_list = []
    for key, value in ranking.items():
        for elem in value:
            user = '■ 솔로랭크 ■ \n티어 : {}\nwins : {}\nlosses : {}\n'.format(key + " " + str(elem[0]), elem[3], elem[4])
            info = \
                {
                    "title": elem[2],
                    "description": user,
                    "thumbnail": {
                        "imageUrl": "",
                    },
                }
            ranking_list.append(info)
            if len(ranking_list) >= 10:
                break
        if len(ranking_list) >= 10:
            break

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": ranking_list
                    }
                }
            ]
        }
    }
    return jsonify(res)




@bp.route("/rotation", methods=('POST',))
def view_rotation():
    rotations = search_rotation_champion()
    if not rotations:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "서버가 불안정합니다. 잠시후 다시 시도해주세요.",
                        },
                    }
                ],
            }
        }
        return jsonify(res)

    rotation_list = []
    for rotation in rotations:
        info = \
            {
                "title": "",
                "description": '',
                "thumbnail": {
                    "imageUrl": rotation[1],
                },
            }
        rotation_list.append(info)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": rotation_list
                    }
                }
            ]
        }
    }
    return jsonify(res)