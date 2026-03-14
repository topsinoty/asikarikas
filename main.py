# Example file showing a circle moving on screen | example taken from https://www.pygame.org/docs/
import pygame
from direction import Direction
from player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player = Player(0, 0)
player_pos = player.get_pos()
Direction = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        Direction = 1
    if keys[pygame.K_s]:
        Direction = 2
    if keys[pygame.K_a]:
        Direction = 3
    if keys[pygame.K_d]:
        Direction = 4

    player.move(Direction)    
    player_pos = player.get_pos()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limts FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
