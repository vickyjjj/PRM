
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
        """
        Initialize mission: set starting and ending points.
        """
        self.start = start 
        self.end = end
        # add start and end points to set of all points 
        self.test_points.add(self.start)
        self.test_points.add(self.end)

    def add_obstacle(self, obst):
        """
        Add obstacle to world if obs does not collide with any
        already-placed obstacles.
        """
        # check existing obstacles 
        for placed_obs in self.obstacles:
            # check obstacle collision
            if obst.collides(placed_obs):
                return False
        self.obstacles.append(obst)
        return True
    
    def add_vertex(self, vert):
        """
        Add test point to world if point has not been added yet
        and doesn't collide with any already-placed obstacles. 
        """
        # check existing points
        if vert not in self.test_points:
            # check obstacle collision for all obstacles 
            for obst in self.obstacles:
                if vert.collides(obst):
                    return False
        else:
            return False
        self.test_points.add(vert)
        return True

    def add_connection(self, conn):
        """
        Add connection to world if it doesn't cross through any obstacles.
        """
        # find line equation between points        
        vertical = False
        vert_s = conn.start
        vert_e = conn.end
        try:
            # non-vertical line
            slope = (vert_s.y-vert_e.y)/(vert_s.x-vert_e.x)
            intercept = vert_s.y-slope*vert_s.x
        except:
            # vertical line
            vertical = True
        # iterate through obstacles
        for obst in self.obstacles:
            if vertical:
                # if vertical, check vertical range not in obstacle occupied points
                for i in range(vert_s.y, vert_e.y):
                    if (vert_s.x, i) in obst.occ_points:
                        return False
            else:
                # sort x positional values
                x_vals = [obst.left, obst.right, vert_s.x, vert_e.x]
                x_vals.sort()
                # check overlap exists between segments and obstacle before checking for overlap
                if x_vals[:2] != [obst.left, obst.right] and x_vals[2:] != [obst.left, obst.right]:
                    # check point on line not in occupied points
                    for i in range(obst.left, obst.right):
                        if (i, int(i*slope+intercept)) in obst.occ_points or (i, int(round(i*slope+intercept))) in obst.occ_points:
                            return False
        # add to world's connections
        self.connections.append(conn)
        # add to vertice's connections
        conn.start.add_connection(conn)
        conn.end.add_connection(conn)
        return True

    def search_paths_bfs(self): # fix
        """
        BFS unweighted
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
                cvert_s = conn.start
                cvert_e = conn.end
                # we have found the goal vertex
                if cvert_s == self.end:
                    path.append(cvert_s)
                    return path
                if cvert_e == self.end:
                    path.append(cvert_e)
                    return path
                # add to queue to search if not already searched this vertex
                if cvert_s not in already_searched:
                    newpath = []
                    for i in path:
                        newpath.append(i)
                    newpath.append(cvert_s)
                    queue.append(newpath)
                    already_searched.add(cvert_s)
                if cvert_e not in already_searched:
                    newpath = []
                    for i in path:
                        newpath.append(i)
                    newpath.append(cvert_e)
                    queue.append(newpath)
                    already_searched.add(cvert_e)
        return None

    def search_paths_bfsw(self): # fix
        """
        BFS weighted by distance
        """
        # initialize queues
        queue = [] # order matters
        already_searched = set()
        queue.append((0,[self.start])) # tuple: distance, list of nodes traversed
        already_searched.add(self.start)

        # begin search
        while (len(queue) != 0):
            # get current vertex to look at m
            to_consider = queue.pop(0)
            weight = to_consider[0]
            path = to_consider[1]
            curr = path[-1]
            # get connecting vertices of this vertex
            for conn in curr.connections:
                cvert_s = conn.start
                cvert_e = conn.end
                # we have found the goal vertex
                if cvert_s == self.end:
                    path.append(cvert_s)
                    return path
                if cvert_e == self.end:
                    path.append(cvert_e)
                    return path
                # add to queue to search if not already searched this vertex
                if cvert_s not in already_searched:
                    newpath = []
                    for i in path:
                        newpath.append(i)
                    newpath.append(cvert_s)
                    newweight = weight + conn.weight
                    if len(queue) != 0 and newweight < queue[-1][0]:
                        for j in range(len(queue)):
                            if queue[j][0] >= newweight:
                                queue.insert(j, (newweight, newpath))
                    else:
                        # weight is larger than all other options
                        queue.append((newweight, newpath))
                    already_searched.add(cvert_s)
                if cvert_e not in already_searched:
                    newpath = []
                    for i in path:
                        newpath.append(i)
                    newpath.append(cvert_e)
                    newweight = weight + conn.weight
                    if len(queue) != 0 and newweight < queue[-1][0]:
                        for j in range(len(queue)):
                            if queue[j][0] >= newweight:
                                queue.insert(j, (newweight, newpath))
                    else:
                        # weight is larger than all other options
                        queue.append((newweight, newpath))
                    already_searched.add(cvert_e)
        return None
    
class Vertex():

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.position = (self.x, self.y) # tuple form
        self.connections = set()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def collides(self, obst):
        """
        Check if point collides with obstacle 
        """
        # fix: this is more specific to rectangles (bounding box check)
        if (self.x >= obst.left and
            self.x <= obst.right and
            self.y >= obst.bottom and
            self.y <= obst.top):
            return True
        return False

    def add_connection(self, other):
        """
        Fix
        """
        if other not in self.connections:
            self.connections.add(other)

    def __repr__(self):
        return "x:" + str(self.x) + "y:" + str(self.y)

class Obstacle():

    def __init__(self, l, r, b, t):
        self.left = int(l)
        self.right = int(r)
        self.top = int(t)
        self.bottom = int(b)
        self.occ_points = self.get_occ_points()

    @abstractmethod
    def collides(self, obs):
        """
        Returns boolean based on obstacle collision
        """

    @abstractmethod
    def get_occ_points(self):
        """
        Returns set of all occupied points 
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
         Fix
        """
        if (obst.left > self.right or
            self.left > obst.right or
            obst.bottom > self.top or
            self.bottom > obst.top):
            return False
        return True

    def get_occ_points(self):
        """
        Returns set of tuple of all occupied points 
        """
        result = set()
        for x in range(self.left, self.right+1):
            for y in range(self.bottom, self.top+1):
                result.add((x,y))
        return result

class Connection():

    def __init__(self, vert_1, vert_2):
        # vertex with the higher y should be initialized as "end" point
        if vert_1.y < vert_2.y:
            self.start = vert_1
            self.end = vert_2
        else:
            self.start = vert_2
            self.end = vert_1
        self.weight = ((self.start.x-self.end.x)**2+(self.start.y-self.end.y)**2)**0.5

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
        plt.gca().annotate("init", start.position)
        plt.gca().annotate("goal", end.position)
        plt.draw()

    def sample(self):
        # sample vertices
        for i in range(50):
            xval = random.randint(0, self.world.width)
            yval = random.randint(0, self.world.height)
            v = Vertex(xval, yval)
            if self.world.add_vertex(v):
                plt.plot([xval],[yval], 'ko')
                plt.draw()
                plt.pause(0.001)

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
                    plt.pause(0.00001)
                    

    def bfs_search(self):
        result = self.world.search_paths_bfs()
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

    def bfsw_search(self):
        result = self.world.search_paths_bfsw()
        if result != None:
            # plot lines of path
            for i in range(len(result)):
                # check not last vertex
                if i != len(result)-1:
                    s_vert = result[i]
                    e_vert = result[i+1]
                    plt.plot([s_vert.x, e_vert.x],[s_vert.y, e_vert.y],'b-')
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
test.bfs_search()
input("Hit enter to continue.")
test.bfsw_search()
print("Finished.")
plt.waitforbuttonpress()
