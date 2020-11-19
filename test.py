from player import Player
from CellularAutomata import CellularAutomata
import time
import datetime
import threading
import os
import imageio
import multiprocessing


def start_game(cellular_a):
    cellular_a.play()

if __name__ == "__main__":
    
    NAME_GAME = "ai9_tes12"#+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    pl1=Player(NAME_GAME,"ai9_pl17")
    #print(pl1.manage_game("new"))
    print(pl1.interact("join"))
    
    
    ca=CellularAutomata(pl1)
    t1 = multiprocessing.Process(target=start_game, args=(ca,))
    

    threads = [t1]
    for n in range(len(threads)):
        threads[n].start()
    
    # Wait all threads to finish.
    for n in range(len(threads)):
        threads[n].join()
    print("finished")