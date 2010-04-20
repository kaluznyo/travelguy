import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_SPACE, K_ESCAPE
import sys
import time
from math import sqrt
from random import choice
from random import random

from copy import deepcopy


try:
    import psyco
    psyco.full()
except ImportError:
    print "No Psyco"

def ga_solve(file=None, gui=True, maxtime=0):
    selector = Selector()
    if file==None:
        listeVilles = selector.collecting()
    else:
        listeVilles = loadCities(file)
    listToDraw = map(lambda x: [int(x[1]),int(x[2])],listeVilles)
    selector.draw(listToDraw)
    #print listToDraw
    prob = Probleme()
    prob.createProbleme(listeVilles)
    pop = Population(prob.findSolutions(20))
    for p in pop.listIndividu:
        print p
    print "Before Mutation .."
    i=0
    while i<10:
        pop.crossPopulation()
        pop.muteAllPopulation(1)
        pop.calculateAllDistance()
        pop.selectPopulation()
        print pop.listIndividu[0].totalDistance
        if gui:
            selector.drawSolution(pop.listIndividu[0].solution)
        i=i+1

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
		#pygame.draw.lines(self.screen,self.city_color,True,self.cities)

    def drawSolution(self,solution):
        position = map(lambda x: x.getPosition(),solution)
        self.draw(self.cities)
        pygame.draw.lines(self.screen,self.city_color,True,position)
        pygame.display.flip()
        time.sleep(3)

        

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
        
#--------
#LOGIC
class City:
    
    def __init__(self,name,x,y):
        self.x = x
        self.y = y
        self.name = name
   
    def __str__(self):
        return "Name :" + self.name + " X: " + str(self.x) + " Y: " + str(self.y)
        
    #Calcule la distance entre deux villes   
    def distance(self,city):
        deltaX = self.x-city.x
        deltaY = self.y-city.y
        #Maybe sqrt is useless
        return sqrt((deltaX**2)+(deltaY**2))
        
    def __eq__(self,other):
        return other.name == self.name
    
    def getPosition(self):
        return [self.x,self.y]
    

        
class Probleme:
    def __init__(self):
        self.cities = []
        self.citiesToVisit = []

    def getNumberCity(self):
        return len(self.cities)
        
    #Recupere les informations a partir d'une ligne d'un fichier data
    def getInformations(self,elt):
        name = elt[0]
        x = int(elt[1])
        y = int(elt[2])
        return City(name,x,y)
    
    #Creer la liste de ville a partir de tout le tableau, recuperer d'un fichier data
    def createProbleme(self,listCities):
        self.cities = [self.getInformations(l) for l in listCities]
    
    def __str__(self):
        for c in self.cities:
            print c
            
    #Cherche la distance la plus petite entre city et les villes de cititesToVisit
    def searchSmallerDistance(self,city,citiesToVisit):
        dist = float('10000000000')
        for c in citiesToVisit:
            distTmp = city.distance(c)
            if distTmp<dist:
                dist = distTmp
                citiyTmp = c
        return citiyTmp,dist
            
    #Cherche une solution en partant d'un point au hasard
    def findSolutionByRandom(self):
        solution = []
        totalDistance = 0
        self.citiesToVisit = deepcopy(self.cities)

        nextCity = choice(self.citiesToVisit)
        solution.append(nextCity)
        self.citiesToVisit.remove(nextCity)
        
        while self.citiesToVisit:
            nextCity, dist = self.searchSmallerDistance(nextCity,deepcopy(self.citiesToVisit))
            totalDistance = totalDistance + dist
            solution.append(nextCity)
            self.citiesToVisit.remove(nextCity)
            
        #On rajoute le dernier lien entre la premiere et dernire ville
        totalDistance = totalDistance + nextCity.distance(solution[0])
        return solution, totalDistance
    
    def findSolutions(self,nbSolution):
        listSolution = []
        while nbSolution>0:
            solution, dist = self.findSolutionByRandom()
            listSolution.append(Solution(solution,dist))
            nbSolution = nbSolution - 1
        return listSolution
            
        
        
