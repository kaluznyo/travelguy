from __future__ import with_statement
import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_SPACE, K_ESCAPE
import sys
from math import sqrt
from random import choice
from copy import deepcopy


try:
    import psyco
    psyco.full()
except ImportError:
    print "No Psyco"

def ga_solve(file=None, gui=True, maxtime=0):
    if file==None:
        selector = Selector()
        listeVilles = selector.collecting()
    else:
        listeVilles = loadCities(file)
        listToDraw = []
        #Provisoire : pour faire une liste [[x,y],[x,y]...] pour le GUI
        for a in listeVilles:
            listTmp = []
            listTmp.append(int(a[1]))
            listTmp.append(int(a[2]))
            listToDraw.append(listTmp)
        print listToDraw
        selector = Selector(listToDraw)
        
    


class Selector:
    def __init__(self,cities):
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
        self.cities = cities
        self.draw(self.cities)
        

    def draw(self,positions):
		self.screen.fill(0)
		for pos in positions:
		    pygame.draw.circle(self.screen,self.city_color,pos,self.city_radius)
		text = self.font.render("Nombre: %i" % len(positions), True, self.font_color)
		textRect = text.get_rect()
		self.screen.blit(text, textRect)
		pygame.display.flip()
		pygame.draw.lines(self.screen,self.city_color,True,self.cities)
        

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
        return "Name :" + self.name + " X: " + str(self.x) + " Y: " + str(self.y)
        
    def distance(self,city):
        deltaX = self.x-city.x
        deltaY = self.y-city.y
        #Maybe sqrt is useless
        return sqrt((deltaX**2)+(deltaY**2))
    def __eq__(self,other):
        return other.name == self.name
    

        
class Probleme:
    def __init__(self):
        self.cities = []
        self.citiesToVisit = []
        self.solution = ""

    def getNumberCity(self):
        return len(self.cities)
        
    #Creer une liste de city
    def createProbleme(self,listCities):  
        for element in listCities:
            name = element[0]
            x = int(element[1])
            y = int(element[2])
            self.cities.append(City(name,x,y))
    
    def __str__(self):
        for c in self.cities:
            print c
    #cherche la distance la plus petite entre city et les villes de cititesToVisit
    def searchMinusDistance(self,city,citiesToVisit):
        dist = float('inf')    
        citiyTmp = None
        for c in citiesToVisit:
            distTmp = city.distance(c)
            if city.distance(c)<dist:
                dist = distTmp
                citiyTmp = c
        citiesToVisit.remove(c)
        return citiyTmp   
            
    #Cherche une solution en partant d'un point au hasard
    def findSolutionByRandom(self):
        self.citiesToVisit = self.cities
        nextCity = choice(self.citiesToVisit)
        self.citiesToVisit.remove(nextCity)
        self.solution += nextCity.name
        while not len(self.citiesToVisit)<=0:
            nextCity = self.searchMinusDistance(nextCity,deepcopy(self.citiesToVisit))
            self.citiesToVisit.remove(nextCity)
            self.solution += nextCity.name     
        
        
class Solution:
    def __init__(self, probleme):
        self.probleme = probleme
        
class Population:
    def __init__(self,listSolution):
        self.listIndividu = listSolution
        
def loadCities(filename):
    data = open(filename,'r')
    return [l.split() for l in data]
    

            

if __name__ == "__main__":
    #main
    #ga_solve(sys.argv[1])
    
    cities = loadCities(sys.argv[1])
    prob = Probleme()
    prob.createProbleme(cities)
    prob.findSolutionByRandom()
    print prob.solution
    

