import CloudFlare
from lib.net import gateway, cloudflare
from lib.util import yaml


def update_dns(config_path : str) -> bool:
    
    config = yaml.yaml_to_dict(yaml_path=config_path)
    
    wan_ip = gateway.Gateway(**config['gateway']).get_wan_ip()
    
    cloudflare_instance = CloudFlare.CloudFlare(
        token=config['cloudflare']['api_key'])

    for dns_record_name in config['dns_record_name']:
        is_updated = cloudflare.update_dns_records(
            cloudflare_instance, wan_ip, dns_record_name)
        
    return is_updated


if (__name__ == '__main__'):
    update_dns('conf/ddns.yaml')
