import pytest
from csirtg_network.interfaces import *


def test_default_address():
    i = default_address()
    print(i)

    assert i

    assert address_to_interface(i)


def test_default_interface():
    i = default_interface()
    assert i

    print(i)
    assert interface_to_address(i)


def test_resolve_endpoint():
    i = default_address()

    endpoint = resolve_endpoint(i, 5590)

    print(endpoint)

    assert endpoint == 'tcp://%s:%d' % (i, 5590)