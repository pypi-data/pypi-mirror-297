def login(client, utils, username, password) :
    data = client.request(utils.BASE_URL + "/auth/login", "POST",
        body = {
            "id": username,
            "pw": password
        }
    )

    client.username = username
    client.password = password
    
    client.accessToken = utils.TOKEN_TYPE + data["accessToken"]
    client.refreshToken = utils.TOKEN_TYPE + data["refreshToken"]

def reissue(client, utils) :
    data = client.request(utils.BASE_URL + "/auth/reissue", "POST",
        body = {
            "refreshToken": client.refreshToken
        }
    )

    client.accessToken = utils.TOKEN_TYPE + data["accessToken"]