from node import Node
from time import process_time


class DepthAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0)
        self.gokuPos = self.firstNode.searchForGoku()
        self.stack = [self.firstNode]
        self.computingTime = ""

    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def start(self):
        startTime = process_time()

        stack = self.stack
        gokuPos = self.gokuPos
        currentNode = stack[0]
        expandedNodes = 0
        depth = 0

        while not (currentNode.isGoal()):
            # print("---")
            # print(currentNode.getMarioPos())
            stack.pop(0)
            expandedNodes += 1

            # Check if right side is free
            if (not (gokuPos[1]+1 > 9) and currentNode.getState()[gokuPos[0], gokuPos[1]+1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "right", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                right = son.rightMovement(gokuPos)
                son.setNewCost(right)
                son.setGokuPos(right)
                son.moveRight(gokuPos)
                if (son.compareCicles2(right)):
                    stack.insert(0, son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()
                    # print(son.getMarioPos())

            # Check if left side is free
            if (not (gokuPos[1]-1 < 0) and currentNode.getState()[gokuPos[0], gokuPos[1]-1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "left", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                left = son.leftMovement(gokuPos)
                son.setNewCost(left)
                son.setGokuPos(left)
                son.moveLeft(gokuPos)
                if (son.compareCicles2(left)):
                    stack.insert(0, son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()
                    # print(son.getMarioPos())

            # Check if down side is free
            if (not (gokuPos[0]+1 > 9) and currentNode.getState()[gokuPos[0]+1, gokuPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "down", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                down = son.downMovement(gokuPos)
                son.setNewCost(down)
                son.setGokuPos(down)
                son.moveDown(gokuPos)
                if (son.compareCicles2(down)):
                    stack.insert(0, son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()
                    # print(son.getMarioPos())

            # Check if up side is free
            if (not (gokuPos[0]-1 < 0) and currentNode.getState()[gokuPos[0]-1, gokuPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "up", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getCell(), currentNode.getSeed())

                up = son.upMovement(gokuPos)
                son.setNewCost(up)
                son.setGokuPos(up)
                son.moveUp(gokuPos)
                if (son.compareCicles2(up)):
                    stack.insert(0, son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()
                    # print(son.getMarioPos())

            currentNode = stack[0]
            gokuPos = currentNode.getGokuPos()

        elapsedTime = process_time() - startTime
        elapsedTimeFormatted = "%.10f s." % elapsedTime
        self.setComputingTime(elapsedTimeFormatted)

        solution = currentNode.recreateSolutionWorld()
        solutionWorld = solution[::-1]
        #print("Nodos expandidos: ", expandedNodes+1)  # Good
        #print("Profundidad: ", depth)
        #print("Costo solución: " + str(currentNode.getCost()))
        print(currentNode.recreateSolution())
        return [solutionWorld, expandedNodes+1, depth, currentNode.getCost()]
