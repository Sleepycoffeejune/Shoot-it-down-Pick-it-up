import pygame as pg
import random

class Trashes:
    def __init__(self):
        self.__trashes = []
        self.__upto = 5
        self.rset_trash()
    
    def all_trash(self):
        return self.__etrashes
    
    def reset_trash(self):
        self.__trashes = []
        for i in range(self.__upto):
            self.__trashes.append(Trash())

    def draw(self,screen,board):
        for f in self.__trashes:
            f.draw(screen,board)
        
class Trash:
    def __init__(self):
        pass
class Food:
    def __init__(self):
        self.__pos = None
        self.__randomstart()

    @property
    def pos(self):
        return self.__pos

    def __randomstart(self, nowallows=None):
        x = random.randint(0,600)
        y = random.randint(0,480)
        if nowallows != None:
            while (x,y) in nowallows:
                x = random.randint(0,600-1)
                y = random.randint(0,480-1)
        self.__pos = (x,y)

    def draw(self,screen,board):
        b = self.__pos
        pg
        pg.draw.rect(screen)