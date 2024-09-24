def getValid(client, utils) :
    return client.request(
        utils.BASE_URL + "/bus",
        "GET",
        header = {
            "Authorization": client.accessToken
        }
    )

def apply(client, utils, id) :
    return client.request(
        utils.BASE_URL + f"/bus/apply/{id}",
        "POST",
        header = {
            "Authorization": client.accessToken
        }
    )