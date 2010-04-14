from __future__ import with_statement
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_SPACE, K_ESCAPE
import sys
from math import sqrt

try:
    import psyco
    psyco.full()
except ImportError:
    pass

def ga_solve(file=None, gui=True, maxtime=0):
    if file==None:
        selector = Selector()
        listeVilles = selector.collecting()
    else:
        listeVilles = loadCities(file)
    print listeVilles



class Selector:
    def __init__(self):
        self.screen_x = 500
        self.screen_y = 500
        self.city_color = [10,10,200] # blue
        self.city_radius = 3
        self.font_color = [255,255,255] # white
        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('Selector')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None,30)
        self.cities = []
        self.draw(self.cities)

    def draw(self,positions):
		self.screen.fill(0)
		for pos in positions:
			pygame.draw.circle(self.screen,self.city_color,pos,self.city_radius)
		text = self.font.render("Nombre: %i" % len(positions), True, self.font_color)
		textRect = text.get_rect()
		self.screen.blit(text, textRect)
		pygame.display.flip()

    def collecting(self):
        collection = []
        i=0
        self.collecting = True
        while self.collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    self.collecting = False
                elif event.type == MOUSEBUTTONDOWN:
			         self.cities.append(pygame.mouse.get_pos())
			         collection.append(['v'+str(i),self.cities[i][0],self.cities[i][1]])
			         i = i+1
			         self.draw(self.cities)
        return collection
        

class City:
    
    def __init__(self,name,x,y):
        self.x = x
        self.y = y
        self.name = name
   
    def __str__(self):
        return self.name + " " + str(self.x) + " " + str(self.y)
        
    def distance(self,city):
        deltaX=abs(self.x-city.x)
        deltaY=abs(self.y-city.y)
        return sqrt((deltaX**2)+(deltaY**2))

        
class Probleme:
    def __init__(self,listCities):
        self.cities = listCities
        
    def getNumberCity(self):
        return len(self.cities)
        
    def __str__(self):
        for c in self.cities:
            print c
class Solution:
    def __init__(self, probleme):
        self.probleme = probleme
        
class Population:
    def __init__(self,listSolution):
        self.listIndividu = listSolution
        
def loadCities(filename):
    data = open(filename,'r')
    return [l.split() for l in data]
    
def createProbleme(listCities):  
    c = []
    for element in listCities:
        name = element[0]
        x = int(element[1])
        y = int(element[2])
        c.append(City(name,x,y))
    return Probleme(c)
            

if __name__ == "__main__":
    #main
    ga_solve()

