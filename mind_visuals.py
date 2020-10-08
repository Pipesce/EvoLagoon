#!/usr/bin/python
# -*- coding: utf-8 -*-

#Como genetic2 pero en Tkinter en vez de VPython

import os, sys
from Tkinter import *
#from visual import *
#from visual.graph import *
import time
import math
import random
from node import *

random.seed(44)

windowX = 800
windowY = 600

nodeRadius = 20.0

mind = Tk()
canvas = Canvas(mind, width=windowX, height=windowY)
canvas.pack(fill='both', expand=1)
mind.title("Creature Mind")


nodeNum = [3,6,2]
layerNum = len(nodeNum)

Wrange = 6.0
WblurRange = 0.4
mutationChance = 0.05

arrowSize = 20.0	#numero mas chico - flecha mas gruesa

nIter = 1000
simulationRate = 100000

inputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

biasN = 0


def activationF(x):
	
	return 2.0/(1.0+math.exp(-x)) - 1

def setW(W):

	for i in range(0,layerNum-1):
		templist_i = []

		for j in range(0,nodeNum[i]+biasN):
			templist_j = []

			for k in range(0,nodeNum[i+1]):
				templist_j.append(Wrange*(random.random()-0.5))
			
			templist_i.append(templist_j)

		W.append(templist_i)

def blurW(W):

	for i in range(0,layerNum-1):

		for j in range(0,nodeNum[i]+biasN):

			for k in range(0,nodeNum[i+1]):
				W[i][j][k] = W[i][j][k] + (WblurRange*(random.random()-0.5))

def mutateW(W):

	for i in range(0,layerNum-1):

		for j in range(0,nodeNum[i]+biasN):

			for k in range(0,nodeNum[i+1]):
				if(mutationChance > random.random()):
					W[i][j][k] = W[i][j][k] + (WblurRange*(random.random()-0.5))				

def drawArrows(W,Nodes):
	
	for i in range(0,layerNum-1):

		for j in range(0,nodeNum[i]+biasN):

			for k in range(0,nodeNum[i+1]):
				
				pos_ix = Nodes[i][j].posX 
				pos_iy = Nodes[i][j].posY 

				pos_fx = Nodes[i+1][k].posX
				pos_fy = Nodes[i+1][k].posY

				pos_label_x = pos_ix + (pos_fx - pos_ix)*0.3
				pos_label_y = pos_iy + (pos_fy - pos_iy)*0.3

				color_a = ('#fff')

				if(W[i][j][k] > 0.0):
					color_a = ('#00f')
				if(W[i][j][k] < 0.0):
					color_a = ('#f00')

				canvas.create_line(pos_ix+nodeRadius, pos_iy, pos_fx-nodeRadius, pos_fy, arrow=LAST, fill=color_a, width=math.fabs(W[i][j][k])/arrowSize)
				canvas.create_text(pos_label_x, pos_label_y, text="%.2f" % (W[i][j][k]))

def initNodes(Nodes):

	for i in range(0,layerNum):

		temp_nodes = []

		for j in range(0,nodeNum[i]+biasN):

			node_ij = Node(i,j,1.0)
			temp_nodes.append(node_ij)

		Nodes.append(temp_nodes)	

def calcNodeVals(Nodes,inputs,W):

	for j in range(0,nodeNum[0]):

		Nodes[0][j].setNodeVal(inputs[j])	


	for i in range(1,layerNum):

		for j in range(0,nodeNum[i]):

			z_ij = 0.0

			for k in range(0,nodeNum[i-1]+biasN):

				z_ij += W[i-1][k][j]*Nodes[i-1][k].nodeVal

			Nodes[i][j].setNodeVal(activationF(z_ij))

def drawNodes(Nodes):

	for i in range(0,layerNum):

		for j in range(0,nodeNum[i]+biasN):

			deltaX = ((windowX-nodeRadius*4.0)/(layerNum-1))
			deltaY = ((windowY-nodeRadius*4.0)/(max(nodeNum)-1+biasN))


			pos_nx = 2.0*nodeRadius + deltaX*i
			pos_ny = 2.0*nodeRadius + 0.5*deltaY*(max(nodeNum)-nodeNum[i]) + deltaY*j
			color_n = ('#00f')
			if(j>nodeNum[i]-1):
				color_n = ('#f0f')
			if(Nodes[i][j].nodeVal<0.0):
				color_n = '#f00'
			

			canvas.create_oval(pos_nx-nodeRadius, pos_ny-nodeRadius, pos_nx+nodeRadius, pos_ny+nodeRadius, fill=color_n)			
			canvas.create_text(pos_nx,pos_ny,text="%.2f" % (Nodes[i][j].nodeVal))
			canvas.update()
			Nodes[i][j].posX = pos_nx
			Nodes[i][j].posY = pos_ny

def clearScreen(mind):
	for obj in mind.objects:
		obj.visible = False

def countObjects():
	k = 0
	for obj in mind.objects:
		k = k+1
	print k


#W[layer of origin][node index of origin][node index of destination]

W = []

setW(W)
#print W

Nodes = []

initNodes(Nodes)

time = 0

while(1>0):

	setW(W)

	#rate(simulationRate)
	#sleep(1)

	inputs = [math.sin(time/10.0),math.cos(time/10.0),random.random(),random.random(),random.random(),random.random()]
	time += 1

	initNodes(Nodes)
	calcNodeVals(Nodes,inputs,W)
	drawNodes(Nodes)
	drawArrows(W,Nodes)
	canvas.update()	

#	countObjects()



