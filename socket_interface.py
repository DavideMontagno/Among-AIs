import telnetlib
import getpass
import time
import datetime

HOST = "margot.di.unipi.it"
PORT = 8421
NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"/"
print(NAME_GAME)
tn = telnetlib.Telnet(HOST, PORT)
tn.write(bytes("NEW "+NAME_GAME+"\n", 'utf-8')) #this worka!
time.sleep(0.5)
print(tn.read_until(b"\n",550))
print("I'm here")
tn.write(bytes(NAME_GAME+" JOIN maDave H - fff\n", 'utf-8')) #this worka!
print("Writed join command")
print(tn.read_until(b"\n",550))
time.sleep(0.5)
tn.write(bytes(NAME_GAME+" LOOK\n","utf-8"))
print(str(tn.read_until(b"\xc2\xbb",550).decode("utf-8") ))
time.sleep(0.5)
tn.write(bytes(NAME_GAME+" START\n","utf-8"))
print(str(tn.read_until(b"\n",550)))
time.sleep(0.5)
tn.write(bytes(NAME_GAME+" SHOOT E\n","utf-8"))
print(str(tn.read_until(b"\n",550)))