from socket import *
from time import sleep
import re

class xboxConsole():
    connected = False
    def __init__(self, ip, port=730, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug

    def connect(self):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.ip, self.port))
            response = s.recv(1024)
            if response.decode("cp1252").startswith("201-"):
                self.connected = True
            else:
                return 'invalid ip'
        except:
            return 'invalid ip'

    def send_packet(self, command, recv_ammount=1, recv_bytes=1024):
        if self.connected:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((self.ip, self.port))
            s.send(bytes(command, "cp1252"))
            if recv_ammount == 0:
                return
            data_chunks = []
            debug_packet_count, packet_count = 0,0
            try:
                while recv_ammount != packet_count:
                    chunk = s.recv(recv_bytes)
                    if self.debug == True:
                        print(f'{packet_count}: {chunk}')

                    packet_count += 1
                    data_chunks.append(chunk)

                s.close()

            except timeout:
                s.close()

            if self.debug:
                print(command)
                for chunk in data_chunks:
                    print(chunk)

            return data_chunks
        else:
            return "Not connected to a console"

    def setMemory(self, address, data):
        self.send_packet("setmem addr=" + address + " data=" + data + "\r\n")

    def xNotify(self, message, logo=0):
        if logo > 76 or logo < 0:
            raise ValueError("Invalid xNotifyLogo")

        self.send_packet(f'consolefeatures ver=2 type=12 params="A\\0\\A\\2\\2/{len(message)}\\{message.encode("cp1252").hex()}"\r\n', recv_ammount=0)

    def GetCpuKey(self):
        while True:
            raw = self.send_packet('consolefeatures ver=2 type=10 params="A\\0\\A\\0\\\"\r\n', recv_ammount=2)
            if len(raw) == 2:
                return raw[1].decode().strip()[4:].lstrip()
            else:
                return raw[1]

            bpcounter += 1
            sleep(2)

    def get_xbdm_name(self):
        dbgname = self.send_packet("DBGNAME\r\n", recv_ammount=2)
        if len(dbgname) == 1:
            if isinstance(dbgname[0], bytes):
                dbgname = dbgname[0].decode()
            else:
                dbgname = dbgname[0]

            matches = list(re.finditer(r'\d+- ', dbgname))
            secondend = matches[1].end()
            return dbgname[secondend:].strip()
        else:
            return dbgname[1].decode('utf-8').strip().split()[-1]
