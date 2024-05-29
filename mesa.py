# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 04:23:16 2024

@author: Luis Damián Anaya Martínez
"""
##Llamado de librerías
import numpy as np
import pygame
import matplotlib.pyplot as plt
import math
# Inicializamos Pygame
pygame.init()

# Definimos constantes globales (de PyGame)
WIDTH, HEIGHT = 700, 700#1360,768               # Altura y Ancho de la ventana
WIN = pygame.display.set_mode((WIDTH,HEIGHT))   # Creamos el objeto ventana
CLOCK = pygame.time.Clock()                     # Creamos el reloj
FPS = 60                                        # Frames por segundo 
g= 0                                            # Gravedad (0)
e=0.05						# Correcciòn de las colisiones
#Donde guardaremos las distribuciones de velocidades
veli=[]
velf=[]

# Mi primer Objeto
class Ball():
    # Constructor del objeto
    def __init__(self, x, y, v_x, v_y):
        self.x      = x
        self.y      = y
        self.v_x    = v_x
        self.v_y    = v_y
        self.mass   = 10
        self.c_f    = 0         #Coeficiente de fricción 
        self.color  = (255,0,0)
        self.r      = 10
    
    # Mueve el objeto
    def move(self, pelotas, dt=0.01):
        if g!=0:
        	self.v_x += - (self.c_f*self.v_x)/(self.mass)*dt  
        	self.v_y += (-g*self.mass -self.c_f*self.v_y)/(self.mass)*dt 
        self.x   += self.v_x * dt 
        self.y   += self.v_y * dt
        # Choque con el suelo
        if self.y < self.r:
            self.v_y = -self.v_y
            self.y = self.r+0.01
        # Choque contra las paredes
        if self.x < self.r:
            self.v_x = - self.v_x
            self.x = self.r
        if self.x > WIDTH-self.r:
            self.v_x = - self.v_x
            self.x = WIDTH-self.r
        # Choque con el techo
        if self.y > HEIGHT-self.r:
            self.v_y = -self.v_y
            self.y = HEIGHT-self.r
            
    # Dibuja el objeto
    def draw(self, win=WIN):
        pygame.draw.circle(win,
                           self.color,
                           (self.x, HEIGHT-self.y),
                           self.r)

def collision(p1, p2):
    d = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    c1= 2 * p2.mass / (p1.mass + p2.mass)
    c2= 2 * p1.mass / (p1.mass + p2.mass)
    if d <= p1.r + p2.r:
        x1=np.array([p1.x, p1.y])
        x2=np.array([p2.x, p2.y])
        v1=np.array([p1.v_x, p1.v_y])
        v2=np.array([p2.v_x, p2.v_y])
        
        v1p= c1*((v1-v2).dot(x1-x2)/d**2)*(x1- x2)
        v2p= c2*((v2-v1).dot(x2-x1)/d**2)*(x2- x1)
        if d < p1.r + p2.r:
        	p1.x+=(p1.x - p2.x)*e
        	p1.y+=(p1.y - p2.y)*e
        	p2.x+=(p2.x - p1.x)*e
        	p2.y+=(p2.y - p1.y)*e
        p1.v_x -= v1p[0]
        p1.v_y -= v1p[1]
        
        p2.v_x -= v2p[0] 
        p2.v_y -= v2p[1]
        
        
def ploteo(pelotas, veli, velf, m):
    
    #'''
    fig, axs=plt.subplots(2,1)
    #axs[0].set_yscale('linear')
    axs[0].set_title("Antes")
    axs[0].hist(veli)
    plt.ylabel('Partículas')
    plt.xlabel('Velocidad')
    #axs[1].set_yscale('linear')
    axs[1].set_title("Después")
    axs[1].hist(velf,30)
    k_B = 1.380649e-23  # Boltzmann constant in J/K
    T = 300  # Temperature in Kelvin

    # Function to calculate Maxwell-Boltzmann distribution
    def maxwell_boltzmann(v, T):
        return (40 * np.pi * (v**2) * (m / (2 * np.pi * k_B * T))**(3/2) * np.exp(-m * (v**2) / (2 * k_B * T)))

    # Define range of velocities
    v = np.linspace(0, 100, 5)  # in m/s
    
    # Mass of particle (in kg)
    m = 1.67e20  # mass of a proton
    
    # Calculate Maxwell-Boltzmann distribution
    f_v = maxwell_boltzmann(v, T)
    
    # Plot
    axs[1].plot(v, f_v, label='Maxwell-Boltzmann Distribution')
    plt.legend()
    plt.grid(True)
    
    '''
    plt.plot(veli, 'r:')
    plt.plot(velf, 'b:')
    '''
    plt.ylabel('Partículas')
    plt.xlabel('Velocidad')
    plt.show
        
# Función Principal
def main():
    pygame.display.set_caption("Colisión de pelotas")
    # Condiciones iniciales
    dt = 0.1 # Time Step
    m = 200  # Número de particulas
    # Creamos las pelotas
    pelotas = []
    for i in range(m):
        pelotas.append(Ball(
            np.random.uniform(0, WIDTH),    # Pos X
            np.random.uniform(0, HEIGHT),   # Pos y
            np.random.uniform(-50,50),       # Vel x
            np.random.uniform(-50,50)        # Vel y
            ))
        #Va primer plot
    for pelota in pelotas:
        veli.append((pelota.v_x**2+pelota.v_y**2)**(1/2))
    
    # Ciclo de animación
    while True:
        # Salir del juego para que no se quede Zombie
        for event in pygame.event.get():
            # Si cerramos la ventana, cierra el juego
            if event.type == pygame.QUIT:
                for pelota in pelotas:
                    velf.append((pelota.v_x**2+pelota.v_y**2)**(1/2))
                ploteo(pelotas, veli, velf, m)
                return
            # Si apretamos escape, cierra el juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        # Hay que repintar el fondo cada frame
        WIN.fill((10,10,10)) # Rellenar de negro
        
        # Dibujamos las pelotas
        for pelota in pelotas:
            pelota.move(pelotas, dt)
            
            for pelote in pelotas:
                if pelota!=pelote:
                    collision(pelote, pelota)
            pelota.draw()
        pygame.display.update()
        CLOCK.tick(FPS)
        
if __name__=='__main__':
    main()    
    pygame.quit()
