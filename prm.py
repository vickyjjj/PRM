
"""
Probabilistic RoadMap (PRM) Method
Victoria Juan
April 2018
"""

# Imports
import math
import random

class World():

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.occupied_vertices = set() # fix: can sets hold custom types?
        self.connections = []

    def init_mission(self, start, end):
        self.start = start 
        self.end = end
        self.add_vertex(self.start.get_vertices())
        self.add_vertex(self.end.get_vertices())

    def add_obstacle(self, obs):
        if is_collision_free(obs):
            self.occupied_vertices.update(obs.get_vertices())

    def add_vertex(self, vert):
        if is_collision_free(vert):
            self.occupied_vertices.update(vert)

    def add_connection(self, conn): # fix
        pass

    def search_paths(self): # fix
        pass

    # helper functions
    
    def is_collision_free(item):
        for vertex in item.get_vertices(): # needs vertex in (x,y) tuples
            if vertex in self.occupied_vertices:
                return False
        return True

class Vertex():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_vertices(self):
        return [(self.x, self.y)]

class Obstacle():

    def __init__(self, l, r, b, t):
        self.left = l
        self.right = r
        self.t = top
        self.b = bottom
        self.all_vertices = create_vertices()

    def get_vertices(self): 
        return_list = []
        for vertex in self.all_vertices:
            return_list.append(vertex.get_vertices())
        return return_list

    # helper functions
    def create_vertices(): # fix: rectangular only 
        return_list = []
        for x in range(self.left+1, self.right+1):
            for y in range(self.bottom+1, self.top+1):
                return_list.append(Vertex(x,y))
        return return_list

class Connection():

    def __init__(self, start, end):
        self.start = start
        self.end = end

class Tester():

    def __init__(self, width, height):
        self.world = World(width, height)
        start = Vertex(1, 1) # fix: should be chosen by user
        end = Vertex(width - 2, height - 2)
        self.world.init_mission(start, end)

        # fix: obstacles should be chosen by user
        self.world.add_obstacle(Obstacle(width*2/3, width-2, 1, height/3))
        self.world.add_obstacle(Obstacle(1, width/3, height*2/3, height-2))

    def sample(self):
        for i in 100:
            v = Vertex(random.randint(0, self.world.width), random.randint(0, self.world.height)) 
            self.world.add_vertex(v)

    def connect(self):
        pass

    def search(self):
        return self.world.search_paths()
        
        
