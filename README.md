# JrpcPy
a python libary for interacting with the xbox 360 jrpc2 and xbdm libary over lan

Example Usage:
```
from jrpcpy import *

xbox = xboxConsole("192.168.0.58", debug=False)
xbox.connect()

xbox.xNotify(xbox.GetCpuKey(), 1)
```
