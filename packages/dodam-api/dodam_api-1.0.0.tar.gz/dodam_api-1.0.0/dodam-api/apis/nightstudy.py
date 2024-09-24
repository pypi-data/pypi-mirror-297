def getMy(client, utils) :
    return client.request(
        utils.BASE_URL + "/night-study/my",
        "GET",
        header = {
            "Authorization": client.accessToken
        }
    )