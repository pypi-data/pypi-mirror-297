import requests
from utils import Utils
from apis import auth
from error import TokenExpiredException

class Client() :
    def __init__(self) :
        self.utils = Utils()
    
    def request(self, url, method, **kwargs) :
        while True:
            try :
                res = requests.request(
                    method,
                    url,
                    headers=kwargs.get("header", {}),
                    json=kwargs.get("body", {}),
                    params=kwargs.get("param", {}),
                )
                
                if (res.status_code == 401) :
                    raise TokenExpiredException
                
                return res.json()["data"]

            except (TokenExpiredException) :
                self.reissue()
                continue

            except (KeyError) :
                return res.json()
    
    def reissue(self) :
        try :
            res = auth.reissue(self, self.utils)
            
            if (res.status_code == 410)  :
                raise TokenExpiredException
            
        except (TokenExpiredException) :
            self.relogin()
    
    def relogin(self) :
        auth.login(self, self.utils, self.username, self.password)
        