import random
import pickle
import time
from scipy.spatial import distance
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid, Node
from pathfinding.finder.a_star import AStarFinder
import sys
import os
import telnetlib
import datetime
import matplotlib.pyplot as plt


class Tournament():
    def __init__(self, name, tournament, host="margot.di.unipi.it",chat_port=8422):
        self.name = name
        self.registration = telnetlib.Telnet(host,chat_port)
        self.registration.write(bytes("NAME "+name+"\n", "utf-8"))
        self.registration.write(bytes("POST "+tournament+" join\n", "utf-8"))
      

       
            
                
