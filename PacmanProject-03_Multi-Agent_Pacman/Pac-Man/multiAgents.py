# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from util import matrixAsList
from game import Directions
import random, util
import math

from game import Agent

"P3-1"
class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print (scores)
        #raw_input()
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        pts = 0
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        curPos = currentGameState.getPacmanPosition()
        FoodList = currentGameState.getFood().asList()
        nearestFood = FoodList[0]
        nearest = manhattanDistance(curPos, FoodList[0])
        for food in FoodList:
            tDist = manhattanDistance(curPos, food)
            if tDist < nearest:
                nearestFood = food
                nearest = tDist


        newPos = successorGameState.getPacmanPosition()
        newFoodDist = manhattanDistance(newPos, nearestFood)
        foodDistDiff = nearest - newFoodDist

        if newPos in FoodList:
            pts += 10

        ghostPos = currentGameState.getGhostPosition(1)
        curDist = manhattanDistance(curPos, ghostPos)
        newDist = manhattanDistance(newPos, ghostPos)
        ghostDistDiff = newDist - curDist
        isNear = 1 if curDist < 4 else 0
        pts += ghostDistDiff * isNear * 20 + foodDistDiff

        "[Project 3] YOUR CODE HERE"
        
        return pts

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

"P3-2"
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "[Project 3] YOUR CODE HERE"

        actionsList = []
        score, choice, actionsList = self.minimax(gameState, self.depth, 0, actionsList)
        #print(self.depth)
        #print(choice)
        #print(score)
        #print(actionsList)
        #raw_input()
        return choice

    def minimax(self, nodeState, depth, playerIndex, actionsList):
        if depth == 0 and playerIndex == 1:
            return (self.evaluationFunction(nodeState), None, actionsList)
        if playerIndex == 0:
            actions = nodeState.getLegalActions(playerIndex)
            #print("depth: " + str(depth))
            #print(actionsList)
            if len(actions) == 0:
                return (self.evaluationFunction(nodeState), None, actionsList)
            vals = [self.minimax(nodeState.generateSuccessor(playerIndex, action), \
                    depth-1, nodeState.getNumAgents()-1, actionsList + [action]) for action in actions]
            #if depth == 4:
                #print(actions)
                #print(vals)
            maxval = max(vals, key=lambda item:item[0])[0]
            actionIndex = [index for index in range(len(vals)) if vals[index][0] == maxval]
            if len(actionIndex) > 1:
                for index in actionIndex:
                    if actions[index] == Directions.STOP:
                        actionIndex.remove(index)
                        break
                index = random.choice(actionIndex)
                return (maxval, actions[index], vals[index][2])
            else:
                return (maxval, actions[actionIndex[0]], vals[actionIndex[0]][2])
        else:
            actions = nodeState.getLegalActions(playerIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(nodeState), None, actionsList)
            vals = [self.minimax(nodeState.generateSuccessor(playerIndex, action), \
                    depth, playerIndex-1, actionsList) for action in actions]
            return min(vals, key=lambda item:item[0])

"P3-3"
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        "[Project 3] YOUR CODE HERE"        

        actionsList = []
        score, choice, actionsList = self.alpha_beta(gameState, self.depth, 0, actionsList, float("-inf"), float("inf"))
        #print(score)
        #print(actionsList)
        #raw_input()
        return choice
        
    def alpha_beta(self, nodeState, depth, playerIndex, actionsList, alpha, beta):
        if depth == 0 and playerIndex == 1:
            #print("depth: " + str(depth))
            #print(actionsList)
            #print("score: " + str(self.evaluationFunction(nodeState)))
            return (self.evaluationFunction(nodeState), None, actionsList)
        if playerIndex == 0:
            actions = nodeState.getLegalActions(playerIndex)
            if len(actions) == 0:
                #print("depth: " + str(depth))
                #print(actionsList)
                #print("score: " + str(self.evaluationFunction(nodeState)))
                return (self.evaluationFunction(nodeState), None, actionsList)
            vals = []
            for action in actions:
                val = self.alpha_beta(nodeState.generateSuccessor(playerIndex, action), \
                        depth-1, nodeState.getNumAgents()-1, actionsList+[action], alpha, beta)
                vals += [val]
                alpha = max(alpha, val[0])
                if beta < alpha:
                    break
            maxval = max(vals, key=lambda item:item[0])[0]
            actionIndex = [index for index in range(len(vals)) if vals[index][0] == maxval]
            if len(actionIndex) > 1:
                for index in actionIndex:
                    if actions[index] == Directions.STOP:
                        actionIndex.remove(index)
                        break
                index = random.choice(actionIndex)
                return (maxval, actions[index], vals[index][2])
            else:
                return (maxval, actions[actionIndex[0]], vals[actionIndex[0]][2])
        else:
            actions = nodeState.getLegalActions(playerIndex)
            if len(actions) == 0:
                return (self.evaluationFunction(nodeState), None, actionsList)
            vals = []
            for action in actions:
                val = self.alpha_beta(nodeState.generateSuccessor(playerIndex, action), \
                        depth, playerIndex-1, actionsList, alpha, beta)
                vals += [val]
                beta = min(beta, val[0])
                if beta < alpha:
                    break
            return min(vals, key=lambda item:item[0])

