from random import randint
from typing import Set
import pygame
import os
from math import *


class Settings(object):
    window_height = 800
    window_width = 500
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    title = "Raumschiff"
    small_size = (20, 20)
    medium_size = (40, 40)
    big_size = (80, 80)
    max_big = 5
    max_medium = 8
    max_small = 10

class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0

class Space_Ship(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = Settings.window_height / 2
        self.rotation = 0
        self.speed_x = 0
        self.speed_y = 0
    #Bewegen des Spielers
    def update(self):

        self.rect.move_ip((self.speed_x, self.speed_y))

        if self.rect.top >= Settings.window_height:
            self.rect.bottom = 1
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window_height
        if self.rect.left >= Settings.window_width:
            self.rect.right = 1
        if self.rect.right <= 0:
            self.rect.left = Settings.window_width

    def move(self):
        if round(self.speed_x - sin(radians(self.rotation)), 0) <= 10:
            if round(self.speed_x - sin(radians(self.rotation)), 0) >= -10:
                self.speed_x = round(self.speed_x - sin(radians(self.rotation)), 0)
        if round(self.speed_y - cos(radians(self.rotation)), 0) <= 10:  
            if round(self.speed_y - cos(radians(self.rotation)), 0) >= -10:   
                self.speed_y = round(self.speed_y - cos(radians(self.rotation)), 0)
    
    def rotate_right(self):
        if self.rotation == 0:
            self.rotation = 360
        self.rotation -= 22.5
        c = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = c
    
    def rotate_left(self):
        if self.rotation == 360:
            self.rotation = 0
        self.rotation += 22.5
        c = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = c

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, filename, size) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = self.image_orig
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.centerx = randint((size[0]//2), Settings.window_width - (size[0]//2))
        self.rect.centery = randint((size[1]//2), Settings.window_height - (size[1]//2))
        self.speed_x = randint(-1, 1)
        self.speed_y = randint(-1, 1)
    
    def update(self):
        self.rect.move_ip((self.speed_x, self.speed_y))

        if self.rect.top >= Settings.window_height:
            self.rect.bottom = 1
        if self.rect.bottom <= 0:
            self.rect.top = Settings.window_height
        if self.rect.left >= Settings.window_width:
            self.rect.right = 1
        if self.rect.right <= 0:
            self.rect.left = Settings.window_width
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.space_ships_group = pygame.sprite.Group()
        self.space_ship = Space_Ship('ship0.png')
        self.space_ships_group.add(self.space_ship)
        self.asteroid_small_group = pygame.sprite.Group()
        self.asteroid_medium_group = pygame.sprite.Group()
        self.asteroid_big_group = pygame.sprite.Group()
        self.small_timer = Timer(1000)
        self.medium_timer = Timer(2000)
        self.big_timer = Timer(3000)
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.obstecles()
            self.update()
            self.draw()
        pygame.quit()    

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_ESCAPE:   
                    self.running = False
                if event.key == pygame.K_RIGHT:         
                    self.space_ship.rotate_right()
                if event.key == pygame.K_LEFT:         
                    self.space_ship.rotate_left()
                if event.key == pygame.K_UP:         
                    self.space_ship.move()
            elif event.type == pygame.QUIT:         
                self.running = False   

    def spawn(self, group, image, size, max):
        if len(group) < max:
            self.asteroid = Asteroids(image, size)
            group.add(self.asteroid)
        self.information_asteroids = group.sprites()
        self.information_ships = self.space_ships_group.sprites()
        #keine Blasen sollen aufeinander spawnen
        if len(group) > 1:
            if (self.information_asteroids[len(group) - 1].rect.left - 10) < self.information_ships[len(self.space_ships_group) - 1].rect.right:
                if self.information_ships[len(self.space_ships_group) - 1].rect.left < (self.information_asteroids[len(group) - 1].rect.right + 10):
                    if (self.information_asteroids[len(group) - 1].rect.top - 10) < self.information_ships[len(self.space_ships_group) - 1].rect.bottom:
                        if self.information_ships[len(self.space_ships_group) - 1].rect.top < (self.information_asteroids[len(group) - 1].rect.bottom + 10):
                            group.remove(self.information_asteroids[len(group) - 1])   

    def obstecles(self):
        if self.big_timer.is_next_stop_reached():
            self.spawn(self.asteroid_big_group, "rock0.png", Settings.big_size, Settings.max_big)
        if self.medium_timer.is_next_stop_reached():
            self.spawn(self.asteroid_medium_group, "rock1.png", Settings.medium_size, Settings.max_medium)
        if self.small_timer.is_next_stop_reached():
            self.spawn(self.asteroid_small_group, "rock2.png", Settings.small_size, Settings.max_small)

    def update(self):
        self.space_ships_group.update()
        self.asteroid_big_group.update()
        self.asteroid_medium_group.update()
        self.asteroid_small_group.update()
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.space_ship.draw(self.screen)
        self.asteroid_big_group.draw(self.screen)
        self.asteroid_medium_group.draw(self.screen)
        self.asteroid_small_group.draw(self.screen)
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()