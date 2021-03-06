import requests
import warnings

# self-defined helper functions
from lib.net.ip import is_valid
from lib.util.exception import MetaException

# Enum for assertion handling choices
from enum import Enum
class AssertType(Enum):
    soft = 0
    hard = 1

class Gateway():
    
    class GatewayError(MetaException):
        pass

    def __init__(self, address : str, username : str, password : str):
        self.__init_var__(address, username, password)
        
    def __init_var__(self, address : str, username : str, password : str):
        self.address  = address
        self.username = username
        self.password = password
        self.session  = requests.Session()
        self.logged_in = False

    def __login(self):
        url = f'http://{self.address}/cgi-bin/luci/'
        data = dict()
        data['username'] = self.username
        data['psd']      = self.password
        response = self.session.post(url=url, data=data)
        if (not response.ok):
            raise response.raise_for_status()
        self.logged_in = True

    def __logout(self):
        self.__assert_logged_in(AssertType.hard)
        url = f'http://{self.address}/cgi-bin/luci/admin/logout'
        response = self.session.post(url=url)
        self.__assert_valid_resp(response, AssertType.hard)
        self.logged_in = False
        
    def __is_logged_in(self) -> bool:
        return self.logged_in
    
    def __assert_logged_in(self, assert_type : AssertType):
        if (not self.__is_logged_in()):
            msg = 'Not logged in.'
            if (assert_type == AssertType.hard):
                raise Gateway.GatewayError(msg)
            else:
                self.__login()

    def __assert_valid_ip(self, ip : str, assert_type : AssertType):
        if (not is_valid(ip)):
            msg = 'The IP address is not valid.'
            if (assert_type == AssertType.hard):
                raise Gateway.GatewayError(msg)
            else:
                warnings.warn(msg)
    
    def __assert_valid_resp(self, response, assert_type : AssertType):
        if (not response.ok):
            msg = 'The gateway sent us a bad response.'
            if (assert_type == AssertType.hard):
                raise Gateway.GatewayError(msg)
            else:
                warnings.warn(msg)
            
    def get_wan_ip(self) -> str:
        self.__assert_logged_in(AssertType.soft)
        url = f'http://{self.address}/cgi-bin/luci/admin/settings/gwinfo'
        data = dict()
        data['get'] = 'part'
        response = self.session.post(url=url, data=data)
        self.__assert_valid_resp(response, AssertType.hard)
        ip = response.json()['WANIP']
        self.__assert_valid_ip(ip ,AssertType.hard)
        self.__logout()
        return ip

