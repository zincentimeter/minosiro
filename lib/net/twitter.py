import tweepy

import lib.util.exception as exception
import lib.util.yaml as yaml

class TwitterError(exception.MetaException): 
    pass

class API_ver_1():

    def get_auth_handler(consumer_key : str,
                        consumer_secret : str,
                        access_token : str,
                        access_token_secret : str,
                        **kwargs) -> tweepy.OAuthHandler:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def get_api_instance(proxy : str,
                    **kwargs) -> tweepy.API:
        try:
            auth = API_ver_1.get_auth_handler(**kwargs['secret'])
        except TypeError:
            raise TwitterError('Wrong config level or key.')
        except KeyError:
            raise TwitterError('Section secret not found in the config.')
        return tweepy.API(auth=auth, proxy=proxy)

