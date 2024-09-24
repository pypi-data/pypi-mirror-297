def getActivates(client, utils) :
    return client.request(
        utils.BASE_URL + "/banner/active",
        "GET",
        header = {
            "Authorization": client.accessToken
        }
    )

def getAllOrderByIdDesc(client, utils) :
    return client.request(
        utils.BASE_URL + "/banner",
        "GET",
        header = {
            "Authorization": client.accessToken
        }
    )