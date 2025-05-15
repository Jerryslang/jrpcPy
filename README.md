# JrpcPy
a python libary for interacting with the xbox 360 jrpc2 and xbdm libary over lan

Example Usage:
```
from jrpcpy import *

console_ip = '192.168.0.***' # change to your consoles local ip

xbox = xboxConsole(console_ip, debug=False)
xbox.connect()

xbox.xNotify(xbox.GetCpuKey(), 1)
```
