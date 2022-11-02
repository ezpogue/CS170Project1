import queue as q #For PriorityQueue
import copy as c #For copying and deep copying lists
import time as t #For timing
from dataclasses import dataclass, field #For PrioritizedItem
from typing import Any #For PrioritizedItem

visited = set()
inserted = set()
maxqueue = 0
depth = 0
frontier = 0

@dataclass(order=True)
class PrioritizedItem:#Wrapper class to be used with the priority queue, taken from https://docs.python.org/3/library/queue.html
    priority: (int, int) #Tuple is used to allow tie-breaking in sorting based on depth
    item: Any=field(compare=False)


class slidepuzzle:#Holds all info for the state of a puzzle

    def __init__(self, dim, state, depth):
        self.dim = dim
        self.state = state
        self.depth = depth #g(n)
        self.heuristic = 0 #h(n)

    def hashkey(self):#Converts the state into a string, allowing it to be used as a dictionary key
        key = ""
        for i in range(self.dim):
            for j in range(self.dim):
                temp = chr(self.state[i][j] + 65)
                key += temp
        return key


def generategoal(dim): #Generates a goal state given the dimension of the puzzle
        goal = list()
        num = 1
        for i in range(0, dim):
            temp = list()
            for j in range(0, dim):
                if i == dim - 1 and j == dim - 1:
                    temp.append(0)
                else:
                    temp.append(num)
                num += 1
            goal.append(temp)
        return goal


def findblank(puzzle): #Finds the 0 tile and returns its coordinates
    for i in range(puzzle.dim):
        for j in range(puzzle.dim):
            if puzzle.state[i][j] == 0:
                return (i, j)


def findval(puzzle, val): #Finds val and returns its coordinates
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == val:
                return (i, j)


def inputpuzzle(dim): #Takes in user input and creates a slide puzzle
    puzzle = list()
    print('Please input a valid ' + str(dim*dim - 1) + '-puzzle')
    for i in range(0, dim):
        temp = list()
        print('Input your ' + str(dim) + ' values for line ' + str(i+1))
        for j in range(0, dim):
            temp.append(int(input()))
        puzzle.append(temp)
    return puzzle


def generalsearch(problem, function, operators): #General search algorithm template, adapted from the slides
    nodes = q.PriorityQueue()
    start = PrioritizedItem(0, problem) #Inserting initial state into queue
    nodes.put(start)
    goal = generategoal(problem.dim) #Generating goal state for comparisons
    while(1):
        if nodes.empty():
            return False #Queue can only be empty if we have checked all nodes
        curr = nodes.get().item
        print('Expanding node with g(n) = '  + str(curr.depth) + ' and h(n) = ' + str(curr.heuristic))
        for i in range(curr.dim):
            for j in range(curr.dim):
                print(curr.state[i][j], end = ' ')
            print()
        visited.add(curr.hashkey()) #Adding state to list of expanded nodes
        if curr.state == goal:
            global depth
            depth = curr.depth
            global frontier
            frontier = nodes.qsize()
            return True
        branches = function(curr, operators) #Uses whatever function we passed to find h(n) for all children nodes
        for branch in branches:
            node = PrioritizedItem((branch.heuristic + branch.depth, branch.depth), branch) #Inserting into queue based on h(n) + g(n), then just g(n) in event of a tie
            nodes.put(c.copy(node))
        global maxqueue
        if nodes.qsize() > maxqueue:
            maxqueue = nodes.qsize() #Updating maximum queue size


def uniformcost(puzzle, operators): #Uniform Cost Search queuing function
    branches = list()
    for op in operators:
        temp = c.deepcopy(puzzle)
        temp = op(temp)
        if temp.hashkey() not in inserted:
            branches.append(slidepuzzle(temp.dim, temp.state, temp.depth+1))
            inserted.add(c.copy(temp.hashkey()))
    return branches


