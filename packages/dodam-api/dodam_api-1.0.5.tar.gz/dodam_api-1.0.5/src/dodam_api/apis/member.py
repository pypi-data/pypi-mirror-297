def getMy(client, utils) :
    return client.request(
        utils.BASE_URL + "/member/my",
        "GET",
        header = {
            "Authorization": client.accessToken
        }
    )