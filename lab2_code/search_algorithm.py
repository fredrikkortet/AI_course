import numpy as np
import math
import random as rand
from heapq import heappop, heappush
import queue
# Priority Queue based on heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []
    def isEmpty(self):
        return len(self.elements) == 0
    def put(self, item, priority):
        heappush(self.elements,(priority,item))
    def get(self):
        return heappop(self.elements)[1]

'''
Node class saves  parent node, path cost, a list called value that coordinates have been saved in
cost : from start point to the goal point cost = gcost+hueristic cost 
gcost : from start point of searching till finding the start point. ex. from 0,0 to -2 
h : heuristic cost  from start to the goal point
value : a list of coordinates 
parent : parent node.

'''
class node:
    def __init__(self):
            self.parent=None
            self.value=[]
            self.cost=math.inf
            self.gcost=math.inf
            self.h=math.inf
    def __iter__(self):
        node=self
        while node is not None:
            yield node
            node = node.parent
    def __eq__(self, other):
        return (self.value == other.value)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.cost < other.cost )

    def __gt__(self, other):
        return (self.cost > other.cost )

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)


'''
This function checks if the the the current node is inside the give coordinates and checks for obstacle  .
x = coordinate on x-axis 
y = coordinate on y-axis
map : the graph
maxy : the limit of the y axis. max size of the map on the y axis
maxx : the limit of the x axis. max size of the map on the x axis

'''
def valid(x,y,map):
    current=[x,y]
    maxy,maxx=len(map),len(map[0])
    if 0<=current[0]<maxx and 0<=current[1]<maxy:
        if map[current[1]][current[0]] != -1:
            return True
    return False




'''
This function is A* algorithm for H-map obstacle. This is a function with self-built heuristic function for the 
capital-H map. 

map: is the graph with capital-H obstacle 
start : the start point
goal : end point
info : information about the obstacle in the map. 
been_here: a list that save visited nodes
currentnode : access to the class node to get access to parent, path and costs and also coordinates.
path_here: a list of paths taken 
nextcost is Manhathan formula to count cost. 

'''
def astarnew(map,start,goal,info):
    been_here=[start]
    priority = PriorityQueue()
    currentnode=node()
    currentnode.value=start # coordinate of the start point saves in list value.
    currentnode.cost=0  # total cost is zero at the beginning
    currentnode.gcost=0 # start cost is also zero
    path_here=[]
    priority.put(currentnode,currentnode.cost)
    while not priority.isEmpty():
        temp=priority.get()
        currentlist=temp
        #print(currentlist)
        current=currentlist.value
        if current ==goal: # checks if we have reached the goal
            for i in currentlist:
                path_here.append(i.value) # saves the coordinates in a list called path_here
            #print("start: ",start,"goal: ",goal,"current: ",current)
            break
        if start == current:# this is for not collide with start get a cost and its not been found later in plotmap
              nextgcost=1#first cost
              nextcost=nextgcost+(abs(current[0]-goal[0])+abs(current[1]-goal[1])) # h(n) = |n.x -goal.x| + |n.y-goal.y|       else:
        else:
            nextgcost=cost_function(currentlist,map) #use the same cost as in greedy
            nextcost=nextgcost+newheuristic(currentlist,map,goal,start,info)#get the gcost + heuristic with the modified one
        for next in get_neighbors2(currentlist,map):#get the special get neighbeors
            if next not in been_here:#check if we already been here on that place
                currentnode=node()#make new node
                currentnode.value=next#put the cordinates in node
                currentnode.parent=currentlist#put current node in parent
                currentnode.cost=nextcost#add the new cost
                currentnode.gcost=nextgcost# add the gcost
                priority.put(currentnode,currentnode.cost)#put node in queue with priority cost
                been_here.append(next)#add to been_here to not search in the same node later
    return np.array(path_here),been_here##send back path and been_here list to process later



'''
check the astarnew function for comments
just a formula changes.
'''
def astarManhattan(map,start,goal):
    been_here=[start]
    priority = PriorityQueue()
    currentnode=node()
    currentnode.value=start
    currentnode.cost=0
    currentnode.gcost=0
    path_here=[]
    priority.put(currentnode,currentnode.cost)
    while not priority.isEmpty():
        temp=priority.get()
        currentlist=temp
        #print(currentlist)
        current=currentlist.value
        if current ==goal:
            for i in currentlist:
                path_here.append(i.value)
            #print("start: ",start,"goal: ",goal,"current: ",current)
            break
        if start == current:
              nextgcost=1
              nextcost=nextgcost+(abs(current[0]-goal[0])+abs(current[1]-goal[1]))
        else:
            nextgcost=cost_function(currentlist,map)
            nextcost=nextgcost+manhattan(currentlist,map,goal)
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                currentnode.gcost=nextgcost
                priority.put(currentnode,currentnode.cost)
                been_here.append(next)
    return np.array(path_here),been_here

'''
check the astarnew function for comments
just a formula changes.
'''
def astarEuclidean(map,start,goal):
    map =np.copy(map)
    been_here=[start]
    priority = PriorityQueue()
    currentnode=node()
    currentnode.value=start
    currentnode.cost=0
    currentnode.gcost=0
    path_here=[]
    priority.put(currentnode,currentnode.cost)
    while not priority.isEmpty():
        temp=priority.get()
        currentlist=temp
        #print(currentlist)
        current=currentlist.value
        if current ==goal:
            for i in currentlist:
                path_here.append(i.value)
            break
        if start == current:
              nextgcost=1
              nextcost=nextgcost+(current[0]-goal[0])**2+(current[1]-goal[1])**2/2
        else:
            nextgcost=cost_function(currentlist,map)
            nextcost=nextgcost+ecluidean(currentlist,map,goal)
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                currentnode.gcost=nextgcost
                priority.put(currentnode,currentnode.cost)
                been_here.append(next)
    return np.array(path_here),been_here

