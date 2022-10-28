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


def main():
    goal = inputpuzzle(3)
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            print(goal[i][j])
    print(hashkey(goal))


main()