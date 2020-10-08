#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from Tkinter import *
#from visual import *
#from visual.graph import *
import time
import math
import random
import node as nod
import mind as mnd
import creature as creat
import aquatic_object as aqo

data = open("lagoon_data.txt", "w")

random.seed(2112)
colors_ = ["#333","#366","#636","#663","#666","#c66","#6c6","#66c","#cc6","#c6c","#6cc","#ccc","#ccf","#cfc","#fcc","#ffc","#fcf","#cff","#fff"]

t_i = time.time()
sim_time = 100.5*3600.0

#simulationNum = 100

windowX = 1280				#dimension X de la ventana
windowY = 800				#dimension Y de la ventana
habX = 290					#dimension X del laberinto
habY = 390					#dimension X del laberinto

v_init = 0.3				#velocidad inicial de cada nave
angle_init = -3.14/2.0		#angulo inicial de cada nave
vMax = 10.0					#velocidad maxima
v_cap = 5.0					#ponderacion (negativa) para calcular delta_v
angle_cap = 1000.0			#ponderacion (negativa) para calcular delta_teta
minSize = 0.05

np = 	250			#numero de peces

food_appear_rate = 0.15
max_food_number = 600
health_drop_rate = 0.0001

reprod_health = 300.0
reprod_cost = 100.0

herb_rate = 0.7
carn_rate = 0.4

species_stats_counter = 100

timeInterval = 10

brain_debug = 0

Fishes = []					#lista de datos de los peces
Shapes = []					#lista de figuras, graficos de los peces
Food = []

fitness = []				

habs = Tk()
canvas = Canvas(habs, width=windowX, height=windowY)
canvas.pack(fill='both', expand=1)
habs.title("Lagoon")
canvas.create_rectangle(0,0,windowX,windowY,fill='#00d')

brain_i = 1					#indice de la nave mostrada en el cerebro
brain_counter = 0			#contador interno para el cerebro
brain_redraw_rate = 2		#cada cuantos pasos se calculan los nodos cerebrales
brain_calc_rate = 100		#relacion de simulaciones sin y con calculo paso a paso

simulation_counter = 0		#contador que dice cuantas simulaciones van

if(brain_debug):

	brain = Toplevel()
	brain_canvas = Canvas(brain, height=600, width=800)
	brain.geometry('800x600+360+0')

	brain_canvas.pack(expand=YES, fill=BOTH)
	brain.title("Ship %i Brain – Simulation number %i." % (brain_i, simulation_counter))

	def drawBrain():
		#Dibujar el cerebro en cada nueva iteracion.
		brain_canvas.delete("all")

		mnd.drawNodes(Fishes[brain_i].nodeWeb, brain_canvas)
		mnd.drawArrows(Fishes[brain_i].W, Fishes[brain_i].nodeWeb, brain_canvas)

		brain.title("Ship %i Brain – Simulation number %i." % (brain_i, simulation_counter))
		brain_canvas.update()	

	def redrawBrain():
		#Redibujar el cerebro en cada nueva iteracion.
		mnd.drawNodes(Fishes[brain_i].nodeWeb, brain_canvas)
		brain_canvas.update()	

def random_color():
	
    return random.choice(colors_)

def set_XY(i):

	theta = Fishes[i].orientation
	sz = Fishes[i].size

	Fishes[i].X_2 = Fishes[i].posX - sz*5.0*math.cos(theta) - sz*20.0*math.sin(theta)
	Fishes[i].Y_2 = Fishes[i].posY - sz*5.0*math.sin(theta) + sz*20.0*math.cos(theta)

	Fishes[i].X_3 = Fishes[i].posX - sz*40.0*math.sin(theta)
	Fishes[i].Y_3 = Fishes[i].posY + sz*40.0*math.cos(theta)	

	Fishes[i].X_4 = Fishes[i].posX - sz*10.0*math.cos(theta) - sz*45.0*math.sin(theta)
	Fishes[i].Y_4 = Fishes[i].posY - sz*10.0*math.sin(theta) + sz*45.0*math.cos(theta)

	Fishes[i].X_5 = Fishes[i].posX + sz*10.0*math.cos(theta) - sz*45.0*math.sin(theta)
	Fishes[i].Y_5 = Fishes[i].posY + sz*10.0*math.sin(theta) + sz*45.0*math.cos(theta)

	Fishes[i].X_6 = Fishes[i].posX + sz*5.0*math.cos(theta) - sz*20.0*math.sin(theta)
	Fishes[i].Y_6 = Fishes[i].posY + sz*5.0*math.sin(theta) + sz*20.0*math.cos(theta)

