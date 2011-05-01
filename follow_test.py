#!/usr/bin/env python
# A simple follow test.
# TODO: Try threading instead of multiprocessing

import multiprocessing
import sys
import time
import pygame

pygame.init()

class Rects(object):
    """Main."""

    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.go_home = False

    def get_image(self):
        return self.image

    def get_rect(self):
        return self.rect

    def set_home_status(self, value):
        self.go_home = bool(value)

    def get_home_status(self):
        return self.go_home

def game():
    """Main game function."""

    home = Rects('home.gif')
    ant_one = Rects('ant.gif')
    ant_two = Rects('ant.gif')
    food = Rects('food.gif')

    home_image = home.get_image()
    home_rect = home.get_rect()
    ant_one_image = ant_one.get_image()
    ant_one_rect = ant_one.get_rect()
    ant_two_image = ant_two.get_image()
    ant_two_rect = ant_two.get_rect()
    food_image = food.get_image()
    food_rect = food.get_rect()

    width = 640
    height = 480
    size = width, height
    black = 0, 0, 0

    screen  = pygame.display.set_mode(size)

    home_rect = home_rect.move(100, 100)
    ant_one_rect = ant_one_rect.move(250, 250)
    ant_two_rect = ant_two_rect.move(350, 350)
    food_rect = food_rect.move(500, 500)
    
    home_center = home_rect.center
    food_center = food_rect.center

    in_rect = False

    parent_conn, child_conn = multiprocessing.Pipe()
    first_ant = multiprocessing.Process(target=a_one, args=(child_conn,
                                                            ant_one,
                                                            ant_one_rect,
                                                            home_rect,
                                                            food_rect,))

    first_ant.daemon = True
    first_ant.start()

    parent_conn_2, child_conn_2 = multiprocessing.Pipe()
    second_ant = multiprocessing.Process(target=a_two, args=(child_conn_2,
                                                             ant_two,
                                                             ant_two_rect,
                                                             home_rect,
                                                             food_rect,))
    second_ant.daemon = True
    second_ant.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        ant_one_rect = ant_one_rect.move(parent_conn.recv())
        ant_two_rect = ant_two_rect.move(parent_conn_2.recv())

        screen.fill(black)
        screen.blit(home_image, home_rect)
        screen.blit(ant_one_image, ant_one_rect)
        screen.blit(ant_two_image, ant_two_rect)
        screen.blit(food_image, food_rect)
        pygame.display.flip()

def a_one(main, ant_one, ant_one_rect, home_rect, food_rect):
    """separate process for first ant."""
    while True:
        if ant_one.get_home_status():
            ant_one_rect = ant_one_rect.move([-1, -1])
            main.send([-1, -1])
        else:
            ant_one_rect = ant_one_rect.move([1, 1])
            main.send([1, 1])

        if ant_one_rect.colliderect(home_rect) and not in_rect:
            ant_one.set_home_status(not ant_one.get_home_status())
            in_rect = True
            time.sleep(3)

        if not (ant_one_rect.colliderect(home_rect) or ant_one_rect.colliderect(food_rect)):
            in_rect = False

        if ant_one_rect.colliderect(food_rect) and not in_rect:
            ant_one.set_home_status(not ant_one.get_home_status())
            in_rect = True
            time.sleep(5)

def a_two(main, ant_one, ant_one_rect, home_rect, food_rect):
    """separate process for first ant."""
    while True:
        if ant_one.get_home_status():
            ant_one_rect = ant_one_rect.move([-1, -1])
            main.send([-1, -1])
        else:
            ant_one_rect = ant_one_rect.move([1, 1])
            main.send([1, 1])

        if ant_one_rect.colliderect(home_rect) and not in_rect:
            ant_one.set_home_status(not ant_one.get_home_status())
            in_rect = True
            time.sleep(3)

        if not (ant_one_rect.colliderect(home_rect) or ant_one_rect.colliderect(food_rect)):
            in_rect = False

        if ant_one_rect.colliderect(food_rect) and not in_rect:
            ant_one.set_home_status(not ant_one.get_home_status())
            in_rect = True
            time.sleep(5)

if __name__=='__main__':
    game()
