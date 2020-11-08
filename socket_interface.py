import telnetlib
import getpass
import time
import datetime

# Connection
HOST = "margot.di.unipi.it"
PORT = 8421
NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
print(NAME_GAME)
tn_server = telnetlib.Telnet(HOST, PORT)
tn_player = []
time_sleep=0.51
num_players = 8

#Start sending commands
time.sleep(time_sleep+0.10)
tn_server.write(bytes("NEW "+NAME_GAME+"\n", 'utf-8')) #this worka!
time.sleep(time_sleep)
tn_server.write(bytes(NAME_GAME+" LOOK\n","utf-8"))
print(str(tn_server.read_until(b"\xc2\xbb\n",time_sleep).decode("utf-8") ))

for i in range(0,num_players):
    tn_player.append(telnetlib.Telnet(HOST, PORT))
    tn_player[i].write(bytes(NAME_GAME+" JOIN player_"+str(i)+" H - fff\n", 'utf-8')) #this worka!
    print(str(tn_player[i].read_until(b"\n",time_sleep).decode("utf-8") ))
    time.sleep(time_sleep)



time.sleep(time_sleep)
tn_server.write(bytes(NAME_GAME+" START\n","utf-8"))
print(str(tn_server.read_until(b"\n",time_sleep).decode("utf-8")))

time.sleep(time_sleep)
tn_player[0].write(bytes(NAME_GAME+" LOOK\n","utf-8"))
print(str(tn_player[0].read_until(b"\xc2\xbb\n",time_sleep).decode("utf-8") ))


time.sleep(time_sleep)
tn_player[0].write(bytes(NAME_GAME+" STATUS\n","utf-8"))
print(str(tn_player[0].read_until(b"\xc2\xbb\n",time_sleep).decode("utf-8") ))
time.sleep(time_sleep)
tn_player[0].write(bytes(NAME_GAME+" MOVE W\n","utf-8"))
print(str(tn_player[0].read_until(b"\n",time_sleep).decode("utf-8")))
time.sleep(time_sleep)
tn_player[0].write(bytes(NAME_GAME+" LOOK\n","utf-8"))
print(str(tn_player[0].read_until(b"\xc2\xbb\n",time_sleep).decode("utf-8") ))

