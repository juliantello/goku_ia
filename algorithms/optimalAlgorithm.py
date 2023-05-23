from node import Node
from time import process_time


class OptimalAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0)
        self.gokuPos = self.firstNode.searchForGoku()
        self.ballPos = self.searchForBall(world)
        self.stack = [self.firstNode]
        self.computingTime = ""

    def getNodeMinSumCostHeuristic(self, stack):
        minNode = min(stack, key=lambda node: node.getSumCostHeuristic())
        return minNode

    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def searchForBall(self, world):
        ballPos = []
        for i in range(10):
            for j in range(10):
                if (world[i, j] == self.firstNode.BALL):
                    ballPos.append(i)
                    ballPos.append(j)
        return ballPos

    def start(self):
        startTime = process_time()

        stack = self.stack
        gokuPos = self.gokuPos
        currentNode = stack[0]
        expandedNodes = 0
        depth = 0

        while not (currentNode.isGoal()):
            # Check if right side is free
            # print("---")
            # print(currentNode.getMarioPos())
            if (not (gokuPos[1]+1 > 9) and currentNode.getState()[gokuPos[0], gokuPos[1]+1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "right", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                right = son.rightMovement(gokuPos)
                son.setNewCost(right)
                son.setGokuPos(right)
                sonManhattanDistance = son.calculateManhattanDistance(
                    self.ballPos)
                sonHeuristic = son.calculateHeuristic(sonManhattanDistance)
                son.setHeuristic(sonHeuristic)
                son.setSumCostHeuristic(son.getHeuristic() + son.getCost())
                son.moveRight(gokuPos)
                if (son.avoidGoBack2(right)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()

                    # print(son.getMarioPos(), "heurística: ", son.getHeuristic())

            # Check if left side is free
            if (not (gokuPos[1]-1 < 0) and currentNode.getState()[gokuPos[0], gokuPos[1]-1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "left", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                left = son.leftMovement(gokuPos)
                son.setNewCost(left)
                son.setGokuPos(left)
                sonManhattanDistance = son.calculateManhattanDistance(
                    self.ballPos)
                sonHeuristic = son.calculateHeuristic(sonManhattanDistance)
                son.setHeuristic(sonHeuristic)
                son.setSumCostHeuristic(son.getHeuristic() + son.getCost())
                son.moveLeft(gokuPos)
                if (son.avoidGoBack2(left)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()

                    # print(son.getMarioPos(), "heurística: ", son.getHeuristic())

            # Check if down side is free
            if (not (gokuPos[0]+1 > 9) and currentNode.getState()[gokuPos[0]+1, gokuPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "down", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                down = son.downMovement(gokuPos)
                son.setNewCost(down)
                son.setGokuPos(down)
                sonManhattanDistance = son.calculateManhattanDistance(
                    self.ballPos)
                sonHeuristic = son.calculateHeuristic(sonManhattanDistance)
                son.setHeuristic(sonHeuristic)
                son.setSumCostHeuristic(son.getHeuristic() + son.getCost())
                son.moveDown(gokuPos)
                if (son.avoidGoBack2(down)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()

                    # print(son.getMarioPos(), "heurística: ", son.getHeuristic())

            # Check if up side is free
            if (not (gokuPos[0]-1 < 0) and currentNode.getState()[gokuPos[0]-1, gokuPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "up", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                up = son.upMovement(gokuPos)
                son.setNewCost(up)
                son.setGokuPos(up)
                sonManhattanDistance = son.calculateManhattanDistance(
                    self.ballPos)
                sonHeuristic = son.calculateHeuristic(sonManhattanDistance)
                son.setHeuristic(sonHeuristic)
                son.setSumCostHeuristic(son.getHeuristic() + son.getCost())
                son.moveUp(gokuPos)
                if (son.avoidGoBack2(up)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()

                    # print(son.getMarioPos(), "heurística: ", son.getHeuristic())

            stack.remove(currentNode)

            currentNode = self.getNodeMinSumCostHeuristic(stack)
            expandedNodes += 1
            gokuPos = currentNode.getGokuPos()
            # print("Mario pos:", marioPos)

        elapsedTime = process_time() - startTime
        elapsedTimeFormatted = "%.10f s." % elapsedTime
        self.setComputingTime(elapsedTimeFormatted)

        solution = currentNode.recreateSolutionWorld()
        solutionWorld = solution[::-1]
        print("Heurística meta: ", currentNode.getHeuristic())
        #print("Nodos expandidos: ", expandedNodes+1)  # Good
        #print("Profundidad: ", depth)
        #print("El costo final de la solución es: " + str(currentNode.getCost()))
        print(currentNode.recreateSolution())
        return [solutionWorld, expandedNodes+1, depth, currentNode.getCost()]
