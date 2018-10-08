# csirtg-network-py
Misc Python Network Utils

Helpful Utils to get your local default interface and address.


```python
>>> from csirtg_network.interfaces import default_address, default_interface, interface_to_address

>>> default_address()
'192.168.1.91'

>>> default_interface()
'en0'

>>> interface_to_address(default_interface())
'192.168.1.91'
```

