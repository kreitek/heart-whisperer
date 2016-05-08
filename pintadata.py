# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def geomean(nums):
    return (reduce(lambda x, y: x*y, nums))**(1.0/len(nums))

def animate(i):
    pullData = open("medida.txt","r").read()
    dataArray = pullData.split('\n')
    tminar = []
    yminar = []
    tmaxar = []
    ymaxar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            tmin,ymin,tmax,ymax = eachLine.split(' ')
            tminar.append(int(tmin))
            yminar.append(int(ymin))
            tmaxar.append(int(tmax))
            ymaxar.append(int(ymax))

    # Filtramos los ultimos 10 segundos
    last = max(tminar[-1], tmaxar[-1])
    prev = min(tminar[-1], tmaxar[-1])
    i = -1
    while (last - prev) < 10000:
        prev = min(tminar[i], tmaxar[i])
        i = i - 1
    ax1.clear()
    ax1.set_xlabel("Tiempo (ms)")

#    import operator
#    import functools
#    from math import sqrt
#    ax1.plot(tmaxar[i:],ymaxar[i:],label="Maximos (raw). Sistolica:" + str(sum(ymaxar[i:]))/len(ymaxar[i:])))
#    ax1.plot(tminar[i:],yminar[i:],label="Minimos (raw). Diastolica:" + str(sum(yminar[i:])/len(yminar[i:])))

    ax1.plot(tmaxar[i:],ymaxar[i:],label="Maximos (raw). Sistolica:" + str(geomean(ymaxar[i:])))
    ax1.plot(tminar[i:],yminar[i:],label="Minimos (raw). Diastolica:" + str(geomean(yminar[i:])))

    ax1.legend()

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
