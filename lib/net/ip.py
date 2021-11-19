import ipaddress


def is_valid(ip : str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
    
def get_type(ip : str) -> str:
    try:
        ip_type = type(ipaddress.ip_address(ip))
        if (ip_type is ipaddress.IPv4Address):
            return 'IPv4'
        elif (ip_type is ipaddress.IPv6Address):
            return 'IPv6'
        else:
            return 'Invalid'
    except ValueError:
        return 'Invalid'