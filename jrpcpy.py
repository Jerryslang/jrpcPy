from socket import *

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

    def sendTextCommand(self, command, recv_ammount=1):
        if self.connected:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((self.ip, self.port))
            s.send(bytes(command, "cp1252"))

            data_chunks = []
            debug_packet_count, packet_count = 0,0
            try:
                while recv_ammount != packet_count:
                    chunk = s.recv(1024)
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
        self.sendTextCommand("setmem addr=" + address + " data=" + data + "\r\n")

    def xNotify(self, message, logo):
        if logo > 76 or logo < 0:
            raise ValueError("Invalid xNotifyLogo")

        self.sendTextCommand(f'consolefeatures ver=2 type=12 params="A\\0\\A\\2\\2/{len(message)}\\{message.encode("cp1252").hex()}"\r\n')

    def GetCpuKey(self):
        raw = self.sendTextCommand('consolefeatures ver=2 type=10 params="A\\0\\A\\0\\\"\r\n', recv_ammount=2)
        if len(raw) == 2:
            key = raw[1].decode().strip()[4:].lstrip()
        else:
            return 'BAD PACKET' # i had a problem with cpukey packets where they would be malformed could be a one time thing but i included this just in case (will add a retry thing later on)
        return key
