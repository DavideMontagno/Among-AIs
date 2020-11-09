from player import Player
import time
import datetime

NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

pl1 = Player(NAME_GAME, "pl1")
print(pl1.manage_game("new"))

print(pl1.interact("join"))
print(pl1.process_map())
