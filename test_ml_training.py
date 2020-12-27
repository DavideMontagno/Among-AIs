from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing
from random import randint

def start_game(cellular_a,starting=False):
    res=cellular_a.play(starting)
    return res

def start_chat(cellular_chat):
    res=cellular_chat.read_chat()
    return res
def single_match():

    #PARAMETRI
    NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")#"Species"
    n_players=randint(4,8)
    flags="T"
    
    if(randint(0, 1)==1):
        flags+="Q"
    else:
        flags+="W"
    flags+=str(randint(1, 3))

    if(randint(0, 1)==1):
        flags+="B"

    print(NAME_GAME)
    print(flags)
    print(n_players)

    #INIZIALIZZAZIONE THREAD COMMUNICATION
    manager = multiprocessing.Manager()

    #OTHER_PLAYER_GAME_INTERFACE___________________________________________________________________
    threads=[]
    for i in range(n_players):

        #Game Interface
        pl=GameInterface(NAME_GAME,NAME_GAME,"Garada"+str(i+1),player_descr="AI9-v1.1",flags=flags)
        if(i==0):
            pl.manage_game("new")

        #Join game and chat
        print(pl.interact("join"))
        pl.command_chat("name")
        pl.command_chat("join")

        manager_dict = manager.dict()
        
        #Cellular automata
        if(i==0):
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="007",save_maps=True) # to Debug
        else:
            if(i%2==1):
                ca = CellularAutomata(pl, manager_dict,debug=False,mode="007",save_maps=True) # to Debug
            else:
                ca = CellularAutomata(pl, manager_dict,debug=False,mode="007",save_maps=True) # to Debug

        # Cellula automata chat
        if(i==0):
            ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)
        else:
            ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)

        # Multiprocessing
        if(i==0):
            t = multiprocessing.Process(target=start_game, args=(ca,True))
        else:
            t = multiprocessing.Process(target=start_game, args=(ca,))

        c = multiprocessing.Process(target=start_chat, args=(ca_chat,))

        threads.append(c)
        threads.append(t)
    #_______________________________________________________________________________

    for n in range(0, len(threads)):
        threads[n].start()

    for n in range(len(threads)):
        threads[n].join()

if __name__ == "__main__":

    for i in range(0,2):
        print("________________________________________________________STARTING ",i)
        single_match()