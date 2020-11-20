from player import Player
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

        pl1=Player(NAME_GAME,NAME_GAME,"pl1")
        print(pl1.manage_game("new"))
        #JOIN GAME
        print(pl1.interact("join"))
        pl1.command_chat("name")
        pl1.command_chat("join")
        pl2=Player(NAME_GAME,NAME_GAME,"ai9_pl2")
        print(pl2.interact("join"))
        
        #print(pl2.chat("join", chat_name=NAME_GAME))
        pl3=Player(NAME_GAME,NAME_GAME,"pl3")
        print(pl3.interact("join"))
        #print(pl3.chat("join", chat_name=NAME_GAME))
        pl4=Player(NAME_GAME,NAME_GAME,"pl4")
        print(pl4.interact("join"))
        #print(pl4.chat("join", chat_name=NAME_GAME))
        pl5=Player(NAME_GAME,NAME_GAME,"pl5")
        print(pl5.interact("join"))
        #print(pl5.chat("join", chat_name=NAME_GAME))
        pl6=Player(NAME_GAME,NAME_GAME,"pl6")
        print(pl6.interact("join"))
        #print(pl6.chat("join", chat_name=NAME_GAME))
        pl7=Player(NAME_GAME,NAME_GAME,"pl7")
        print(pl7.interact("join"))
        #print(pl7.chat("join", chat_name=NAME_GAME))
        pl8=Player(NAME_GAME,NAME_GAME,"pl8")
        print(pl8.interact("join"))
        #print(pl8.chat("join", chat_name=NAME_GAME))
        '''pl9=Player(NAME_GAME,"pl9")
        print(pl9.interact("join"))
        #print(pl9.chat("join", chat_name=NAME_GAME))
        pl10=Player(NAME_GAME,"pl10")
        print(pl10.interact("join"))
        #print(pl10.chat("join", chat_name=NAME_GAME))
        pl11=Player(NAME_GAME,"pl11")
        print(pl11.interact("join"))
        #print(pl11.chat("join", chat_name=NAME_GAME))
        pl12=Player(NAME_GAME,"pl12")
        print(pl12.interact("join"))
        #print(pl12.chat("join", chat_name=NAME_GAME))
        pl13=Player(NAME_GAME,"pl13")
        print(pl13.interact("join"))
        #print(pl13.chat("join", chat_name=NAME_GAME))
        pl14=Player(NAME_GAME,"pl14")
        print(pl14.interact("join"))
        #print(pl14.chat("join", chat_name=NAME_GAME))
        pl15=Player(NAME_GAME,"pl15")
        print(pl15.interact("join"))
        #print(pl15.chat("join", chat_name=NAME_GAME))
        #input("Press Enter to continue...")'''
        # START GAME
       

        if(pl1.manage_game("start")=="ERROR 501 Need two non-empty teams to start"):
            print("ERRORE CREAZIONE")
            exit()
        else: print("Started")
        #print(pl1.status("look"))


        ca=CellularAutomata(pl1)
        ca_chat = CellularAutomata_chat(pl1)
        #result = ca.play()

        t1 = multiprocessing.Process(target=start_game, args=(ca,))
        c1 = multiprocessing.Process(target=start_chat, args=(ca_chat,))
        ca2=CellularAutomata(pl2)
        t2 = multiprocessing.Process(target=start_game, args=(ca2,))
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
        '''ca9=CellularAutomata(pl9)
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
        threads = [t1, c1]#,t2,t3,t4,t5,t6,t7,t8]#,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,c1]
        #threads = [t1,c1]
        for n in range(len(threads)):
            threads[n].start()
        # Wait all threads to finish.
        for n in range(len(threads)):
            threads[n].join()
        name="work"
        '''if(result==True):
            count = count+1
            name="work_"
        else:
            name="error"'''

        print(pl1.status("status"))
        images = []
        for file_name in os.listdir(png_dir):
            if file_name.endswith('.png'):
                file_path = os.path.join(png_dir, file_name)
                images.append(imageio.imread(file_path))
                os.remove(file_path)
        imageio.mimsave(png_gif_dir+name+NAME_GAME+".gif", images)
        os.rmdir(png_dir)
        print("finished")

    except Exception as e:
        print(e)
    '''print("Executed correctly: "+str(count)+" on "+str(tot))
    print("Finito.")'''






