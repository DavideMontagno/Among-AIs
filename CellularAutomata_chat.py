import sys
import os

import datetime
import time


class CellularAutomata_chat():
    def __init__(self,  player, manager_dict,debug=False): 
        self.player = player
        self.debug = debug
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
        while(True):
            result = str(self.player.chat.read_until(
            b"\n").decode("utf-8"))
            chat.append(result)

            self.process_message(result)

            if(self.debug): print(result)
            if("Game finished!" in result): 
                break
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
