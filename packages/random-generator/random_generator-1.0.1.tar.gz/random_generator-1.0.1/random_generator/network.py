import random as random_libs


def ip(ip_pattern: str = '*.*.*.*'):
    segments = ip_pattern.split('.')
    data = [(random_libs.randint(0, 255) if segment == '*' else int(segment)) for segment in segments]
    return '.'.join(map(str, data))


def mac_address(pattern='*:*:*:*:*:*'):
    segments = pattern.split(':')
    final_mac = []
    for segment in segments:
        if segment == '*':
            final_mac.append(format(random_libs.randint(0, 255), '02x'))
        else:
            final_mac.append(segment)
    return ':'.join(final_mac)
