import queue as q
import copy as c

visited = set()
inserted = set()
maxqueue = 0

def hashkey(state):
    key = ""
    for i in range(len(state)):
        for j in range(len(state[i])):
            temp = chr(state[i][j] + 65)
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


def generatefalse(dim):
    false = list()
    for i in range(0, dim):
        temp = list()
        for j in range(0, dim):
            temp.append(-1)
        false.append(temp)
    return false

def findblank(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
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
    nodes = q.Queue()
    nodes.put(problem)
    goal = generategoal(len(problem))
    while(1):
        if nodes.empty():
            return generatefalse(len(problem))
        curr = nodes.get()
        visited.add(hashkey(curr))
        if curr == goal:
            return curr
        branches = function(curr, operators)
        for branch in branches:
            nodes.put(c.deepcopy(branch))
        global maxqueue
        if nodes.qsize() > maxqueue:
            maxqueue = nodes.qsize()


def uniformcost(puzzle, operators):
    branches = list()
    for op in operators:
        temp = c.deepcopy(puzzle)
        temp = op(temp)
        if hashkey(temp) not in inserted:
            branches.append(c.deepcopy(temp))
            inserted.add(hashkey(temp))
    return branches


def left(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != 0:
        problem[i][j], problem[i][j-1] = problem[i][j-1], problem[i][j]
    return problem


def right(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if j != len(problem) - 1:
        problem[i][j], problem[i][j+1] = problem[i][j+1], problem[i][j]
    return problem


def up(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != 0:
        problem[i][j], problem[i-1][j] = problem[i-1][j], problem[i][j]
    return problem


def down(problem):
    i, j = findblank(problem)[0], findblank(problem)[1]
    if i != len(problem) - 1:
        problem[i][j], problem[i+1][j] = problem[i+1][j], problem[i][j]
    return problem


def main():
    operators = [up, down, left, right]
    puzzle = inputpuzzle(3)
    visited.add(hashkey(puzzle))
    inserted.add(hashkey(puzzle))
    puzzle = generalsearch(puzzle, uniformcost, operators)
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            print(puzzle[i][j], end = " ")
        print()
    print(hashkey(puzzle))
    expanded = len(visited)
    print(expanded)
    print(maxqueue)


main()
