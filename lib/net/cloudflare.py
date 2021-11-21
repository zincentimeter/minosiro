import ipaddress
import CloudFlare


def get_zone_name(dns_record_name : str) -> str:
    return '.'.join(dns_record_name.split('.')[-2:])


def get_zone_id(cloudflare_instance : CloudFlare, 
                dns_record_name : str) -> str:
    zone_name = get_zone_name(dns_record_name)
    # grab the zone identifier
    try:
        params = {'name' : zone_name}
        zones = cloudflare_instance.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))
    return zones.pop()['id']


def get_record_type(ip : str) -> str:
    try:
        ip_type = type(ipaddress.ip_address(ip))
        if (ip_type is ipaddress.IPv4Address):
            return 'A'
        elif (ip_type is ipaddress.IPv6Address):
            return 'AAAA'
        else:
            return 'Invalid'
    except ValueError:
        return 'Invalid'


def get_dns_records(cloudflare_instance : CloudFlare,
                    zone_id : str,
                    dns_record_name : str,
                    pending_record_type : str) -> list:
    try:
        params = {
            'name':dns_record_name,
            'match':'all',
            'type':pending_record_type}
        dns_records = cloudflare_instance.zones.dns_records.get(
            zone_id, params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records %s - %d %s - api call failed' % 
                (dns_record_name, e, e))
    return dns_records


def update_dns_records(cloudflare_instance : CloudFlare,
                        new_ip : str,
                        dns_record_name : str) -> bool:
    zone_id = get_zone_id(cloudflare_instance, dns_record_name)
    pending_record_type = get_record_type(new_ip)
    dns_records = get_dns_records(cloudflare_instance,
                                                zone_id,
                                                dns_record_name,
                                                pending_record_type)
    is_updated = False
    
    # update the record - unless it's already correct
    for dns_record in dns_records:
        old_ip = dns_record['content']
        old_record_type = dns_record['type']

        if (new_ip == old_ip):
            print('UNCHANGED: %s %s' % (dns_record_name, new_ip))
            updated = True
            continue
        
        time_to_live = dns_record['ttl']
        proxied_state = dns_record['proxied']
        dns_record_id = dns_record['id']
        dns_record = {
            'name':dns_record_name,
            'type':pending_record_type,
            'content':new_ip,
            'ttl':time_to_live,
            'proxied':proxied_state
        }
        
        try:
            response = cloudflare_instance.zones.dns_records.put(
                zone_id, dns_record_id, data=dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.dns_records.put %s - %d %s - api call failed' %
                    (dns_record_name, e, e))
        print('UPDATED: %s %s -> %s' % (dns_record_name, old_ip, new_ip))
        is_updated = True
        
    # no exsiting dns record to update - so create dns record
    if (not is_updated):
        create_dns_records(cloudflare_instance, new_ip,
                                            dns_record_name)
        is_updated = True
    return is_updated


def create_dns_records(cloudflare_instance : CloudFlare,
                        new_ip : str,
                        dns_record_name : str,
                        ttl : int = 120,
                        proxied : bool = False):
    zone_id = get_zone_id(cloudflare_instance, dns_record_name)
    pending_record_type = get_record_type(new_ip)
    dns_record = {
        'name':dns_record_name,
        'type':pending_record_type,
        'content':new_ip,
        'ttl':ttl,
        'proxied':proxied
    }
    try:
        dns_record = cloudflare_instance.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.dns_records.post %s - %d %s - api call failed' % (dns_record_name, e, e))
    print('CREATED: %s %s' % (dns_record_name, new_ip))