class Solution:
    def __init__(self, solution,totalDistance=0):
        self.solution = solution
        self.totalDistance = totalDistance
    
    def __repr__(self):
        return repr((self.solution, self.totalDistance))
        
    def __str__(self):
        for c in self.solution:
            print c
        return str(self.totalDistance)
    

    def mutate(self):
        #choice marche pas ... pk ?...
        index =  int(random() * len(self.solution))
        index2 =  int(random() * len(self.solution))   
        cityToMove = self.solution[index]
        cityToMove2 = self.solution[index2]
       
        self.solution[int(index)] = cityToMove2
        self.solution[int(index2)] = cityToMove
    
    def mutateSolution(self,nbMutation):
        #improve. range...
        #TODO recalculate distance..
        while nbMutation>0:
            self.mutate()
            nbMutation = nbMutation - 1
    #define len, getitem
    
    def calculateTotalDistance(self):
        i=0
        while i<len(self.solution)-1:
            self.totalDistance=self.totalDistance+self.solution[i].distance(self.solution[i+1])
            i=i+1
        #Ajout du premier jusque a la fin
        self.totalDistance=self.totalDistance+self.solution[0].distance(self.solution[len(self.solution)-1])

        
        
        
        
        
class Population:
    def __init__(self,listSolution):
        self.listIndividu = listSolution
        
    def muteAllPopulation(self,nbMutation):
        for p in self.listIndividu:
            p.mutateSolution(nbMutation)
        
    def crossPopulation(self):
        i=0
        newList = []
        while i<len(self.listIndividu):
            parent1 = self.listIndividu[i]
            if(i+1==len(self.listIndividu)):
                parent2 = self.listIndividu[0]
            else:
                parent2 = self.listIndividu[i+1]
            nbCity = len(self.listIndividu[i].solution)
            for dumb in xrange(2):
                j=0
                new = []       
                new.append(choice(self.listIndividu[i].solution))              
                while j<nbCity-1:
                    distParent1 = new[len(new)-1].distance(parent1.solution[j])
                    distParent2 = new[len(new)-1].distance(parent2.solution[j])
                    if distParent1<distParent2 and (parent1.solution[j] not in new):
                        new.append(parent1.solution[j])
                    elif distParent1>distParent2 and (parent2.solution[j] not in new):
                        new.append(parent2.solution[j])
                    else:
                        tmp = choice(self.listIndividu[i].solution)
                        while (tmp  in new):
                            tmp = choice(self.listIndividu[i].solution)
                            #print tmp
                            #print "---------"
                            #for h in self.listIndividu[i].solution:
                             #   print h
                        new.append(tmp)
                    j = j + 1
                newList.append(Solution(new))            
            i=i+1
        self.listIndividu = []
        self.listIndividu = newList
            
    def selectPopulation(self):
        self.listIndividu = sorted(self.listIndividu, key=lambda sol: sol.totalDistance)   
        self.listIndividu = self.listIndividu[:(len(self.listIndividu))/2]
        # middle = len(self.listIndividu)%3
        #  tmpList = self.listIndividu[:middle]
        #  for dump in xrange(len(self.listIndividu)/2-middle):
        #      tmpList.append(choice(self.listIndividu[middle:]))
        #  self.listIndividu = tmpList
        print "------"
        for e in self.listIndividu:
            print e.totalDistance
        print "------"
        
        
        
        
    def calculateAllDistance(self):
        for e in self.listIndividu:
             e.calculateTotalDistance()
        

        
def loadCities(filename):
    data = open(filename,'r')
    return [l.split() for l in data]
    

            

if __name__ == "__main__":
    #main
    if len(sys.argv)>1:
        ga_solve(sys.argv[1])
    else:
        ga_solve()

    
        
    #TODO Refaire crossPopulation pour tenir compte de la distance (voir PDF prof)
    #TODO methode pour recalculer tout le parcoure
    #TODO selection
    #TODO GUI
    #TODO methode crossPopulation totalement bidouille....
    
        

