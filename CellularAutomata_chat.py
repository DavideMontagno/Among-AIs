import sys
import os

import datetime
import time


class CellularAutomata_chat():
    def __init__(self,  player, manager_dict,log=False,debug=False): 
        self.player = player
        self.debug = debug
        self.log=log
        self.impostors={}
        self.allies=[]
        self.already_shooted_name=[]
        
        self.manager_dict=manager_dict


    def process_message(self,text):

        # Shot message
        if("hit" in text):

            message=text.split()

            if(self.allies==[]):
                if("allies" in self.manager_dict):
                    self.allies=self.manager_dict["allies"]
                    self.impostors={k:0 for k in self.allies}

            if(self.allies!=[]):
                
                if(message[4] in self.allies and message[2] in self.allies):
                    self.impostors[message[2]]+=1
                    self.manager_dict["impostors"]=self.impostors

            # manage already shooted player
            self.already_shooted_name.append(message[4])
            self.manager_dict["already_shooted_name"]=self.already_shooted_name

        # End game message
        if("Game finished!" in text):
            self.manager_dict["finish"]=True

        # Start game message
        if("Now starting!" in text):
            self.manager_dict["start_match"]=True

        # Initial immortal cooldown end message
        if("Hunting season open!" in text):
            self.manager_dict["cooldown_shot_end"]=True
        
        # Initial cooldown end message
        if("You can now catch the flag!" in text):
            self.manager_dict["cooldown_catch_end"]=True

    def read_chat(self):
        end=False
        chat = []
        if(self.log==False):
            current_chat=self.player.chat
        else:
            current_chat=self.player.chat_log
        count_scores=0

        while(True):
            result = str(current_chat.read_until(
            b"\n").decode("utf-8"))
            chat.append(result)

            if(self.debug): print(result)


            if(self.log==False):
                self.process_message(result)
            else:# Exit condition log chat
                if("SCORES" in result):
                    count_scores+=1
                elif(count_scores>=1):
                    break

            if("Game finished!" in result): #Exit condition chat
                break

        if(self.log):
            print("______________________Salvataggio Log")
            with open('log.txt', 'w') as f:
                for item in chat:
                    f.write("%s\n" % item)
        else:
            if(self.debug): 
                file_object = open('sample.txt', 'a')
                file_object.write(chat[-1])

            while(True):
                line = str(self.player.chat.read_until(b"\n").decode("utf-8"))
                chat.append(line)
                if(self.debug): 
                    file_object.write(line+"\n")
                    print(line)

                if("-----------------" in line):
                    return 0
        return 0
