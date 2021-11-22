from lib.net import twitter, stream
from lib.util import yaml
from lib.file import path, file

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
            file_instance = file.File.create_by_downloading(
                url=file_url,
                local_directory=path.get_type_path(
                    file_type='raw_data',
                    **minosiro_conf['directory']),
                proxy_conf=minosiro_conf['proxy'])
            twi_info_dict = twitter.API_ver_1.get_media_info_dict(
                tweet, media_file)
            file_instance.append_structure_info(
                field_name='source', structure_info_dict=twi_info_dict)