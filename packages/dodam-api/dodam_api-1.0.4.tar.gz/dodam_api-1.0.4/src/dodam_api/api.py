from client import Client
from utils import Utils
from apis import (
    auth,
    member,
    nightstudy,
    bus,
    point,
    banner
)

class Api() :
    def __init__(self) :
        self.client = Client()
        self.utils = Utils()

    def login(self, id, pw):
        """
        Login to DodamDodam and Save Tokens to Instance
        
        :param id: DodamDodam ID
        :param pw: DodamDodam PW
        """
        return auth.login(self.client, self.utils, id, pw)

    def refresh_token(self) :
        """
        Reissue Access Token Using Refresh Token
        """
        return auth.reissue(self.client, self.utils)
    
    def get_my_info(self) :
        """
        Returns My Info
        """
        return member.getMy(self.client, self.utils)
    
    def get_my_nightstudy(self):
        """
        Returns List of My NightStudy
        """
        return nightstudy.getMy(self.client, self.utils)
    
    def get_valid_bus(self):
        """
        Returns List of Valid Bus
        """
        return bus.getValid(self.client, self.utils)
    
    def get_my_dormitory_point(self):
        """
        Returns My Dormitory Point
        """
        return point.getMyScoreByDormitory(self.client, self.utils)
    
    def get_my_school_point(self):
        """
        Returns My School Point
        """
        return point.getMyScoreBySchool(self.client, self.utils)

    def apply_bus(self, id) :
        """
        Apply to Certain Bus
        :param id: Bus ID
        """
        return bus.apply(self.client, self.utils, id)
    
    def get_all_banner(self) :
        """
        Returns All of Banner
        """
        return banner.getAllOrderByIdDesc(self.client, self.utils)
    
    def get_activate_banner(self) :
        """
        Returns Banner That Is Activated
        """
        return banner.getActivates(self.client, self.utils)
    