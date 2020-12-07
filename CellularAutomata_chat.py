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
        
        self.manager_dict=manager_dict


    def process_message(self,text):

        if("hit" in text):

            if(self.allies==[]):
                if("allies" in self.manager_dict):
                    self.allies=self.manager_dict["allies"]
                    self.impostors={k:0 for k in self.allies}
            if(self.allies!=[]):
                message=text.split()
                if(message[4] in self.allies and message[2] in self.allies):
                    self.impostors[message[2]]+=1
                    self.manager_dict["impostors"]=self.impostors
        if("Game finished!" in text):
            self.manager_dict["finish"]=True
        if("Now starting!" in text):
            self.manager_dict["start_match"]=True
        if("Hunting season open!" in text):
            self.manager_dict["cooldown_shot_end"]=True
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
        
        while(True):
            line = str(self.player.chat.read_until(b"\n").decode("utf-8"))
            chat.append(line)
            if(self.debug): print(line)
            if("-----------------" in line):
                return 0
