class Node:

    EMPTY = 0
    WALL = 1
    GOKU = 2
    FREEZER = 3
    CELL = 4
    SEED = 5
    BALL = 6
    FOUND_BALL = 7

    def __init__(self, state, father, operator, depth, cost, cell, seed):
        self.__state = state
        self.__father = father
        self.__operator = operator
        self.__depth = depth
        self.__cost = cost
        self.__cell = cell 
        self.__seed = seed  # Cost to go through a cell or freezer when having a seed comes down to 1
        self.__gokuPos = []
        self.__heuristic = 0  # The correct value is given only when the avara algorithm is used
        self.__sumCostHeuristic = 0
        self.__awaitingCharacter = 0

    def getRigthCount(self):
        count = 0
        currentNode = self
        operator = currentNode.getOperator()
        while operator != "first father":
            if operator =="right":
                count += 1
            currentNode = currentNode.getFather()
            operator = currentNode.getOperator()
        return count

    def getState(self):
        return self.__state

    def getFather(self):
        return self.__father

    def getOperator(self):
        return self.__operator

    def getDepth(self):
        return self.__depth

    def getCost(self):
        return self.__cost

    def getHeuristic(self):
        return self.__heuristic

    def getGokuPos(self):
        return self.__gokuPos

    def getCell(self):
        return self.__cell

    def getSeed(self):
        return self.__seed

    def getState(self):
        return self.__state.copy()

    def getAwaitingCharacter(self):
        return self.__awaitingCharacter
    
    def getSumCostHeuristic(self):
        return self.__sumCostHeuristic

    def setState(self, newState):
        self.__state = newState

    def setFather(self, newFather):
        self.__father = newFather

    def setOperator(self, newOperator):
        self.__operator = newOperator

    def setDepth(self, newDepth):
        self.__depth = newDepth

    def setCost(self, newCost):
        self.__cost = newCost

    def setHeuristic(self, newHeuristic):
        self.__heuristic = newHeuristic

    def setGokuPos(self, newGokuPos):
        self.__gokuPos = newGokuPos

    def setCell(self, newCellValue):
        self.__cell = newCellValue

    def setSeed(self, newSeedValue):
        self.__seed = newSeedValue

    def setAwaitingCharacter(self, awaitingCharacter):
        self.__awaitingCharacter = awaitingCharacter

    def setSumCostHeuristic(self, newValue):
        self.__sumCostHeuristic = newValue

    def calculateManhattanDistance(self, ballPos):
        iDistance = ballPos[0] - self.getGokuPos()[0]
        jDistance = ballPos[1] - self.getGokuPos()[1]
        manhattanDistance = abs(iDistance) + abs(jDistance)
        return manhattanDistance

    def calculateHeuristic(self, manhattanDistance):
        heuristic = 0
        # assuming Goku has several seeds, only a max. of 12 squares would cost half as much.
        if (manhattanDistance > 12):
            heuristic = manhattanDistance - 6
        else:
            heuristic = manhattanDistance / 2
        return heuristic

    def rightMovement(self, gokuPos):
        return [gokuPos[0], gokuPos[1] + 1 if gokuPos[1] < 9 else False]

    def leftMovement(self, gokuPos):
        return [gokuPos[0], gokuPos[1] - 1 if gokuPos[1] > 0 else False]

    def upMovement(self, gokuPos):
        return [gokuPos[0] - 1 if gokuPos[0] > 0 else False, gokuPos[1]]

    def downMovement(self, gokuPos):
        return [gokuPos[0] + 1 if gokuPos[0] < 9 else False, gokuPos[1]]

    # True means that the node can expand their sons, false means it can't
    def avoidGoBack2(self, nextGokuPos):
        currentNode = self
        fatherNode = self.getFather()
        grandFatherNode = fatherNode.getFather()
        nextNodePosition = nextGokuPos
        if grandFatherNode.getOperator() != "first father":
            if (grandFatherNode.getGokuPos() == nextNodePosition):
                if (grandFatherNode.getSeed() != currentNode.getSeed() or (fatherNode.getSeed() == 1 and currentNode.getSeed() == 0)):
                    return True
                else:
                    return False
        return True

    def compareCicles2(self, nextGokuPos):
        currentNode = self
        fatherNode = self.getFather()
        grandFatherNode = fatherNode.getFather()
        nextNodePosition = nextGokuPos
        while grandFatherNode.getOperator() != "first father":
            if (grandFatherNode.getGokuPos() == nextNodePosition):
                if (grandFatherNode.getSeed() != currentNode.getSeed() or (fatherNode.getSeed() == 1 and currentNode.getSeed() == 0)):
                    grandFatherNode = grandFatherNode.getFather()
                else:
                    return False
            else:
                grandFatherNode = grandFatherNode.getFather()
        return True

    def moveRight(self, posGoku):
        i = posGoku[0]
        j = posGoku[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i, j+1])
        return self

    def moveLeft(self, posGoku):
        i = posGoku[0]
        j = posGoku[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i, j-1])
        return self

    def moveDown(self, posGoku):
        i = posGoku[0]
        j = posGoku[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i+1, j])
        return self

    def moveUp(self, posGoku):
        i = posGoku[0]
        j = posGoku[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i-1, j])
        return self

    def setNewCost(self, pos):
        i = pos[0]
        j = pos[1]
        state = self.getState()
        currentCost = self.getCost()  # Current cost is the one from the father
        # If the position where Goku will move into has a Freezer inside then:
        if state[i, j] == self.FREEZER:
            if self.getSeed() > 0:  # If true, Goku can use the seed to kill Freezer
                self.setCost(currentCost + 1)
            else:  # If all of the cases above did not meet, Goku is affected by Freezer
                self.setCost(currentCost + 4)
        elif state[i, j] == self.CELL:
            if self.getSeed() > 0:  # If true, Goku can use the seed to kill Cell
                self.setCost(currentCost + 1)
            else:  # If all of the cases above did not meet, Goku is affected by Cell
                self.setCost(currentCost + 7)
        else:
            self.setCost(currentCost + 1)

    # pos is the future position of Goku
    def takeDecision(self, pos):
        i = pos[0]
        j = pos[1]
        if self.__state[i, j] == self.BALL:
            self.setAwaitingCharacter(self.EMPTY)
            self.__state[i, j] = self.FOUND_BALL
        elif self.__state[i, j] == self.FREEZER:
            if self.getSeed() > 0:
                self.setAwaitingCharacter(self.EMPTY)
                self.setSeed(self.getSeed() - 1 if self.getSeed() > 0 else 0)
            else:
                self.setAwaitingCharacter(self.FREEZER)
        elif self.__state[i, j] == self.CELL:
            if self.getSeed() > 0:
                self.setAwaitingCharacter(self.EMPTY)
                self.setSeed(self.getSeed() - 1 if self.getSeed() > 0 else 0)
            else:
                self.setAwaitingCharacter(self.CELL)
        elif self.__state[i, j] == self.SEED:
            self.setSeed(self.getSeed() + 1)
            self.setAwaitingCharacter(self.EMPTY)
        else:
            self.setAwaitingCharacter(self.EMPTY)

        if self.__state[i, j] != self.FOUND_BALL:
            self.__state[i, j] = self.GOKU

    def recreateSolution(self):
        directions = []
        currentNode = self
        while currentNode.getOperator() != "first father":
            directions.append(
                str(currentNode.getOperator() + " " + str(currentNode.getCost()) + " Seed: " + str(currentNode.getSeed())))
            currentNode = currentNode.getFather()
        return directions

    def recreateSolutionWorld(self):
        directions = []
        currentNode = self
        while currentNode.getOperator() != "first father":
            directions.append(currentNode.getState())
            currentNode = currentNode.getFather()
        return directions

    def searchForGoku(self):
        gokuPos = [-1, -1]  # Goku position [x,y]
        state = self.__state
        for i in range(10):
            for j in range(10):
                if (state[i, j] == self.GOKU):
                    gokuPos[0] = i
                    gokuPos[1] = j

        self.setGokuPos(gokuPos)
        return gokuPos

    def isGoal(self):
        state = self.__state
        for i in range(10):
            for j in range(10):
                if (state[i, j] == self.FOUND_BALL):
                    state[i, j] = self.GOKU
                    return True
        return False