def misplacedtile(puzzle, operators): #Misplaced Tile Heuristic queuing function
    branches = list()
    for op in operators:
        temp = c.deepcopy(puzzle)
        temp = op(temp)
        if temp.hashkey() not in inserted:
            branches.append(slidepuzzle(temp.dim, temp.state, temp.depth+1))
            inserted.add(c.copy(temp.hashkey()))
    for branch in branches:
        branch.heuristic = mtheuristic(branch)
    return branches


def manhattandistance(puzzle, operators):#Manhattan Distance Heuristic queuing function
    branches = list()
    for op in operators:
        temp = c.deepcopy(puzzle)
        temp = op(temp)
        if temp.hashkey() not in inserted:
            branches.append(slidepuzzle(temp.dim, temp.state, temp.depth+1))
            inserted.add(c.copy(temp.hashkey()))
    for branch in branches:
        branch.heuristic = mdheuristic(branch)
    return branches

def ucheuristsic(puzzle): #Returns h(n) for Uniform Cost, only used in main
    return 0


def mtheuristic(puzzle):#Returns h(n) for Missing Tile
    distance = 0
    goal = generategoal(puzzle.dim)
    for i in range(0, puzzle.dim):
        for j in range(0, puzzle.dim):
            if puzzle.state[i][j] != 0 and puzzle.state[i][j] != goal[i][j]: #If a tile is in the wrong place, increment by 1
                distance += 1
    return distance


def mdheuristic(puzzle):#Returns h(n) for Manhattan Distance
    distance = 0
    goal = generategoal(puzzle.dim)
    for i in range(0, puzzle.dim):
        for j in range(0, puzzle.dim):
            if puzzle.state[i][j] != 0 and puzzle.state[i][j] != goal[i][j]:#If a tile is in the wrong place, increment by x offset and y offset
                d = findval(goal, puzzle.state[i][j])
                distance += abs(i - d[0]) + abs(j - d[1])
    return distance


def up(problem): #Operator that moves the 0 tile up
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != 0:
        problem.state[i][j], problem.state[i-1][j] = problem.state[i-1][j], problem.state[i][j]
    return problem


def down(problem): #Operator that moves the 0 tile down
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != problem.dim - 1:
        problem.state[i][j], problem.state[i+1][j] = problem.state[i+1][j], problem.state[i][j]
    return problem


def left(problem):#Operator that moves the 0 tile left
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != 0:
        problem.state[i][j], problem.state[i][j-1] = problem.state[i][j-1], problem.state[i][j]
    return problem


def right(problem):#Operator that moves the 0 tile right
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != problem.dim - 1:
        problem.state[i][j], problem.state[i][j+1] = problem.state[i][j+1], problem.state[i][j]
    return problem


def main():
    operators = [up, down, left, right] #List of operator functions
    queuingfunctions = [uniformcost, misplacedtile, manhattandistance]#List of queuing functions
    heuristics = [ucheuristsic, mtheuristic, mdheuristic]#List of heuristic functions
    dim = int(input('Choose the size of your puzzle: '))
    puzzle = slidepuzzle(dim, inputpuzzle(dim), 0) #Create initial state from input
    #puzzle = slidepuzzle(dim, [[1,2,3],[4,5,6],[8,7,0]], 0) #For testing
    visited.add(puzzle.hashkey())
    inserted.add(puzzle.hashkey())
    qf = int(input('Choose your queuing function:\n (1) = Uniform cost\n (2) = Misplaced tile heuristic\n (3) = Manhattan distance heuristic:'))-1
    puzzle.heuristic = heuristics[qf](puzzle)
    timer = t.time() #Start timer
    outcome = generalsearch(puzzle, queuingfunctions[qf], operators)
    timer = t.time() - timer #Stop timer
    print('Is the goal state reachable? ' + str(outcome))
    tested = len(visited) - 1
    print('Number of nodes tested: ' + str(tested))
    print('Maximum nodes in the queue: ' + str(maxqueue))
    print('Solution depth: ' + str(depth))
    print('Number of frontier nodes: ' + str(frontier))
    print('Time taken: ' + str(round(timer, 3)))



main()
