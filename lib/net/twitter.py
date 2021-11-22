import tweepy

import lib.util.exception as exception
import lib.util.yaml as yaml

class TwitterError(exception.MetaException): 
    pass

class API_ver_1():

    def get_media_info_dict(tweet : tweepy.models.Status = None,
                        media_file : dict = None) -> dict:
        layout_doc = \
        '''
            # Parse Rule:
            # 1. 'key: list'  parse to next level
            # 2. 'str'        get value from file
            # 3. 'key: value' get value from file AND 
            #                 substitute it with the key in layout 
            tweet:
            - id_str: 'https://twitter.com/i/status/{tweet_url}'
            - text
            - user:
                - id_str: 'https://twitter.com/i/user/{user_url}'
                - name
                - screen_name
            media_file:
            - media_url
            - media_url_https
        '''
        media_info_dict = dict()
        media_info_layout = yaml.yaml_to_dict(yaml_string=layout_doc)
        return yaml.parse_info_dict(
            tweet=tweet.__getstate__().get('_json'), 
            media_file=media_file, 
            info_layout=media_info_layout)

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

