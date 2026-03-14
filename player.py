import pygame

class Player:

    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.isAlive = True

    def move(self, direction):
        if (direction == 0):
            pass
        if (direction == 1):
            self.y -= self.speed
        if (direction == 2):
            self.y += self.speed
        if (direction == 3):
            self.x -= self.speed
        if (direction == 4):
            self.x += self.speed

    def kill(self):
        self.isAlive = False

    def revive(self): 
        self.isAlive = True
    
    def get_pos(self):
        return (self.x, self.y)