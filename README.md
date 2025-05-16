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

Avaliable Functions:
----------------------
### xbox.connect
- establishes a connection to the xbox
- no arguments
 
xbox.xNotify
- sends a notification to the xbox
- 2 arguments (message, logo)

- message: string
- logo: number between 0 and 76

xbox.GetCpuKey
- retrives the cpu key
- no arguments

xbox.sendTextCommand
- sends a packet to the xbox
- 2 arguments (command(required), recv_ammount(optional))
- command: string
- recv_ammount number (this dictates how many packets to recive in response to the packet from {command})
  if your unsure enable debug then set it to 100 since theres a 5 second timeout anyway debug will show you all the packets that it actually recives

xbox.setMemory
- sets a memory address
- 2 arguments (address data)
- both args are strings

get_xbdm_name
- retrives xbdm name
- no arguments

--------------------------
## Debug Mode
debug mode allows you to see plain recieved packets its usefull if your working with raw packets
