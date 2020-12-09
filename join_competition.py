from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
from Tournament import Tournament
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
    

    ## start with tournament
    tournament = "SmartCUP"
    pltournament1 = Tournament(name="ai9_pl1", tournament=tournament)
    pltournament2 = Tournament(name="ai9_pl2", tournament=tournament)
    pltournament3 = Tournament(name="ai9_pl3", tournament=tournament)
    input('Finished to join in tournament correctly! Press any key to continue..')
    ##start with game
    manager = multiprocessing.Manager()
    for i in range(1, 13):
        value=tournament+"-"+str(i)+"-1"
        print("Start game on: "+value)
        input('wait')
        SAME_NAME = value
        NAME_GAME = SAME_NAME#+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        NAME_CHAT = SAME_NAME
        debug = False
        debug_chat = False


        pl1=GameInterface(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl1",player_descr="ai9_1.0")
        print(pl1.interact("join"))
        ai_dict = manager.dict()
        ca=CellularAutomata(pl1,ai_dict,debug=debug,mode='007')
        ca_chat = CellularAutomata_chat(pl1,ai_dict,debug=debug_chat)
        pl1.command_chat("join")
        t_pl1 = multiprocessing.Process(target=start_game, args=(ca,))
        c_pl1 = multiprocessing.Process(target=start_chat, args=(ca_chat,))

        
        pl2=GameInterface(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl2",player_descr="ai9_1.0")
        print(pl2.interact("join"))
        ai_dict = manager.dict()
        ca2=CellularAutomata(pl2,ai_dict,debug=debug,mode='kamikaze')
        ca2_chat = CellularAutomata_chat(pl2,ai_dict,debug=debug_chat)
        t_pl2 = multiprocessing.Process(target=start_game, args=(ca2,))
        c_pl2 = multiprocessing.Process(target=start_chat, args=(ca2_chat,))
        pl2.command_chat("name")
        pl2.command_chat("join")

        
        pl3=GameInterface(game_name=NAME_GAME,chat_name=NAME_CHAT,player_name="ai9_pl3",player_descr="ai9_1.0")
        
        print(pl3.interact("join"))
        ai_dict = manager.dict()
        ca3=CellularAutomata(pl3,ai_dict,debug=debug, mode='kamikaze')
        ca3_chat = CellularAutomata_chat(pl3,ai_dict,debug=debug_chat)
        t_pl3 = multiprocessing.Process(target=start_game, args=(ca3,))
        c_pl3 = multiprocessing.Process(target=start_chat, args=(ca3_chat,))
        pl3.command_chat("name")
        pl3.command_chat("join")

        
        
        
        t_pl1.start()
        t_pl2.start()
        t_pl3.start()


        c_pl1.start()
        c_pl2.start()
        c_pl3.start()

        t_pl1.join()
        t_pl2.join()
        t_pl3.join()

        c_pl1.join()
        c_pl2.join()
        c_pl3.join()



#       c_pl1.terminate()
#       c_pl2.terminate()
#       c_pl3.terminate()
        #pl1.command_chat("leave")
        #pl2.command_chat("leave")
        #pl3.command_chat("leave")
    print("finished")
