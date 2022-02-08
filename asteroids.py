from typing import Set
import pygame
import os
from random import randint 

#Ich besitze keinerlei Rechte an den, in diesem Programm, verwendeten Bildern.
#Mit den diesem Programm wird kein kommerzieller Gewinn erzielt.
#Die in diesem Programm verwendeten Bilder stammen von den vollgenden Internetseiten:
#'djungle_rain.png' stammt von https://www.umdiewelt.de/t4455_18 (www.umdiewelt.de)
#'dragonfly.png' stammt von https://miausmiles.com/2011/incredible-random-stuff/draw-something-every-day-035 (www.miausmiles.com)
#'drop.png' stammt von http://www.clipartpanda.com/clipart_images/domain-raindrop-clip-art-19285059 (www.clipartpanda.com)
#Ich bedanke mich bei den Contan Creatorn für ihre gute Arbeit

class Settings(object):
    window_height = 780
    window_width = 600
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    dragonfly_size = (50, 60) 
    title = "Liebelle im Regen"

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image_orig = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, Settings.dragonfly_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.centerx = Settings.window_width / 2          #Spielersprite wird plaziert in der Mitten des Bildschirms
        self.rect.bottom = Settings.window_height -10
        self.speed = 5
    #Bewegen des Spielers
    def watch_for_move(self):
        press = pygame.key.get_pressed()                       #registiert Tastendruck
        if press[pygame.K_UP]:
            self.rect.top -= self.speed
        if press[pygame.K_DOWN]:
            self.rect.top += self.speed
        if press[pygame.K_RIGHT]:
            self.rect.left += self.speed
        if press[pygame.K_LEFT]:
            self.rect.left -= self.speed
        #Wandkollision
        if self.rect.top <= 5:
            self.rect.top += 5
        if self.rect.bottom >= Settings.window_height -5:
            self.rect.top -= 5
        if self.rect.left <= 5:
            self.rect.left += 5                                
        if self.rect.right >= Settings.window_width -5:
            self.rect.right -= 5
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.dragonfly_group = pygame.sprite.Group()
        self.running = True
        self.counter = 0
        self.dragonflys = 0
        self.lives = 3
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.player()
            self.draw()
        pygame.quit()
        pygame.font.quit()      

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_ESCAPE:   
                    self.running = False
                if event.key == pygame.K_r:         
                    self.dragonfly_image = pygame.transform.rotate(self.dragonfly.image, 90)
            elif event.type == pygame.QUIT:         
                self.running = False

    def player(self):
        if self.dragonflys == 0 and self.lives > 0:           #falls der Spieler kollidiert und er noch Leben übrig hat
            self.dragonfly = Dragonfly('ship0.png')
            self.dragonfly_group.add(self.dragonfly)          #wird ein neuer Spieler erstellt
            self.dragonflys = 1                               #self.dragonflys ist 1 wenn der Spieler noch nicht collidiert ist
        else:
            pass
        self.dragonfly.watch_for_move()


        if self.dragonflys == 0: 
            self.drop_group.empty()      #wenn ein Spieler neu erscheinen muss werden werden alle Hindernisse entfernt
            #aktualisieren Hindernisspunktestand
            self.life_counter = self.font_counter.render('Remaining Lives: ' + str(self.lives), True, [255, 0, 0])
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.dragonfly.draw(self.screen)
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()