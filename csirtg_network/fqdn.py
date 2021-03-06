import os, socket
import dns.resolver
from dns.resolver import NoAnswer, NXDOMAIN, NoNameservers, Timeout
from dns.name import EmptyLabel
import re

TIMEOUT = os.getenv('CSIRTG_NETWORK_RESOLVER_TIMEOUT', '15')
TIMEOUT = int(TIMEOUT)


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def url_resolve(url):
    u = urlparse(url)
    return u.hostname


def fqdn_resolve(host):
    try:
        host = socket.gethostbyname(host)
        return host
    except:
        return


def ns_resolve(data, t='A', timeout=TIMEOUT, nameserver=None):
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    resolver.search = []

    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answers = resolver.query(data, t)
        resp = []
        for rdata in answers:
            resp.append(rdata)
    except (NoAnswer, NXDOMAIN, EmptyLabel, NoNameservers, Timeout) as e:
        if str(e).startswith('The DNS operation timed out after'):
            return

        if not str(e).startswith('The DNS response does not contain an answer to the question'):
            if not str(e).startswith('None of DNS query names exist'):
                return

        return

    return resp


def peers_resolve(i):
    match = re.search('^(\S+)\/\d+$', i)
    if match:
        i = match.group(1)

    # cache it to the /24
    i = list(reversed(i.split('.')))
    i = '0.{}.{}.{}'.format(i[1], i[2], i[3])

    answers = ns_resolve('{}.{}'.format(i, 'peer.asn.cymru.com', timeout=15), t='TXT')
    if answers is None or len(answers) == 0:
        return

    peers = []

    # Separate fields and order by netmask length
    # 23028 | 216.90.108.0/24 | US | arin | 1998-09-25
    # 701 1239 3549 3561 7132 | 216.90.108.0/24 | US | arin | 1998-09-25
    for p in answers:
        bits = str(p).replace('"', '').strip().split(' | ')
        asn = bits[0]
        prefix = bits[1]
        cc = bits[2]
        rir = bits[3]
        asns = asn.split(' ')
        for a in asns:
            peers.append({
                'asn': a,
                'prefix': prefix,
                'cc': cc,
                'rir': rir
            })

    return peers
