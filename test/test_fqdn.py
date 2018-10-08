from csirtg_network.fqdn import *


def test_url_fqdn():
    assert url_resolve('https://example.com') == 'example.com'


def test_fqdn_resolve():
    assert fqdn_resolve('csirtgadgets.com')


def test_ns_resolve():
    assert ns_resolve('csirtgadgets.com')


def test_peers_resolve():
    i = fqdn_resolve('csirtgadgets.com')
    assert peers_resolve(i)
