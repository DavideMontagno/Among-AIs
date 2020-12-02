from GameInterface import GameInterface
from CellularAutomata import CellularAutomata
from CellularAutomata_chat import CellularAutomata_chat
import time
import datetime
import threading
import os
import imageio
import multiprocessing

count=0
png_gif_dir = "./gif/"
tot=1


def start_game(cellular_a):
    cellular_a.play()
def start_chat(cellular_chat):
    cellular_chat.read_chat()
    pass

if __name__ == "__main__":
    
    try:
        #CREATION
        NAME_GAME = "ai9_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(NAME_GAME)
        png_dir = str(NAME_GAME)

        pl1=GameInterface(NAME_GAME,NAME_GAME,"ai9_pl1",player_descr="9-1")
        print(pl1.manage_game("new"))
        #JOIN GAME
        print(pl1.interact("join"))
        pl1.command_chat("name")
        pl1.command_chat("join")

        pl2=GameInterface(NAME_GAME,NAME_GAME,"ai9_pl2",player_descr="9-1")
        print(pl2.interact("join"))
        pl2.command_chat("name")
        pl2.command_chat("join")

        #print(pl2.chat("join", chat_name=NAME_GAME))
        pl3=GameInterface(NAME_GAME,NAME_GAME,"pl3",player_descr="9-1")
        print(pl3.interact("join"))
        #print(pl3.chat("join", chat_name=NAME_GAME))

        pl4=GameInterface(NAME_GAME,NAME_GAME,"pl4",player_descr="9-1")
        print(pl4.interact("join"))
        #print(pl4.chat("join", chat_name=NAME_GAME))

        pl5=GameInterface(NAME_GAME,NAME_GAME,"pl5",player_descr="9-1")
        print(pl5.interact("join"))
        #print(pl5.chat("join", chat_name=NAME_GAME))

        pl6=GameInterface(NAME_GAME,NAME_GAME,"pl6",player_descr="9-1")
        print(pl6.interact("join"))
        #print(pl6.chat("join", chat_name=NAME_GAME))

        pl7=GameInterface(NAME_GAME,NAME_GAME,"pl7",player_descr="9-1")
        print(pl7.interact("join"))
        #print(pl7.chat("join", chat_name=NAME_GAME))

        pl8=GameInterface(NAME_GAME,NAME_GAME,"pl8",player_descr="9-1")
        print(pl8.interact("join"))
        #print(pl8.chat("join", chat_name=NAME_GAME))

        # START GAME
       

        if(pl1.manage_game("start").lower().find("error")!=-1):
            print("ERRORE CREAZIONE")
            exit()
        else: print("Started")
        #print(pl1.status("look"))


        #ca=CellularAutomata(pl1)
        ca = CellularAutomata(pl1, debug=False) # to Debug
        ca_chat = CellularAutomata_chat(pl1,debug=True)
        #result = ca.play()
        
        t1 = multiprocessing.Process(target=start_game, args=(ca,))
        c1 = multiprocessing.Process(target=start_chat, args=(ca_chat,))
        '''
        ca2=CellularAutomata(pl2)
        ca_chat2 = CellularAutomata_chat(pl2)
        t2 = multiprocessing.Process(target=start_game, args=(ca2,))
        c2 = multiprocessing.Process(target=start_chat, args=(ca_chat2,))
        ca3=CellularAutomata(pl3)
        t3 = multiprocessing.Process(target=start_game, args=(ca3,))
        ca4=CellularAutomata(pl4)
        t4 = multiprocessing.Process(target=start_game, args=(ca4,))
        ca5=CellularAutomata(pl5)
        t5 = multiprocessing.Process(target=start_game, args=(ca5,))
        ca6=CellularAutomata(pl6)
        t6 = multiprocessing.Process(target=start_game, args=(ca6,))
        ca7=CellularAutomata(pl7)
        t7 = multiprocessing.Process(target=start_game, args=(ca7,))
        ca8=CellularAutomata(pl8)
        t8 = multiprocessing.Process(target=start_game, args=(ca8,))
        ca9=CellularAutomata(pl9)
        t9 = multiprocessing.Process(target=start_game, args=(ca9,))
        ca10=CellularAutomata(pl10)
        t10 = multiprocessing.Process(target=start_game, args=(ca10,))
        ca11=CellularAutomata(pl11)
        t11 = multiprocessing.Process(target=start_game, args=(ca11,))
        ca12=CellularAutomata(pl12)
        t12 = multiprocessing.Process(target=start_game, args=(ca12,))
        ca13=CellularAutomata(pl13)
        t13 = multiprocessing.Process(target=start_game, args=(ca13,))
        ca14=CellularAutomata(pl14)
        t14 = multiprocessing.Process(target=start_game, args=(ca14,))
        ca15=CellularAutomata(pl15)
        t15 = multiprocessing.Process(target=start_game, args=(ca15,))
        '''
        threads = [t1,c1]# , c1] ,t2,c2],t2,t3,t4,t5,t6,t7,t8]#,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,c1]
        #threads = [t1,c1]
        for n in range(len(threads)):
            threads[n].start()
        # Wait all threads to finish.
        t1.join()
        name="work"
        c1.terminate()
    except Exception as e:
        print(e)
