from lib.net import twitter, stream
from lib.util import yaml
from lib.file import path


if (__name__ == '__main__'):
    minosiro_conf = yaml.yaml_to_dict(yaml_path='conf/minosiro.yaml')
    twi_conf = yaml.yaml_to_dict(yaml_path='conf/twitter.yaml')
    
    twi_instance = twitter.API_ver_1.get_api_instance(
        proxy=minosiro_conf['proxy']['https'], **twi_conf)
    
    liked_tweets = twi_instance.get_favorites(
        screen_name='zincentimeter', count=5)
    
    for tweet in liked_tweets:
                
        if (not hasattr(tweet, 'extended_entities')):
            continue
        
        if ('media' not in tweet.extended_entities):
            continue
        
        for media_file in tweet.extended_entities['media']:
            file_url = media_file['media_url_https']
            stream.download(file_url, 
                        path.get_type_path('raw_data',
                                           **minosiro_conf['directory']),
                        proxy_conf=minosiro_conf['proxy'])
