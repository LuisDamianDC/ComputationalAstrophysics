# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:47:26 2024

@author: LuisDamiánDC_
"""
pip install numpy
import numpy as np
import matplotlib.pyplot as plt
N=100
L=10
u=np.zeros(L+2)
dx=L/N
Nc=0.8
a=0.8 #velocidad
tf=0.1
dt=Nc*dx/a

x=np.arange(N+1, -0.1, -dx)*L/N

def u0i(x):
    return np.exp(-(x-2))

def u0a(x):
    return np.exp(-(x-2)**2)

def primtocons(p):
    return u

def primtoflux(p):
    return u**2

def constoprim(u):
    return u

u=u0a(x)
ui=u0i(x)
U=constoprim(u)
F=primtoflux(u)
P=primtocons(u)


for t in np.arange(0, tf, dt):
    for i in range(1, N+1):
        U[i]=(U[i+1]+U[i-1])/2-(dt/(2*dx))*(F[i+1]-F[i-1])
        F[i+1]=(U[i]+U[i+1])/2-(dx/(2*dt))*(U[i+1]-U[i])
    F=constoprim(u)
    U=primtoflux(u)
    P=primtocons(u)
    u[0]=u[N+1]
plt.plot(x, U, 'r')
plt.plot(x, P, 'g')
plt.plot(x, F, 'b')