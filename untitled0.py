# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:47:26 2024

@author: LuisDamiánDC_
"""

import numpy as np
import matplotlib.pyplot as plt
N=100
L=10
u=np.zeros(L+2)
dx=L/N
a=0.5 #velocidad
tf=1
dt=0.9*L/N/a

x=np.arange(N+1, -0.1, -dx)*L/N

def u0i(x):
    return np.exp(-(x-2))

def u0a(x):
    return np.exp(-(x-2)**2)

def primtocons(p):
    return p

def primtoflux(p):
    return p

def constoprim(u):
    return a*u

#f=u0i(x)
u=u0a(x)
ui=u0a(x)
u[0]=u[N+1]
F=constoprim(u)
U=primtoflux(u)
P=primtocons(u)
#plt.plot(x, f)
#plt.plot(x, u)


for t in np.arange(0, tf, dt):
    print(t)
    for i in range(1, N+1):
        u[i]=(u[i+1]+u[i-1])/2-a*dt/(2*dx)*(F[i+1]-F[i-1])
        #u[i]=u[i]-a*dt/(2*dx)*(u[i+1]-u[i-1])
    
plt.plot(x, u)
plt.plot(x, ui)