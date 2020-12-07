from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing
from Tournament import Tournament

count=0
png_gif_dir = "./gif/"
tot=1


def start_game(cellular_a):
    res= cellular_a.play()
    return res
def start_chat(cellular_chat):
    res= cellular_chat.read_chat()
    return res

stat = []
if __name__ == "__main__":
    
    ### VARIABLE SETTING FOR TOURNAMENT OR LOCAL TEST
    n_player = 5
    n_matches = 2
    tournament = "ai9_testg" ## SET THIS NAME TO JOIN TOURNAMENT, OR DEFINE NAME FOR LOCAL MATCH
    flags="Q1B"


    participate_tournament = False
    repeatly_creation_game = True
    creation_game=True ### SET IT TO TRUE IF YOU WANT CREATE THE GAME
    created=False
    debug=False
    userdata = {}

    manager = multiprocessing.Manager()

    for i in range(0,n_player):
        d = {i:0}
        userdata.update(d)

    #### THREADS FOR MATCH
    manager_game = "" ### USED WHEN WE WANT CREATE A GAME
    threads_player = []
    threads_chat = []


    if(participate_tournament):
        for i in range(0,n_player):
            Tournament(name="AI9-"+str(i+1), tournament=tournament)
        input('Completed registring all players in tournament: '+str(tournament))
    count=0

    for match in range(1,n_matches):
        try:
            NAME_GAME = tournament+"2-"+str(match)
            png_dir = str(NAME_GAME)
            print(NAME_GAME)
            input('Input')
            for i in range(0,n_player):
                temp = GameInterface(NAME_GAME,NAME_GAME,"AI9-"+str(i+1),player_descr="v0.1",flags=flags)

                if(i%2==0):
                    mode="007"
                else:
                    mode="kamikaze"

                if(creation_game):
                    result = temp.manage_game("new").lower()
                    print(result)
                    if(result.find("error")!=-1):
                        print("ERRORE CREAZIONE")
                        exit()
                    else: 
                        creation_game=False
                        created=True
                        manager_game = temp
                print(temp.interact("join"))
                temp.command_chat("name")
                temp.command_chat("join")
                
                manager_dict = manager.dict()
                ca = CellularAutomata(temp, manager_dict,debug=debug,mode=mode) # to Debug
                if(i==0):
                    ca_chat = CellularAutomata_chat(temp, manager_dict,debug=True)
                else:
                    ca_chat = CellularAutomata_chat(temp, manager_dict,debug=False)
                t_player = multiprocessing.Process(target=start_game, args=(ca,))
                chat_player = multiprocessing.Process(target=start_chat, args=(ca_chat,))
                threads_player.append(t_player)
                threads_chat.append(chat_player)
            
                
            for n in range(len(threads_chat)):
                threads_chat[n].start()
            
            for n in range(len(threads_player)):
                threads_player[n].start()

                if(created):
                    manager_game.manage_game("start")
                    print("Game started...")
                    created=False

            for n in range(len(threads_player)):
                userdata[n]+=threads_player[n].join()


            for n in range(len(threads_chat)):
                threads_chat[n].terminate()

            if(repeatly_creation_game):
                creation_game=True
            count+=1
        except:
            pass
    print("Matches completled: "+str(count))
    print(userdata)