'''
check the astarnew function for comments
just a formula changes.
gcost = cost from start of searching to current point which is the start point ex. -2 
'''
def greedy(map,start,goal):
    been_here=[start]
    priority = PriorityQueue()
    currentnode=node()
    currentnode.value=start
    currentnode.cost=0
    path_here=[]
    priority.put(currentnode,currentnode.cost)
    while not priority.isEmpty():
        temp=priority.get()
        currentlist=temp
        #print(currentlist)
        current=currentlist.value
        if current ==goal:
            for i in currentlist:
                path_here.append(i.value)
            #print("start: ",start,"goal: ",goal,"current: ",current)
            break
        if start == current:
              nextcost=1
        else:
            nextcost=cost_function(currentlist,map)
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                priority.put(currentnode,currentnode.cost)
                been_here.append(next)
    return np.array(path_here),been_here

'''
DFS algorithm
been_here is a list that saves the visited nodes. 
stack is a stack data structure
it uses last in first out. 
'''
def searchdepth(map,start,goal):
    been_here=[start]
    stack = queue.LifoQueue()
    currentnode=node()
    currentnode.value=start
    currentnode.cost=0
    path_here=[]
    stack.put(currentnode)
    while not stack.empty():
        currentlist=stack.get()
        current=currentlist.value
        if current ==goal:
            for i in currentlist:
                path_here.append(i.value)
            #print("start: ",start,"goal: ",goal,"current: ",current)
            break
        if start == current:
              nextcost=1
        else:
            nextcost=cost_function(currentlist,map)
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                stack.put(currentnode)
                been_here.append(next)
    return np.array(path_here),been_here



'''
search() function is a bfs searching algorithm 
BFS algorithm
been_here is a list that saves the visited nodes. 
 que : is a queue not a priority queue. 
'''

def search(map, start, goal):
    been_here =[start]
    currentnode= node()
    currentnode.value=start
    currentnode.cost=0
    path_here=[]
    #print(start,"end ",goal)
    que= queue.Queue()

    que.put(currentnode)
    while not que.empty():
        currentlist = que.get()
        current=currentlist.value
        if current == goal:
            for i in currentlist:
                path_here.append(i.value)
            break
        if start == current:
              nextcost=1
        else:
            nextgcost=cost_function(currentlist,map)
            nextcost=nextgcost
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                que.put(currentnode)
                been_here.append(next)
    return np.array(path_here),been_here


'''

'''
def random_search(map,start,goal):
    been_here =[start]
    currentnode= node()
    currentnode.value=start
    currentnode.cost=0
    path_here=[]
    #print(start,"end ",goal)
    que= []

    que.append(currentnode)
    while not que.count == 0:
        currentlist = que.pop(rand.randint(0,len(que)-1))
        current=currentlist.value
        #parent=currentlist
        #print("path ",parent.parent)is
        if current == goal:
            for i in currentlist:
                #print(i.value)
                path_here.append(i.value)
            #print("start: ",start,"goal: ",goal,"current: ",current)
            break
        #if current not in path_here:
        #    path_here.append(current)
        if start == current:
              nextcost=1
        else:
            nextcost=cost_function(currentlist,map)
        for next in get_neighbors(currentlist,map):
            if next not in been_here:
                currentnode=node()
                currentnode.value=next
                currentnode.parent=currentlist
                currentnode.cost=nextcost
                que.append(currentnode)
                been_here.append(next)
    return np.array(path_here),been_here

def get_neighbors(currentlist,map):
    neighbors=[]
    neighbors.clear()
    current=currentlist.value
    #lencg on map top and right 
    temp=[current[0]+1,current[1]]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
    temp=[current[0]-1,current[1]]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
    temp=[current[0],current[1]-1]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
    temp=[current[0],current[1]+1]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)

    #print(neighbors)
    return neighbors
def get_neighbors2(currentlist,map):
    neighbors=[]
    current=currentlist.value
    #lencg on map top and right 
    temp=[current[0]+1,current[1]]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
        #currentlist.great=1
    temp=[current[0]-1,current[1]]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
        #currentlist.great=1
    temp=[current[0],current[1]-1]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
        #currentlist.great=1
    temp=[current[0],current[1]+1]
    if valid(temp[0],temp[1],map):
        neighbors.append(temp)
    #print(neighbors)
    return neighbors

def cost_function(cost,map):
    cord=cost.value
    map[cord[1]][cord[0]]=cost.cost
    return cost.parent.cost+1

def ecluidean(cost,map,goal):
    cord=cost.value
    e=((cord[0]-goal[0])**2+(cord[1]-goal[1])**2)**0.5
    map[cord[1]][cord[0]]=e
    return e

def manhattan(cost,map,goal):
    cord=cost.value
    m=abs(cord[0]-goal[0])+abs(cord[1]-goal[1])
    map[cord[1]][cord[0]]=m
    return m
def newheuristic(cost,map,goal,start,info):
    ytop,ybot,minx=info
    cord=cost.value
    obstacle = np.where(map[ybot]==-1)[0][0]
    middle=ybot+(ytop-ybot)//2
    if cord[1] in range(ybot,ytop) and cord[0] in range(max(obstacle,start[0]),goal[0]):
        C = 5000-abs(minx -cord[0])**2-abs(cord[1]-middle)**2
        map[cord[1]][cord[0]]=C
        return C
    C=abs(cord[0]-goal[0])+abs(cord[1]-goal[1])
    map[cord[1]][cord[0]]=C
    return C
