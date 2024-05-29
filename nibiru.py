# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 05:25:57 2024

@author: LuisDamian
"""


import pygame
import numpy as np
import matplotlib.pyplot as plt
#print('Instalación de REBOUND')
#!pip install rebound
import rebound
pygame.init()

w, h= 1000, 700
win=pygame.display.set_mode((w, h))
pygame.display.set_caption("Simulador de Nibiru")
#Colores de los planetas
blanco= (255, 255, 255)
amarillo = (255, 255, 0)
azul = (100, 149, 237)
rojo = (188, 39, 50)
gris = (80, 78, 81)
verde = (150, 255, 150)

fuente = pygame.font.SysFont("ComicSans", 16)


class planeta:
    UA= 149.6e9 #Definición de unidad astronómica
    G = 6.67428E-11 #Constante de gravitación universal
    S = 200/UA #UA por 100 pixeles
    T = 86400*1 #segundos en un día
    def __init__(self, x, y, r, color, m , yvi=0, xvi=0):
        self.x = x*planeta.UA #Las entradas de la clase están en UA
        self.y = y*planeta.UA
        self.r = r
        self.color = color
        self.m = m*1.98892e30
        
        self.orbit = [] #Sin órbita
        self.sun = False #No hay sol inicialmente
        self.dis= 0 #Distancia
        
        self.xv = xvi*planeta.UA/(planeta.T*365.24) #Velocidades iniciales
        self.yv = yvi*planeta.UA/(planeta.T*365.24)
    
    def draw(self, win):
        x = self.x * self.S + w/2
        y = self.y * self.S + h/2 #Introducimos la escala y centramos
        #Dibujado de las órbitas
        if len(self.orbit)>2:
            actualiza= []
            for punto in self.orbit:
                x, y = punto
                x= x*self.S+w/2
                y= y*self.S+h/2
                actualiza.append((x, y))
            pygame.draw.lines(win, self.color, False, actualiza, 2)
          
        if not self.sun:
            dis_t= fuente.render(f'{round(self.dis/1000, 1)} km', 1, blanco)
            win.blit(dis_t, (x, y))
        
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
    
    def nuevapos(self, planetas):
        total_fx = total_fy = 0
        for planeta in planetas:
            if self == planeta:
                continue
            fx, fy = self.atraccion(planeta)
            total_fx += fx
            total_fy += fy
        self.xv += total_fx / self.m * self.T
        self.yv += total_fy / self.m * self.T
        
        self.x += self.xv * self.T
        self.y += self.yv * self.T
        self.orbit.append((self.x, self.y))


def main():
    sim = rebound.Simulation()          # Comenzamos la simulación
    sim.units = ('AU', 'yr', 'Msun')    # Especificamos unidades
    sim.integrator = 'ias15'            # Integrador
    # Añadimos los objetos
    sim.add('Sun')
    sim.add('Mercury')
    sim.add('Venus')
    sim.add('Earth')
    sim.add('Mars')
    sim.add('Jupiter')
    sim.add('Saturn')
    sim.add('Uranus')
    sim.add('Neptune')
    # Nos movemos al centro de masa
    sim.move_to_com()
    # Visualizamos nuestros objetos
    fig= rebound.OrbitPlot(sim, color=True)
    #Empieza pygame
    run = True #Util para parar el programa
    clock = pygame.time.Clock() #Controlar frames del programa
    sol = planeta(0, 0, 30, amarillo, 1)
    sol.sun = True
    
    mercurio=planeta(sim.particles[1].x, sim.particles[1].y, 8, gris, sim.particles[1].m, sim.particles[1].vy, sim.particles[1].vx)
    venus=planeta(sim.particles[2].x, sim.particles[2].y, 15, verde, sim.particles[2].m, sim.particles[2].vy, sim.particles[2].vx)
    tierra=planeta(sim.particles[3].x, sim.particles[3].y, 16, azul, sim.particles[3].m, sim.particles[3].vy, sim.particles[3].vx)
    marte=planeta(sim.particles[4].x, sim.particles[4].y, 12, rojo, sim.particles[4].m, sim.particles[4].vy, sim.particles[4].vx)
    #jupiter=planeta(sim.particles[5].x, sim.particles[5].y, 15, verde, sim.particles[5].m, sim.particles[5].vy, sim.particles[5].vx)
    #saturno=planeta(sim.particles[6].x, sim.particles[6].y, 15, verde, sim.particles[6].m, sim.particles[6].vy, sim.particles[6].vx)
    #urano=planeta(sim.particles[7].x, sim.particles[7].y, 16, azul, sim.particles[7].m, sim.particles[7].vy, sim.particles[7].vx)
    #neptuno=planeta(sim.particles[8].x, sim.particles[8].y, 12, rojo, sim.particles[8].m, sim.particles[8].vy, sim.particles[8].vx)
    
    
    nibiru=planeta(10, 0,18,  blanco, 6e25, 343) #https://es.wikipedia.org/wiki/Planeta_Nueve
    planetas = [sol, mercurio, venus, tierra, marte, nibiru]
    '''  
    for i in sim.particles[1:8]:
        planetas.append(planeta(i.x, i.y, 8, gris, i.m, i.vy, i.vx))
    '''
    
    while run:
        clock.tick(60)
        win.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        for p in planetas:
            p.nuevapos(planetas)
            p.draw(win)
        pygame.display.update() #Actualiza la pantalla
    pygame.quit()

main()
