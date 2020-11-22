from player import Player
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing


def start_game(cellular_a):
    cellular_a.play()

def start_chat(cellular_a):
    cellular_a.read_chat()

if __name__ == "__main__":
    
    NAME_GAME = "ai9_webapp2.2_4_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    NAME_CHAT = "ai9_webapp2.2_4"
    debug = True

    pl1=Player(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl7",player_descr="ai9_1.0")
    #pl2=Player(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl8",player_descr="ai9_1.0")
    #pl3=Player(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl3",player_descr="ai9_1.0")
   
    print(pl1.manage_game("new"))
    print(pl1.interact("join"))
    #print(pl2.interact("join"))
    #print(pl3.interact("join"))
    
    ca=CellularAutomata(pl1,debug=debug)
    ca_chat = CellularAutomata_chat(pl1)
    t_pl1 = multiprocessing.Process(target=start_game, args=(ca,))
    c_pl1 = multiprocessing.Process(target=start_chat, args=(ca_chat,))
    pl1.command_chat("name")
    pl1.command_chat("join")



    '''ca2=CellularAutomata(pl2,debug=debug)
    ca2_chat = CellularAutomata_chat(pl2)
    t_pl2 = multiprocessing.Process(target=start_game, args=(ca2,))
    c_pl2 = multiprocessing.Process(target=start_chat, args=(ca2_chat,))
    pl2.command_chat("name")
    pl2.command_chat("join")'''


    '''ca3=CellularAutomata(pl3,debug=debug)
    ca3_chat = CellularAutomata_chat(pl3)
    t_pl3 = multiprocessing.Process(target=start_game, args=(ca3,))
    c_pl3 = multiprocessing.Process(target=start_chat, args=(ca3_chat,))
    pl3.command_chat("name")
    pl3.command_chat("join")'''



    t_pl1.start()
    #t_pl2.start()
    c_pl1.start()
    #c_pl2.start()
    #c_pl1.start()
    t_pl1.join()
    #t_pl2.join()
    c_pl1.terminate()
    #c_pl2.terminate()
    print("finished")