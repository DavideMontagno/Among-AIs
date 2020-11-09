from player import Player
import time
import datetime

NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

pl1=Player(NAME_GAME,"pl1")
print(pl1.manage_game("new"))

print(pl1.interact("join"))

pl2=Player(NAME_GAME,"pl2")
print(pl2.interact("join"))

pl3=Player(NAME_GAME,"pl3")
print(pl3.interact("join"))

pl4=Player(NAME_GAME,"pl4")
print(pl4.interact("join"))

pl5=Player(NAME_GAME,"pl5")
print(pl5.interact("join"))

pl6=Player(NAME_GAME,"pl6")
print(pl6.interact("join"))

pl7=Player(NAME_GAME,"pl7")
print(pl7.interact("join"))

pl8=Player(NAME_GAME,"pl8")
print(pl8.interact("join"))

pl9=Player(NAME_GAME,"pl9")
print(pl9.interact("join"))


print(pl1.manage_game("start"))
print(pl1.status("status"))
print(pl1.status("look"))
print(pl1.interact("move","W"))
print(pl2.interact("move","W"))
print(pl1.status("status"))
print(pl1.status("look"))