"P3-4 Side Mission (optional)"
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        
        "*** YOUR CODE HERE ***"
        
        util.raiseNotDefined()

"P3-4"
def foodBFS(currentGameState):
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    curPos = currentGameState.getPacmanPosition()
    visited = []
    foodList = currentGameState.getFood().asList()
    nodeQueue = util.Queue()
    nodeQueue.push((curPos, 0))

    while not nodeQueue.isEmpty():
        node, d = nodeQueue.pop()
        visited += [node]
        for direction in directions:
            newPos = (node[0] + direction[0], node[1] + direction[1])
            if currentGameState.hasWall(newPos[0], newPos[1]):
                continue
            else:
                if newPos not in visited:
                    nodeQueue.push((newPos, d+1))
                if newPos in foodList:
                    return (newPos, d+1)
    return (None, float("inf"))


#def betterEvaluationFunction(currentGameState):
    #"""
      #Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      #evaluation function.

      #DESCRIPTION: <write something here so we know what you did>
    #"""
    
    #"[Project 3] YOUR CODE HERE"

    #foodList = currentGameState.getFood().asList()
    #curPos = currentGameState.getPacmanPosition()
    #nearFoodPos, nearFoodDist = foodBFS(currentGameState)
    ##print(curPos)
    ##print(nearFoodPos)
    ##print(nearFoodDist)
    ##raw_input()
    
    #return scoreEvaluationFunction(currentGameState) + 1/nearFoodDist
    #util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function.

      DESCRIPTION: <write something here so we know what you did>
    """
    
    "[Project 3] YOUR CODE HERE"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    
    # get the number of capsules left
    numOfCapsule = len(currentGameState.getCapsules())
    # calculate the distance to the closest ghost and the distance to any intersection
    
    #forkDist, forkPos = ForkDist(currentGameState)
    #ghostDist = GhostDistPos(currentGameState, forkPos)
    if GhostSafety(currentGameState): safety = 1000
    else: safety = 0
    
    # calculate the distance to the closest food
    foodDist = FoodDist(currentGameState)
    
    return score*10 - foodDist - 300*numOfCapsule + safety
    
def GhostSafety(currentGameState):
    forkList = ForkList(currentGameState)
    ghostStates = currentGameState.getGhostStates()
    
    if not forkList: return True
    
    threat = 0
    for ghostState in ghostStates:
        for point in forkList:
            dist = BFS(currentGameState, ghostState.getPosition(), point[0])
            if ghostState.scaredTimer > dist: continue
            if dist < point[1]: 
                threat += 1
                break
    
    if threat >= len(forkList): return False
    else: return True

def ForkList(currentGameState):
    '''
    The distance to the nearest fork points
    '''
    ret = []
    pacmanPos = currentGameState.getPacmanPosition()
    walls = currentGameState.getWalls()
    
    visitedPositions = [pacmanPos]
    positionQueue = [(pacmanPos, 0)]
    
    if posDegree(currentGameState, pacmanPos) >= 3: return ret
    while positionQueue:
        pos = positionQueue[0][0]
        depth = positionQueue[0][1]
        
        for nextPos in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if walls[nextPos[0]][nextPos[1]]: continue
            if nextPos in visitedPositions: continue
            degree = posDegree(currentGameState, nextPos)
            if degree >= 3:
                ret.append((nextPos, depth+1))
            else:
                positionQueue.append( (nextPos, depth+1) )
                visitedPositions.append( nextPos )
        
        positionQueue.pop(0)
        
    return ret
    
def posDegree(currentGameState, pos):
    '''
    The degree of a given position
    '''
    walls = currentGameState.getWalls()
    degree = 0
    for nextPos in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
        if not walls[nextPos[0]][nextPos[1]]:
            degree += 1
    return degree
    
def FoodDist(currentGameState):
    '''
    Calculate the steps required to get to the nearest food
    '''
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    walls = currentGameState.getWalls()
    
    visitedPositions = [pacmanPos]
    positionQueue = [(pacmanPos, 0)]
    
    while positionQueue:
        pos = positionQueue[0][0]
        depth = positionQueue[0][1]
        
        for nextPos in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if food[nextPos[0]][nextPos[1]]:
                return depth+1;
            if (nextPos not in visitedPositions) and (not walls[nextPos[0]][nextPos[1]]):
                positionQueue.append( (nextPos, depth+1) )
                visitedPositions.append( nextPos )
        
        positionQueue.pop(0)
        
    return 0
    
def BFS(currentGameState, start, target):
    '''
    The distance between 'start' and 'target'
    '''
    #for action in state.getLegalActions():
    walls = currentGameState.getWalls()
    start = (int(start[0]), int(start[1]))
    visitedPositions = [start]
    positionQueue = [(start, 0)]
    
    while positionQueue:
        pos = positionQueue[0][0]
        depth = positionQueue[0][1]
        
        for nextPos in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
            if nextPos == target:
                return depth+1;
            if (nextPos not in visitedPositions) and (not walls[nextPos[0]][nextPos[1]]):
                positionQueue.append( (nextPos, depth+1) )
                visitedPositions.append( nextPos )
        
        positionQueue.pop(0)
        
    return 100



# Abbreviation
better = betterEvaluationFunction

