import argparse
import time
import random
import math
import sys

import pygame
from pygame.locals import *

window_x = 999
window_y = 999
acceleration_factor = 99
amount_of_planets = 22

parser = argparse.ArgumentParser()
parser.add_argument("-wx","--window-x", help="x dimension of display", type=int, default=window_x)
parser.add_argument("-wy","--window-y", help="y dimension of display", type=int, default=window_y)
parser.add_argument("-p","--planet-amount", help="amount of planets",type=int,default=amount_of_planets)
parser.add_argument("-ac","--acceleration-factor", help="multiplied effect of gravity on speed", type=int,default=acceleration_factor)
args = parser.parse_args()

window_x = args.window_x
window_y = args.window_y
acceleration_factor = args.acceleration_factor
amount_of_planets = args.planet_amount


PLANET_OPTIONS = ["moon.png", "earth.png", "sun.jpg"]
pygame.init()
Surface = pygame.display.set_mode((window_x, window_y))
planets_list = []


class Particle:
    def __init__(self, x=None, y=None):
        if x is not None:
            self.x = x
        else:
            self.x = random.randint(10, window_x)
        if y != None:
            self.y = window_y - y
        else:
            self.y = random.randint(10, window_y)
        self.speedx = random.random() - 0.5
        self.speedy = random.random() - 0.5
        self.mass = random.randint(2, 20)
        self.radius = math.sqrt(self.mass)
        self.file = random.choice(PLANET_OPTIONS)
        self.last_move = time.time()


for x in range(amount_of_planets):
    planets_list.append(Particle())


def move():
    for P in planets_list:
        for P2 in planets_list:
            if P != P2:
                XDiff = P.x - P2.x
                YDiff = P.y - P2.y
                distance = math.sqrt((XDiff ** 2) + (YDiff ** 2))
                if distance < 10:
                    distance = 10
                # F = (G*M*M)/(R**2)
                # F = M*A  ->  A = F/M
                # A = (G*M)/(R**2)
                acceleration = 0.125 * P2.mass / (distance ** 3)
                P.speedx -= acceleration * XDiff * acceleration_factor
                P.speedy -= acceleration * YDiff * acceleration_factor
    for P in planets_list:
        now = time.time()
        time_since_last_move = now - P.last_move
        P.x += P.speedx * time_since_last_move
        P.y += P.speedy * time_since_last_move
        P.last_move = now


def edge_bounce(planet):
    if planet.x > window_x - planet.radius:
        planet.x = window_x - planet.radius
        planet.speedx *= -1
    if planet.x < 0 + planet.radius:
        planet.x = 0 + planet.radius
        planet.speedx *= -1
    if planet.y > window_y - planet.radius:
        planet.y = window_y - planet.radius
        planet.speedy *= -1
    if planet.y < 0 + planet.radius:
        planet.y = 0 + planet.radius
        planet.speedy *= -1


def collision_detect():
    for P in planets_list:
        edge_bounce(P)
        for P2 in planets_list:
            if P != P2:
                distance_between_points = math.sqrt(((P.x - P2.x) ** 2) + ((P.y - P2.y) ** 2))
                if distance_between_points < (P.radius + P2.radius):
                    P.speedx = ((P.mass * P.speedx) + (P2.mass * P2.speedx)) / (P.mass + P2.mass)
                    P.speedy = ((P.mass * P.speedy) + (P2.mass * P2.speedy)) / (P.mass + P2.mass)

                    # 2 become 1
                    # precise new location
                    P.x = ((P.mass * P.x) + (P2.mass * P2.x)) / (P.mass + P2.mass)
                    P.y = ((P.mass * P.y) + (P2.mass * P2.y)) / (P.mass + P2.mass)

                    # 2 become 1
                    P.mass += P2.mass  # new mass
                    P.radius = math.sqrt(P.mass)  # new radius
                    planets_list.remove(P2)  # only one star survives


def draw():
    Surface.fill((0, 0, 0))
    for P in planets_list:
        my_image = pygame.image.load(P.file)
        scale_image = pygame.transform.scale(my_image, (int(2 * P.radius), int(2 * P.radius)))
        Surface.blit(scale_image, (int(P.x - P.radius), int(window_y - P.radius - P.y)))
    pygame.display.flip()


def GetInput():
    key_stete = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or key_stete[K_ESCAPE]:
            pygame.quit()
            sys.exit()


def main():
    print("click screen to create more planets")
    while True:
        GetInput()
        move()
        collision_detect()
        draw()
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONUP:
            print("created planet at (%d, %d)" % event.pos)
            planets_list.append(Particle(event.pos[0], event.pos[1]))


if __name__ == '__main__':
    main()
