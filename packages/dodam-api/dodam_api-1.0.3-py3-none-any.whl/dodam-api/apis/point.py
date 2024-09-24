def getMyScoreByDormitory(client, utils) :
    return client.request(
        utils.BASE_URL + "/point/score/my",
        "GET",
        param = {
            "type": "DORMITORY"
        },
        header = {
            "Authorization": client.accessToken
        }    
    )

def getMyScoreBySchool(client, utils) :
    return client.request(
        utils.BASE_URL + "/point/score/my",
        "GET",
        param = {
            "type": "SCHOOL"
        },
        header = {
            "Authorization": client.accessToken
        }
    )