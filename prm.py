
"""
Probabilistic RoadMap (PRM) Method
Victoria Juan
April 2018
"""

# Imports
import math
import random
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class World():

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.obstacles = []
        self.test_points = set()
 #       self.occupied_vertices = set() # fix: can sets hold custom types?
        self.connections = []

    def init_mission(self, start, end):
        self.start = start 
        self.end = end
        self.add_vertex(self.start.get_vertices())
        self.add_vertex(self.end.get_vertices())

    def add_obstacle(self, obs):
        """
        Add obstacle to world if obs does not collide with any
        already-placed obstacles.
        """
        for placed_obs in self.obstacles:
            if obs.collides(placed_obs):
                return False
        self.obstacles.append(obs)
        return True
    
##    def add_vertex(self, vert):
##        if is_collision_free(vert):
##            self.test_points.update(vert)
##
##    def add_connection(self, conn): # fix
##        pass
##
##    def search_paths(self): # fix
##        pass
##
##    # helper functions
##    
##    def is_collision_free(item):
##        for vertex in item.get_vertices(): # needs vertex in (x,y) tuples
##            if vertex in self.obstacles:
##                return False
##        return True

class Vertex():

    def __init__(self, x, y):
        self.x = x
        self.y = y

##    def get_vertices(self):
##        return (self.x, self.y)

class Obstacle():

    def __init__(self, l, r, b, t):
        self.left = l
        self.right = r
        self.top = t
        self.bottom = b
 #       self.all_vertices = create_vertices()

##    def get_vertices(self):
##        """
##        Returns array of vertices in tuple format
##        """
##        return_list = []
##        for vertex in self.all_vertices:
##            return_list.append(vertex.get_vertices())
##        return return_list

    # helper functions
##    @abstractmethod
##    def create_vertices():
##        """
##        Returns array of Vertex class vertices within obstacle boundaries
##        """

    @abstractmethod
    def collides(self, obs):
        """
        Returns boolean based on obstacle collision
        """

class Rectangle(Obstacle):

    def __init__(self, l, r, b, t):
        # fix: throw exception if l/r and b/t do not match position
        super().__init__(l, r, b, t)

    # helper functions
##    def create_vertices():
##        """
##        Returns array of Vertex class vertices within rectangular boundaries
##        """
##        return_list = []
##        for x in range(self.left, self.right):
##            for y in range(self.bottom, self.top):
##                return_list.append(Vertex(x,y))
##        return return_list

    def collides(self, obst):
        """
        Returns boolean based on obstacle collision.
        For a rectangle, doesn't collide if:
         - one rectangle is left of other rectangle
         - one rectangle is above other rectangle
        """
        if ((obst.left > self.right) |
            (self.left > obst.right) |
            (obst.bottom > self.top) |
            (self.bottom > obst.top)):
            return False
        return True

class Connection():

    def __init__(self, start, end):
        self.start = start
        self.end = end

class Tester():

    def __init__(self, width, height):
        self.world = World(width, height)
        
        # fix: obstacles should be chosen by user
        self.world.add_obstacle(Rectangle(width*1/5, width*2/5, 0, height*2/3))
        self.world.add_obstacle(Rectangle(width*3/5, width*4/5, height*1/3, height))

        self.plot(self.world)

    def plot(self, world):
        plt.axis([0, world.width, 0, world.height])
        for obs in world.obstacles:
            rect = patches.Rectangle((obs.left, obs.bottom), obs.right-obs.left, obs.top-obs.bottom)
            plt.gca().add_patch(rect)
        plt.show()

##        # fix: should be chosen by user
##        start = Vertex(1, 1)
##        end = Vertex(width - 2, height - 2)
##        self.world.init_mission(start, end)

##    def sample(self):
##        for i in 100:
##            v = Vertex(random.randint(0, self.world.width), random.randint(0, self.world.height)) 
##            self.world.add_vertex(v)
##
##    def connect(self):
##        pass
##
##    def search(self):
##        return self.world.search_paths()

test = Tester(50, 30)
