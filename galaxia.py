# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 21:19:16 2024

@author: LuisDamian
"""

import pygame
import numpy as np
pygame.init()

w, h= 1000, 700
win=pygame.display.set_mode((w, h))
pygame.display.set_caption("Simulador orbital del Sagitario A*")
#Colores de las estrellas
amarillo = (255, 255, 0)
agujero = (80, 78, 81)
blanco= (255, 255, 255)
fuente = pygame.font.SysFont("ComicSans", 16)


class star:
    pc= 149.6e9*206265 #Definición de parsec
    G = 6.67428E-11 #Constante de gravitación universal
    S = 200/pc #UA por 100 pixeles
    T = 86400*36524 #segundos en un año
    def __init__(self, x, y, r, color, m, yvi=0):
        self.x = x*star.pc #Las entradas de la clase están en pc
        self.y = y*star.pc
        self.r = r
        self.color = color
        self.m = m
        
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
            pygame.draw.lines(win, self.color, False, actualiza, 2)
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
        fuerza = (self.G * self.m * o.m)/ (d**2)
        ang = np.arctan2(dy, dx)
        fuerzax = np.cos(ang) * fuerza
        fuerzay = np.sin(ang) * fuerza
        return fuerzax, fuerzay
        
    def nuevapos(self, star):
        total_fx = total_fy = 0
        for orbital in star:
            if self == orbital:
                continue
            fx, fy = self.atraccion(orbital)
            total_fx += fx
            total_fy += fy
        self.xv += total_fx / self.m * self.T
        self.yv += total_fy / self.m * self.T
        
        self.x += self.xv * self.T
        self.y += self.yv * self.T
        self.orbit.append((self.x, self.y))


def main():
    run = True #Util para parar el programa
    clock = pygame.time.Clock() #Controlar frames del programa
    sagitarioa = star(0, 0, 30, agujero, 4.1e6*1.98892e30) #Sagitario A*
    sagitarioa.sun = True
    sol = star(1, 0, 8, amarillo, 1.98892e30, 110400) #Pelotita de la masa del sol
    #Orbita estable en 110400
    
    estrellas = [sol, sagitarioa]
    for i in range(25):
        estrellas.append(star(np.random.uniform(0.5, 2),
                              np.random.uniform(0, 0.5),
                              4, blanco, 1.98892e3, 
                              np.random.uniform(50000,130400)))
    for i in range(25):
        estrellas.append(star(np.random.uniform(-2, -0.5),
                              np.random.uniform(0, 0.5),
                              4, blanco, 1.98892e3, 
                              np.random.uniform(50000,130400)))    
    
    
    while run:
        clock.tick(60)
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        for s in estrellas:
            s.nuevapos(estrellas)
            s.draw(win)
        pygame.display.update() #Actualiza la pantalla
    pygame.quit()

main()
