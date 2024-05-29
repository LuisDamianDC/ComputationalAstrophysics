# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 20:45:11 2024
Simulador del Sistema Solar
@author: LuisDamian
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt
pygame.init()

w, h= 1000, 700
win=pygame.display.set_mode((w, h))
pygame.display.set_caption("Simulador orbital de colisión galáctica")
#Colores de los planetas
blanco= (255, 255, 255)
amarillo = (255, 255, 0)
azul = (100, 149, 237)
rojo = (188, 39, 50)
gris = (80, 78, 81)
verde = (150, 255, 150)
N=1

fuente = pygame.font.SysFont("ComicSans", 16)

class star:
    pc= 149.6e9*206265 #Definición de parsec
    G = 6.67428E-11 #Constante de gravitación universal
    S = 10/pc #pc por 10 pixeles
    T = 86400*365240 #segundos en un año
    def __init__(self, x, y, r, color, m, yvi=0, xcm=0, ycm=0):
        self.x = x*star.pc-xcm #Las entradas de la clase están en pc
        self.y = y*star.pc-ycm
        self.r = r
        self.color = color
        self.m = m*1.98892e30 #masas solares
        
        self.orbit = [] #Sin órbita
        self.sun = False #No hay sol inicialmente
        self.dis= 0 #Distancia
        
        self.xv = 0 #Velocidades iniciales
        self.yv = yvi
    
    def draw(self, win):
        x = self.x * self.S + w/2
        y = self.y * self.S + h/2 #Introducimos la escala y centramos
        if len(self.orbit)>2:
            actualiza= []
            for punto in self.orbit:
                x, y = punto
                x= x*self.S+w/2
                y= y*self.S+h/2
                actualiza.append((x, y))
            #pygame.draw.lines(win, self.color, False, actualiza, 2)
        #if not self.sun:
        #    dis_t= fuente.render(f'{round(self.dis, 1)} pc', 1, blanco)
        #    win.blit(dis_t, (x, y))
        
        pygame.draw.circle(win, self.color, (x, y), self.r) #Dibujamos el planeta
        
        
    def atraccion(self, o): #atracción entre cualquier cuerpo y nuestro cuerpo
        o_x, o_y= o.x, o.y
        dx = o_x - self.x
        dy = o_y - self.y
        d = np.sqrt(dx**2+dy**2)
        
        if o.sun:
            self.dis = d #distancia al sol 
        fuerza = (self.G * self.m * o.m)/ (d**2+5e3)
        ang = np.arctan2(dy, dx)
        fuerzax = np.cos(ang) * fuerza
        fuerzay = np.sin(ang) * fuerza
        return fuerzax, fuerzay
        
    def nuevapos(self, star, xcm, ycm):
        total_fx = total_fy = 0
        for orbital in star:
            if self == orbital:
                continue
            fx, fy = self.atraccion(orbital)
            total_fx += fx
            total_fy += fy
        self.xv += total_fx / self.m * self.T
        self.yv += total_fy / self.m * self.T
        
        self.x += self.xv * self.T-1*xcm
        self.y += self.yv * self.T-1*ycm
        self.orbit.append((self.x, self.y))



def main():
    #Empieza pygame
    run = True #Util para parar el programa
    clock = pygame.time.Clock() #Controlar frames del programa
    ViaLactea = star(-20, 0, 10, gris, 4.1e6, 100)
    ViaLactea.sun=True
    Andromeda = star(20, 0, 10, amarillo, 1.4e8, -100) #https://esahubble.org/images/heic0512a/
    #Andromeda.sun=True
    #775kpc
    estrellas = [ViaLactea, Andromeda]
    for i in range(10):
        estrellas.append(star(20+np.random.uniform(-2, 4),
                              np.random.uniform(-2, 2.5),
                              4, blanco, 1,
                              np.random.uniform(50000,130400)))
    for i in range(100):
        estrellas.append(star(-20+np.random.uniform(1, 4),
                              np.random.uniform(-1, 5),
                              4, blanco, 1,
                              np.random.uniform(50000,130400)))
    
    while run:
        xcm=(ViaLactea.m*ViaLactea.x+Andromeda.m*Andromeda.x)/(ViaLactea.m+Andromeda.m)
        ycm=(ViaLactea.m*ViaLactea.y+Andromeda.m*Andromeda.y)/(ViaLactea.m+Andromeda.m)
        clock.tick(60)
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        for p in estrellas:
            p.nuevapos(estrellas,xcm, ycm)
            p.draw(win)
        pygame.display.update() #Actualiza la pantalla
    pygame.quit()

main()
