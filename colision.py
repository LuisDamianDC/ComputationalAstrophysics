# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:06:02 2024

@author: Herma
"""

import pygame
import sys
import random
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clase para representar una pelota
class Ball:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]

# Función para detectar colisiones entre dos pelotas
def check_collision(ball1, ball2):
    distance = math.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)
    if distance <= ball1.radius + ball2.radius:
        return True
    return False

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colisión de pelotas")
clock = pygame.time.Clock()

# Crear las pelotas
ball1 = Ball(100, 300, 30, RED, [3, 0])
ball2 = Ball(700, 300, 30, WHITE, [-3, 0])

# Bucle principal
while True:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento de las pelotas
    ball1.move()
    ball2.move()

    # Comprobar colisión
    if check_collision(ball1, ball2):
        ball1.velocity[0] *= -1
        ball1.velocity[1] *= -1
        ball2.velocity[0] *= -1
        ball2.velocity[1] *= -1

    # Dibujar las pelotas
    ball1.draw(screen)
    ball2.draw(screen)

    pygame.display.flip()
    clock.tick(60)
