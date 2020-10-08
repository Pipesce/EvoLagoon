#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import Tkinter
#from visual import *
#from visual.graph import *
import time
import math
import random
import node as nod
import mind as mnd

class Creature:
# Características de una criatura.

	maxSpeed = 5.0

	def __init__(self, W, posX, posY, speed, theta):
		"Definir las propiedades de una criatura"
		self.W = W
		self.species = 0
		self.size = 1.0
		self.color = ''
		self.health = 100.0  

		self.state = 'normal'

		self.left_eye_R = 0.0
		self.left_eye_G = 0.0
		self.left_eye_B = 0.0

		self.left_eye_R = 0.0
		self.left_eye_G = 0.0
		self.left_eye_B = 0.0

		self.herbivore = 0
		self.carnivore = 0

		self.vision = []
		self.vision_angle = math.pi/8.0
		self.vision_range = random.random()*100.0

		self.speed = speed
		self.orientation = theta		#0.0 is in the Y direction

		self.posX = posX
		self.posY = posY	

		self.X_2 = posX + 5.0*math.cos(theta) - 20.0*math.sin(theta)
		self.Y_2 = posY + 5.0*math.sin(theta) + 20.0*math.cos(theta)

		self.X_3 = posX - 40.0*math.sin(theta)
		self.Y_3 = posY + 40.0*math.cos(theta)		

		self.X_4 = posX - 5.0*math.cos(theta) - 50.0*math.sin(theta)
		self.Y_4 = posY - 5.0*math.sin(theta) + 50.0*math.cos(theta)

		self.X_5 = posX + 5.0*math.cos(theta) - 50.0*math.sin(theta)
		self.Y_5 = posY + 5.0*math.sin(theta) + 50.0*math.cos(theta)

		self.X_6 = posX - 5.0*math.cos(theta) - 20.0*math.sin(theta)
		self.Y_6 = posY - 5.0*math.sin(theta) + 20.0*math.cos(theta)

		self.nodeWeb = []
		mnd.initNodes(self.nodeWeb)

		self.alive = 1

	#	self.distanceToTarget = 1.0
	#	self.targetColor = (0.0,0.0,0.0)

	def setSpeed(speed):
		self.speed = speed

	def setOrientation(theta):
		self.orientation = theta % (2.0*math.pi)

	def changeOrientation(theta):
		"turn, clockwise is positive (?)"
		self.orientation = (self.orientation + theta) % (2.0*math.pi)

	def changeSpeed(vel):
		"turn, clockwise is positive (?)"
		newSpeed = (self.speed + vel)
		if(newSpeed > maxSpeed):
			newSpeed = maxSpeed
		if(newSpeed < 0.0):
			newSpeed = 0.0
		self.speed = newSpeed

	def initCreatureNodes(creatur):
		mnd.initNodes(creatur.nodeWeb)




