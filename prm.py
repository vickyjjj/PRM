
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
        self.connections = []

    def init_mission(self, start, end):
        self.start = start 
        self.end = end
        self.test_points.add(self.start)
        self.test_points.add(self.end)

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

    def add_connection(self, conn):
        vertical = False
        safe = True
        # fix: the following assignment was pretty random
        vert = conn.start
        curr_vert = conn.end
        try:
            slope = (vert.y-curr_vert.y)/(vert.x-curr_vert.x)
            intercept = vert.y-slope*vert.x
        except:
            vertical = True
        # iterate through obstacles
        for obst in self.obstacles:
            if vertical:
                if (vert.x <= obst.right and
                    vert.x >= obst.left):
                    # check y position is within obstacle too
                    safe = False
                    break
            else:
                # check left
                if ((obst.left <= vert.x and
                     obst.left >= curr_vert.x) or
                    (obst.left <= curr_vert.x and
                     obst.left >= vert.x)):
                    left = slope*obst.left+intercept
                    if (left <= obst.top and
                        left >= obst.bottom):
                        safe = False
                        break
                # check right
                if ((obst.right <= vert.x and
                     obst.right >= curr_vert.x) or
                    (obst.right <= curr_vert.x and
                     obst.right >= vert.x)):
                    right = slope*obst.right+intercept
                    if (right <= obst.top and
                        right >= obst.bottom):
                        safe = False
                        break
        if safe:
            # add to world's connections
            self.connections.append(conn)
            # add to vertice's connections
            conn.start.add_connection(conn.end)
            conn.end.add_connection(conn.start)
            return True
        return False

    def search_paths(self): # fix
        """
        BFS
        """
        # initialize queues
        queue = [] # order matters
        already_searched = set()
        queue.append([self.start])
        already_searched.add(self.start)

        # begin search
        while (len(queue) != 0):
            # get current vertex to look at m
            path = queue.pop(0)
            curr = path[-1]
            # get connecting vertices of this vertex
            for conn in curr.connections:
                # we have found the goal vertex
                if conn == self.end:
                    path.append(conn)
                    return path
                # add to queue to search if not already searched this vertex
                if conn not in already_searched:
                    newpath = []
                    for i in path:
                        newpath.append(i)
                    newpath.append(conn)
                    queue.append(newpath)
                    already_searched.add(conn)
        return None                  
            
class Vertex():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connections = set()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_vertices(self):
        return (self.x, self.y)

    def collides(self, obst):
        # bounding box check
        # fix: this is more specific to rectangles 
        if (self.x >= obst.left and
            self.x <= obst.right and
            self.y >= obst.bottom and
            self.y <= obst.top):
            return True
        return False

    def add_connection(self, other):
        if other not in self.connections:
            self.connections.add(other)

    def __repr__(self):
        return "x:" + str(self.x) + "y:" + str(self.y)

class Obstacle():

    def __init__(self, l, r, b, t):
        self.left = l
        self.right = r
        self.top = t
        self.bottom = b

    @abstractmethod
    def collides(self, obs):
        """
        Returns boolean based on obstacle collision
        """

class Rectangle(Obstacle):

    def __init__(self, l, r, b, t):
        # fix: throw exception if l/r and b/t do not match position
        super().__init__(l, r, b, t)

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
        for i in range(30):
            xval = random.randint(0, self.world.width)
            yval = random.randint(0, self.world.height)
            v = Vertex(xval, yval)
            if self.world.add_vertex(v):
                plt.plot([xval],[yval], 'ko')
                plt.draw()
                plt.pause(0.01)

    def connect(self):
        temp_list = list(self.world.test_points)
        # iterate through vertices
        for i in range(len(temp_list)):
            # iterate through remaining vertices
            curr_vert = temp_list[i]
            for j in range(i+1, len(temp_list)):
                vert = temp_list[j]
                c = Connection(curr_vert, vert)
                if self.world.add_connection(c):
                    # plot connection
                    plt.plot([curr_vert.x, vert.x],[curr_vert.y, vert.y],'k-')
                    plt.pause(0.01)
                    

    def search(self):
        result = self.world.search_paths()
        if result != None:
            # plot lines of path
            for i in range(len(result)):
                # check not last vertex
                if i != len(result)-1:
                    s_vert = result[i]
                    e_vert = result[i+1]
                    plt.plot([s_vert.x, e_vert.x],[s_vert.y, e_vert.y],'r-')
                    plt.pause(0.01)
        else:
            print("None")

test = Tester(50, 30)
input("Hit enter to continue.")
test.initialization()
input("Hit enter to continue.")
test.sample()
input("Hit enter to continue.")
test.connect()
input("Hit enter to continue.")
test.search()
print("Finished.")
plt.waitforbuttonpress()
