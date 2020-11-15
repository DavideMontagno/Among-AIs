from player import Player
from CellularAutomata import CellularAutomata
import time
import datetime
import threading


#CREATION
NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

pl1=Player(NAME_GAME,"pl1")
print(pl1.manage_game("new"))

#JOIN GAME
print(pl1.interact("join"))

pl2=Player(NAME_GAME,"pl2")
print(pl2.interact("join"))

pl3=Player(NAME_GAME,"pl3")
print(pl3.interact("join"))

pl4=Player(NAME_GAME,"pl4")
print(pl4.interact("join"))

# START GAME
if(pl1.manage_game("start")=="ERROR 501 Need two non-empty teams to start"):
    print("ERRORE CREAZIONE")
    exit()


print(pl1.status("status"))

print(pl1.status("look"))


ca=CellularAutomata(pl1)
ca.play()
'''t1 = threading.Thread(target=ca.play(), args=(1,))
ca2=CellularAutomata(pl2)
t2 = threading.Thread(target=c2.play(), args=(1,))
ca3=CellularAutomata(pl3)
t3 = threading.Thread(target=c3.play(), args=(1,))
ca3=CellularAutomata(pl4)
t4 = threading.Thread(target=c4.play(), args=(1,))


t1.start()
t2.start()
t3.start()
t3.start()'''
print("Finito.")


