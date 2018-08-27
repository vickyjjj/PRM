
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
        self.add_vertex(self.start)
        self.add_vertex(self.end)

    def add_obstacle(self, obst):
        """
        Add obstacle to world if obs does not collide with any
        already-placed obstacles.
        """
        for placed_obs in self.obstacles:
            if obst.collides(placed_obs):
                return False
        self.obstacles.append(obst)
        return True
    
    def add_vertex(self, vert):
        if vert not in self.test_points:
            for obst in self.obstacles:
                if vert.collides(obst):
                    return False
        else:
            return False
        self.test_points.add(vert)
        return True

##    def add_connection(self, conn): # fix
##        pass
##
##    def search_paths(self): # fix
##        pass

class Vertex():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_vertices(self):
        return (self.x, self.y)

    def collides(self, obst):
        if (self.x >= obst.left and
            self.x <= obst.right and
            self.y >= obst.bottom and
            self.y <= obst.top):
            return True
        return False

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
        if (obst.left > self.right or
            self.left > obst.right or
            obst.bottom > self.top or
            self.bottom > obst.top):
            return False
        return True

class Connection():

    def __init__(self, start, end):
        self.start = start
        self.end = end

class Tester():

    def __init__(self, width, height):
        # initialize world
        self.world = World(width, height)
        # make plot interactive - i.e. updates as we go along
        plt.ion()

        # initialize obstacles
        # fix: obstacles should be chosen by user
        self.world.add_obstacle(Rectangle(width*1/5, width*2/5, 0, height*2/3))
        self.world.add_obstacle(Rectangle(width*3/5, width*4/5, height*1/3, height))
        
        # plot obstacles
        plt.axis([0, self.world.width, 0, self.world.height])
        for obs in self.world.obstacles:
            rect = patches.Rectangle((obs.left, obs.bottom), obs.right-obs.left, obs.top-obs.bottom)
            plt.gca().add_patch(rect)
        plt.draw()
        
    def initialization(self):
        # initialize path travel mission 
        # fix: should be chosen by user
        start = Vertex(1, 1)
        end = Vertex(self.world.width-1, self.world.height-1)
        self.world.init_mission(start, end)

        # plot init and goal points
        plt.plot([start.x, end.x], [start.y, end.y], 'ro')
        plt.gca().annotate("init", start.get_vertices())
        plt.gca().annotate("goal", end.get_vertices())
        plt.draw()

    def sample(self):
        # sample vertices
        for i in range(100):
            xval = random.randint(0, self.world.width)
            yval = random.randint(0, self.world.height)
            v = Vertex(xval, yval)
            if self.world.add_vertex(v):
                plt.plot([xval],[yval], 'ko')
                plt.draw()
                plt.pause(0.05)

##    def connect(self):
##        pass
##
##    def search(self):
##        return self.world.search_paths()

test = Tester(50, 30)
input("Hit enter to continue.")
test.initialization()
input("Hit enter to continue.")
test.sample()
print("Finished.")
plt.waitforbuttonpress()