def defineFishes():
	#Definir los peces al comienzo
	for i in range(np):

		W_i = []
		mnd.setW(W_i)
		ship_i = creat.Creature(W_i, windowX*random.random(), windowY*random.random(), vMax*(random.random())**2, 6.28*random.random())   #windowX*0.5 + 240*(random.random()-0.5)
		ship_i.color = random_color()
		ship_i.size = 0.75*(random.random()**2)+minSize
		ship_i.species = i

		herb = random.random()
		carn = random.random()

		if(herb < herb_rate):
			ship_i.herbivore = 1
		if(carn < carn_rate):
			ship_i.carnivore = 1
			ship_i.size *= 2.0

		Fishes.append(ship_i)

		fitness.append(10000)

		set_XY(i)

		points = [Fishes[i].posX, Fishes[i].posY, 
			Fishes[i].X_2, Fishes[i].Y_2, 
			Fishes[i].X_3, Fishes[i].Y_3,
			Fishes[i].X_4, Fishes[i].Y_4, 
			Fishes[i].X_5, Fishes[i].Y_5,
			Fishes[i].X_3, Fishes[i].Y_3,
			Fishes[i].X_6, Fishes[i].Y_6]

		color_outline = 'black'

		if(Fishes[i].carnivore == 1):
			color_outline = 'red'

		if(Fishes[i].herbivore == 1):
			color_outline = 'green'

		if(Fishes[i].carnivore == 1 and Fishes[i].herbivore == 1):
			color_outline = 'white'

		if(not (Fishes[i].carnivore == 1) and not (Fishes[i].herbivore == 1)):
			color_outline = 'black'

		fish = Fishes[i]
		Shapes.append(canvas.create_polygon(points, outline=color_outline, fill=ship_i.color, width=2))


	#	drawVision(fish)

def drawVision(fish):
	
	va = fish.vision_angle
	vr = fish.vision_range
	theta = fish.orientation

	v_points = [fish.posX - vr*math.cos(theta+va) + vr*math.sin(theta+va),
		fish.posY - vr*math.sin(theta+va) - vr*math.cos(theta+va),
		fish.posX,
		fish.posY,
		fish.posX + vr*math.cos(theta-va) + vr*math.sin(theta-va),
		fish.posY + vr*math.sin(theta-va) - vr*math.cos(theta-va)
		]

	canvas.delete(fish.vision)
	fish.vision = canvas.create_line(v_points)

def createFood():
	rnd_f = random.random()
	if(rnd_f > 1.0-food_appear_rate and len(Food) < max_food_number):
		rnd_x = windowX*random.random()
		rnd_y = windowY*random.random()

		points_f = [rnd_x+5,rnd_y,rnd_x,rnd_y+5,rnd_x-5,rnd_y,rnd_x,rnd_y-5]

		fd_i = aqo.AquaticObject(rnd_x,rnd_y)
		Food.append(fd_i)

		Food[-1].X = rnd_x
		Food[-1].Y = rnd_y

		Food[-1].figure = canvas.create_polygon(points_f, outline='black', fill='green', width=1)

def checkFeed():

	for i, elem_i in reversed(list(enumerate(Fishes))):
		for j in range(len(Food)):
			if(math.fabs(Fishes[i].posX-Food[j].X) < 5.0+elem_i.size and math.fabs(Fishes[i].posY-Food[j].Y) < 5.0+elem_i.size and Fishes[i].herbivore):
				
				canvas.delete(Food[j].figure)
				Food.pop(j)

				Fishes[i].health += 25.0 # /Fishes[i].size

	#			print "Un pez de la especie %i se ha comido un alga, ahora tiene una vida de %.1f. Quedan %i peces." % (Fishes[i].species, Fishes[i].health, len(Fishes))
				break
		for j, elem_j in reversed(list(enumerate(Fishes))):
			if(math.fabs(Fishes[i].posX-Fishes[j].posX) < 5.0+(elem_i.size-elem_j.size) and math.fabs(Fishes[i].posY-Fishes[j].posY) < 5.0+(elem_i.size-elem_j.size) and Fishes[i].carnivore and (Fishes[i].size / Fishes[j].size) > 1.5 and i!=j):

				Fishes[i].health += (Fishes[j].health/10.0)*Fishes[j].size/Fishes[i].size
	#			print "El pez %i, de tamaño %.2f, se ha comido al pez %i, de tamaño %.2f." % (i, Fishes[i].size, j, Fishes[j].size)
				elem_j.alive = 0
	#			print "Un pez de la especie %i ha muerto luego de %.2f segundos." % (Fishes[i].species, fitness[i])
				canvas.delete(Fishes[j].vision)
				Fishes.pop(j)
				canvas.delete(Shapes[j])
				Shapes.pop(j)


	#			print "Un pez de la especie %i se ha comido un alga, ahora tiene una vida de %.1f. Quedan %i peces." % (Fishes[i].species, Fishes[i].health, len(Fishes))
				break

