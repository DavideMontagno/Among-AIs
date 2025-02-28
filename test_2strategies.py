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

png_gif_dir = "./gif/"
tot=1
debug = False
join_tournament = False
if(join_tournament):
    tournament = "SmartCUP3"
    pltournament1 = Tournament(name="Garada1", tournament=tournament)
    pltournament2 = Tournament(name="Garada2", tournament=tournament)
    pltournament3 = Tournament(name="Garada3", tournament=tournament)
    input('Finished to join in tournament correctly! Press any key to continue..')

def start_game(cellular_a,starting=False):
    res=cellular_a.play(starting)
    return res

def start_chat(cellular_chat):
    res=cellular_chat.read_chat()
    return res

if __name__ == "__main__":


    #PARAMETRI
    NAME_GAME = "Species"
    n_players=1
    flags="W1B"
    
    print(NAME_GAME)

    #INIZIALIZZAZIONE THREAD COMMUNICATION
    manager = multiprocessing.Manager()

    #OTHER_PLAYER_GAME_INTERFACE___________________________________________________________________
    threads=[]
    for i in range(n_players):
        pl=GameInterface(NAME_GAME,NAME_GAME,"Garada"+str(i+1),player_descr="AI9-v1.1",flags=flags)


        print(pl.interact("join"))
        pl.command_chat("name")
        pl.command_chat("join")

        manager_dict = manager.dict()

        if(i%2==1):
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="007") # to Debug
        else:
            ca = CellularAutomata(pl, manager_dict,debug=False,mode="007") # to Debug
        ca_chat = CellularAutomata_chat(pl, manager_dict,debug=False)
        t = multiprocessing.Process(target=start_game, args=(ca,))

        c = multiprocessing.Process(target=start_chat, args=(ca_chat,))
        threads.append(c)
        threads.append(t)
    #_______________________________________________________________________________

    for n in range(0, len(threads)):
        threads[n].start()

    for n in range(len(threads)):
        threads[n].join()
