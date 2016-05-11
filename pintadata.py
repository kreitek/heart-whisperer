#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
# from serial import Serial
import sys
from math import log

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
fichero = sys.argv[1]

# s = Serial(port="/dev/ttyUSB0", baudrate=115200)

def geomean(nums):
    n = len(nums) if len(nums) < 60 else 60
#    print n
    return (reduce(lambda x, y: x*y, nums[-n:]))**(1.0/n)
    #reduce(lambda x, y: x*y, nums))**(1.0/int(len(nums)))
    #try:
    #	return (reduce(lambda x, y: x*y, nums))**(1.0/int(len(nums)))
    #except OverflowError:
    #	return -1

def formula(x):
    	#result = nums*0.524152
	return (0.26455*x + 54.4878)

def interpol(maxm):
	sistolica = formula(maxm)
	if maxm < 100:
		result = "Fototipo 3 o sup."
	elif maxm > 600:
		result = "Saturado"
	elif sistolica > 150:
		result = "Tension Alta! (" + str(sistolica) + ")"
	elif sistolica < 110:
		result = "Tension Baja! (" + str(sistolica) + ")"
	else:
            result = str(sistolica)
	return result

def diferencial(maxm, minm):
	dif = maxm - minm
	sistolica = formula(maxm)
	result = ""

	if dif > 10 and dif < 20:
		difreal = str(sistolica - 60)
	elif dif > 20 and dif < 25:
		difreal = str(sistolica - 70)
	else:
		difreal = -1

	if difreal != -1:
		diastolica = str(difreal)
	else:
		diastolica = "!! "+ str(dif)

	if maxm < 100:
		result = "Fototipo 3 o sup."
	elif maxm > 600:
		result = "Saturado"
	elif sistolica > 150:
		result = "Tension Alta! (" + diastolica + ")"
	elif sistolica < 110:
		result = "Tension Baja! (" + diastolica + ")"
	else:
		result = diastolica
	return result
		

def animate(i):
    pullData = open(fichero,"r").read()
    dataArray = pullData.split('\n')
    tminar = []
    yminar = []
    tmaxar = []
    ymaxar = []
    for eachLine in dataArray:
        if len(eachLine.split(' ')) == 4:
            try:
                tmin,ymin,tmax,ymax = eachLine.split(' ')
                tminar.append(int(tmin))
                yminar.append(int(ymin))
                tmaxar.append(int(tmax))
                ymaxar.append(int(ymax))
            except ValueError, e:
                tminar.append(0)
                yminar.append(0)
                tmaxar.append(0)
                ymaxar.append(0)
                pass  # rint "Error", e

    if len(tminar) == 0:
        tminar, tmaxar = [0], [0]
        yminar, ymaxar = [0], [0]

    # Filtramos los ultimos 10 segundos
    last = max(tminar[-1], tmaxar[-1])
    prev = min(tminar[-1], tmaxar[-1])
    i = -1
    while (last - prev) < 10000 and i > -len(tminar) and i > -120:
        prev = min(tminar[i], tmaxar[i])
        i = i - 1
    ax1.clear()
    ax1.set_xlabel("Tiempo (ms)")

#    import operator
#    import functools
#    from math import sqrt
#    ax1.plot(tmaxar[i:],ymaxar[i:],label="Maximos (raw). Sistolica:" + str(sum(ymaxar[i:]))/len(ymaxar[i:])))
#    ax1.plot(tminar[i:],yminar[i:],label="Minimos (raw). Diastolica:" + str(sum(yminar[i:])/len(yminar[i:])))

    geo_max = geomean(ymaxar[i:])
    geo_min = geomean(yminar[i:])
	
    ax1.plot(tmaxar[i:],ymaxar[i:],label="Maximos (raw). Sistolica:" + str(geo_max) + " Estimado:" + str(interpol(geo_max)))
    ax1.plot(tminar[i:],yminar[i:],label="Minimos (raw). Diastolica:" + str(geo_min) + " Estimado: - ")

    ax1.legend()

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