def reproduce(i):

	if(Fishes[i].health > reprod_health):

		Fishes[i].health -= reprod_cost

		W_i = Fishes[i].W
		mnd.mutateW(W_i)

		p_x = Fishes[i].posX + 20.0*(random.random()-0.5)
		p_y = Fishes[i].posY + 20.0*(random.random()-0.5)
		or_ = 6.29*random.random()
		vel_ = vMax*random.random()

		ship_i = creat.Creature(W_i, p_x, p_y, vel_, or_)   #windowX*0.5 + 240*(random.random()-0.5)
		ship_i.color = Fishes[i].color
		ship_i.size = Fishes[i].size*(1.0+0.1*(random.random()-0.5))
		if(ship_i.size < minSize):
			ship_i.size = minSize
		ship_i.species = Fishes[i].species

		ship_i.herbivore = Fishes[i].herbivore
		ship_i.carnivore = Fishes[i].carnivore

		Fishes.append(ship_i)

		fitness.append(10000)

		set_XY(-1)
	
		points = [Fishes[-1].posX, Fishes[-1].posY, 
			Fishes[-1].X_2, Fishes[-1].Y_2, 
			Fishes[-1].X_3, Fishes[-1].Y_3,
			Fishes[-1].X_4, Fishes[-1].Y_4, 
			Fishes[-1].X_5, Fishes[-1].Y_5,
			Fishes[-1].X_3, Fishes[-1].Y_3,
			Fishes[-1].X_6, Fishes[-1].Y_6]

		color_outline = 'black'

		if(Fishes[i].carnivore == 1):
			color_outline = 'red'

		if(Fishes[i].herbivore == 1):
			color_outline = 'green'

		if(Fishes[i].carnivore == 1 and Fishes[i].herbivore == 1):
			color_outline = 'white'

		Shapes.append(canvas.create_polygon(points, outline=color_outline, fill=Fishes[i].color, width=2))

	#	print "¡Un pez de la especie %i se ha reproducido!" % (Fishes[i].species)

def periodicity():

	for i in range(len(Fishes)):

		if(Fishes[i].posX > windowX):
			Fishes[i].posX -= windowX
			Fishes[i].X_2 -= windowX
			Fishes[i].X_3 -= windowX
			Fishes[i].X_4 -= windowX
			Fishes[i].X_5 -= windowX
			Fishes[i].X_6 -= windowX

		if(Fishes[i].posX < 0.0):
			Fishes[i].posX += windowX
			Fishes[i].X_2 += windowX
			Fishes[i].X_3 += windowX
			Fishes[i].X_4 += windowX			
			Fishes[i].X_5 += windowX
			Fishes[i].X_6 += windowX

		if(Fishes[i].posY > windowY):
			Fishes[i].posY -= windowY
			Fishes[i].Y_2 -= windowY
			Fishes[i].Y_3 -= windowY
			Fishes[i].Y_4 -= windowY
			Fishes[i].Y_5 -= windowY
			Fishes[i].Y_6 -= windowY

		if(Fishes[i].posY < 0.0):
			Fishes[i].posY += windowY
			Fishes[i].Y_2 += windowY
			Fishes[i].Y_3 += windowY
			Fishes[i].Y_4 += windowY
			Fishes[i].Y_5 += windowY
			Fishes[i].Y_6 += windowY		

def getInputs():
	#función que actualiza los valores de entrada en cada iteración
	for i in range(len(Fishes)):

		Fishes[i].nodeWeb[0][0].nodeVal = (Fishes[i].health)/reprod_health
		Fishes[i].nodeWeb[0][1].nodeVal = 2.0*(((Fishes[i].orientation)%(2.0*math.pi))-math.pi)
		Fishes[i].nodeWeb[0][2].nodeVal = 2.0*(Fishes[i].speed/vMax)-1.0

def checkInteraction():

	arfarf = 1

def checkHealth():

	for i, elem in reversed(list(enumerate(Fishes))):
		param = 1.0
		if(elem.herbivore):
			param *= 2.5
		if(elem.carnivore):
			param *= 3.0
		if(elem.herbivore and elem.carnivore):
			param *= 3.0
		if(elem.herbivore == 0 and elem.carnivore == 0):
			param = 100000.0

		elem.health -= health_drop_rate*(5.0)*(1.0+(elem.speed/vMax))*param

		if(elem.health < 0.0):
			elem.alive = 0
	#		print "Un pez de la especie %i ha muerto luego de %.2f segundos." % (Fishes[i].species, fitness[i])
			canvas.delete(elem.vision)
			Fishes.pop(i)
			canvas.delete(Shapes[i])
			Shapes.pop(i)
			fitness[i] = (time.time()-t_i)

