import os, sys
import Tkinter
#from visual import *
#from visual.graph import *
import time
import math
import random

class Node:
# Nodo, simulacion de una neurona.

	def __init__(self,layerNum,nodeNum,nodeVal):
		self.layerNum = layerNum
		self.nodeNum = nodeNum
		self.nodeVal = nodeVal
		self.nodesFrom = []
		self.nodesTo = []
		self.posX = 0.0
		self.posY = 0.0

	def setNodeVal(self,nodeVal):
		self.nodeVal = nodeVal

	def linkTo(self,nodeTo):
		self.nodesTo.append(nodeTo)

	def linkFrom(self,nodeFrom):
		self.nodesFrom.append(nodeFrom)


