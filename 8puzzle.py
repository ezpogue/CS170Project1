import queue as q
import copy as c
import time as t
from dataclasses import dataclass, field
from typing import Any

visited = set()
inserted = set()
maxqueue = 0
depth = 0

@dataclass(order=True)
class PrioritizedItem:#Taken from https://docs.python.org/3/library/queue.html
    priority: int
    item: Any=field(compare=False)


class slidepuzzle:

    def __init__(self, dim, state, depth):
        self.dim = dim
        self.state = state
        self.depth = depth
        self.heuristic = 0

    def hashkey(self):
        key = ""
        for i in range(self.dim):
            for j in range(self.dim):
                temp = chr(self.state[i][j] + 65)
                key += temp
        return key


def generategoal(dim):
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


def findblank(puzzle):
    for i in range(puzzle.dim):
        for j in range(puzzle.dim):
            if puzzle.state[i][j] == 0:
                return (i, j)


def findval(puzzle, val):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == val:
                return (i, j)


def inputpuzzle(dim):
    puzzle = list()
    print('Please input a valid ' + str(dim*dim - 1) + '-puzzle')
    for i in range(0, dim):
        temp = list()
        print('Input your ' + str(dim) + ' values for line ' + str(i+1))
        for j in range(0, dim):
            temp.append(int(input()))
        puzzle.append(temp)
    return puzzle


def generalsearch(problem, function, operators):
    nodes = q.PriorityQueue()
    start = PrioritizedItem(0, problem)
    nodes.put(start)
    goal = generategoal(problem.dim)
    while(1):
        if nodes.empty():
            return False
        curr = nodes.get().item
        print('Expanding node with g(n) = '  + str(curr.depth) + ' and h(n) = ' + str(curr.heuristic))
        for i in range(curr.dim):
            for j in range(curr.dim):
                print(curr.state[i][j], end = ' ')
            print()
        visited.add(curr.hashkey())
        if curr.state == goal:
            global depth
            depth = curr.depth
            return True
        branches = function(curr, operators)
        for branch in branches:
            node = PrioritizedItem(branch.heuristic + branch.depth, branch)
            nodes.put(c.copy(node))
        global maxqueue
        if nodes.qsize() > maxqueue:
            maxqueue = nodes.qsize()


def uniformcost(puzzle, operators):
    branches = list()
    for op in operators:
        temp = c.deepcopy(puzzle)
        temp = op(temp)
        if temp.hashkey() not in inserted:
            branches.append(slidepuzzle(temp.dim, temp.state, temp.depth+1))
            inserted.add(c.copy(temp.hashkey()))
    return branches


def misplacedtile(puzzle, operators):
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


def manhattandistance(puzzle, operators):
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


def mtheuristic(puzzle):
    distance = 0
    goal = generategoal(puzzle.dim)
    for i in range(0, puzzle.dim):
        for j in range(0, puzzle.dim):
            if goal[i][j] != puzzle.state[i][j]:
                distance += 1
    return distance


def mdheuristic(puzzle):
    distance = 0
    goal = generategoal(puzzle.dim)
    for i in range(0, puzzle.dim):
        for j in range(0, puzzle.dim):
            if goal[i][j] != puzzle.state[i][j]:
                k,l = findval(goal, puzzle.state[i][j])[0], findval(goal, puzzle.state[i][j])[1]
                distance += abs(i - k) + abs(j - l)
    return distance


def up(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != 0:
        problem.state[i][j], problem.state[i-1][j] = problem.state[i-1][j], problem.state[i][j]
    return problem


def down(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != problem.dim - 1:
        problem.state[i][j], problem.state[i+1][j] = problem.state[i+1][j], problem.state[i][j]
    return problem


def left(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != 0:
        problem.state[i][j], problem.state[i][j-1] = problem.state[i][j-1], problem.state[i][j]
    return problem


def right(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != problem.dim - 1:
        problem.state[i][j], problem.state[i][j+1] = problem.state[i][j+1], problem.state[i][j]
    return problem


def main():
    operators = [up, down, left, right]
    queuingfunctions = [uniformcost, misplacedtile, manhattandistance]
    dim = int(input('Choose the size of your puzzle: '))
    puzzle = slidepuzzle(dim, inputpuzzle(dim), 0)
    visited.add(puzzle.hashkey())
    inserted.add(puzzle.hashkey())
    qf = int(input('Choose your queuing function:\n (1) = Uniform cost\n (2) = Misplaced tile heuristic\n (3) = Manhattan distance heuristic:'))-1
    timer = t.time()
    outcome = generalsearch(puzzle, queuingfunctions[qf], operators)
    timer = t.time() - timer
    print('Is the goal state reachable? ' + str(outcome))
    expanded = len(visited)
    print('Number of nodes expanded: ' + str(expanded))
    print('Maximum nodes in the queue: ' + str(maxqueue))
    print('Solution depth: ' + str(depth))
    print('Time taken: ' + str(timer))


main()