def fieldCalc(fish):
	Xfield = 0.0
	Yfield = 0.0

	for j in range(len(Food)):
		Xfield += (1.0/(Food[j].X-fish.posX)**2)

			
def checkDead():
	#funcion que determina si quedan naves vivas
	for i in range(len(Fishes)):
		if(Fishes[i].alive == 1):
			return 1

	return 0

def median(lst):
    #calculo de la mediana de una lista
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0	

def percentile(lst,cutoffNum):
    #calculo de cualquier percentil de una lista
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // cutoffNum

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0	

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def main():
	global habs, brain, brain_i, brain_counter, simulation_counter

	avgFitness = 0
	spe_stat = 0

	for kk in range(np):
		createFood()

	defineFishes()

	while (simulation_counter<1): 

		simulation_counter += 1

		habs.title("Lagoon")
		
		getInputs()

		if(brain_debug):
			
			drawBrain()

		while (time.time()-t_i < sim_time):

			getInputs()

			createFood()

			for i in range(len(Fishes)):                  # start the dance

			#	print "La velocidad del organismo " + str(i) + " es " + str(Fishes[i].speed)
			#	print "La orientación del organismo " + str(i) + " es " + str(Fishes[i].orientation) + "\n"
			
				inputs_i = [Fishes[i].posX, Fishes[i].posY, Fishes[i].orientation, Fishes[i].speed]
			
				mnd.calcNodeVals(Fishes[i].nodeWeb, inputs_i, Fishes[i].W)

				d_vel = (Fishes[i].nodeWeb[-1][0].nodeVal)/v_cap
				d_orient = (Fishes[i].nodeWeb[-1][1].nodeVal)/angle_cap

#				print Fishes[i].nodeWeb[-1][1].nodeVal

				Fishes[i].speed += d_vel
	
				if (Fishes[i].speed > vMax): 
					Fishes[i].speed = vMax
				if (Fishes[i].speed < 0.0):
					Fishes[i].speed = 0.0

				Fishes[i].orientation = ((Fishes[i].orientation + d_orient) )#  % (4.0*math.pi))

#				print Fishes[i].orientation	

				spd = Fishes[i].speed
				posX = Fishes[i].posX
				posY = Fishes[i].posY
				teta = Fishes[i].orientation

				dx = spd * math.sin(teta)
				dy = -spd * math.cos(teta)

				Fishes[i].posX = posX + dx
				Fishes[i].posY = posY + dy

				set_XY(i)		

				periodicity()

				reproduce(i)

	#			drawVision(Fishes[i])

				canvas.coords(Shapes[i],Fishes[i].posX, Fishes[i].posY, Fishes[i].X_2, Fishes[i].Y_2, Fishes[i].X_3, Fishes[i].Y_3, Fishes[i].X_4, Fishes[i].Y_4, Fishes[i].X_5, Fishes[i].Y_5, Fishes[i].X_3, Fishes[i].Y_3, Fishes[i].X_6, Fishes[i].Y_6)
		#		canvas.move(Shapes[i], dx, dy)



#				checkCollision(Fishes[i], i)
			checkFeed()
			checkHealth()


			if(brain_debug):

				brain_counter += 1

				if(brain_counter >= brain_redraw_rate and (simulation_counter % brain_calc_rate == 0)):
					redrawBrain()
					brain_counter = 0
			
			habs.update_idletasks()
			habs.update()

			spe_stat += 1
			if(spe_stat == species_stats_counter):
				spe_stat = 0
				spe_list = []
				bigfish = []
				for j in range(3*np):
					spe_list.append(0)

				for j in range(len(Fishes)):
					k = Fishes[j].species
					spe_list[k] += 1
					if(k == 143):
						bigfish = Fishes[j]
				print "–––––––––––––––––––––––––––––––– \n"
				for j in range(np):
					if(spe_list[j]>0):
						print "Tiempo: %i – La especie %i cuenta con %i individuos. Corresponde a %.1f%% de la población." % ((time.time()-t_i), j, spe_list[j],100.0*spe_list[j]/len(Fishes))
				print "–––––––––––––––––––––––––––––––– \n"
				data.write("%i \t %i \t %i \t %i \t %i \t %i \n" % (spe_list[15], spe_list[84],spe_list[90], spe_list[269],spe_list[275], len(Fishes)))

	data.close() 

if __name__ == '__main__':
    main()

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
