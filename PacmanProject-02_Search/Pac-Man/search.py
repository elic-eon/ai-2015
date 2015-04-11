# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

"P2-1"
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "[Project 2] YOUR CODE HERE"
    visitedPositions = [problem.getStartState()]
    positionStack = [(problem.getStartState(), None, 1)]
    degreeStack = [0]
    directionStack = []
    while not problem.isGoalState(positionStack[-1][0]):
        successors = problem.getSuccessors(positionStack[-1][0])
        degree = 0
        
        for successor in successors:
            if successor[0] not in visitedPositions:
                positionStack.append(successor)
                degree += 1

        if degree == 0:
            positionStack.pop()
            directionStack.pop()
        else:
            degreeStack.append(degree)
            
        while degreeStack[-1] == 0:
            positionStack.pop()
            degreeStack.pop()
            directionStack.pop()

        degreeStack[-1] -= 1
        directionStack.append(positionStack[-1][1])
        visitedPositions.append(positionStack[-1][0])
                
    return directionStack

"P2-2"
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "[Project 2] YOUR CODE HERE"
    visitedPositions = [problem.getStartState()]
    positionQueue = [(problem.getStartState(), None, 1, 0)]
    position = 0;
    while not problem.isGoalState(positionQueue[position][0]):
        successors = problem.getSuccessors(positionQueue[position][0])
        
        for successor in successors:
            if successor[0] not in visitedPositions:
                visitedPositions.append(successor[0])
                positionQueue.append(successor + (position,))

        position += 1
    
    directions = []
    
    while position != 0:
        directions.insert(0, positionQueue[position][1])
        position = positionQueue[position][3]
        
    return directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

"P2-3"
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "[Project 2] YOUR CODE HERE"
    path = []
    visited = []
    pq = util.PriorityQueue()
    pq.push((problem.getStartState(), path), 0 + heuristic(problem.getStartState(), problem))
    while pq.isEmpty() != 1:
        lowest, path = pq.pop()
        if problem.isGoalState(lowest):
            return path
        states = problem.getSuccessors(lowest)
        for state in states:
            if state[0] not in visited:
                newpath = path + [state[1]]
                pq.push((state[0], newpath), problem.getCostOfActions(newpath) + heuristic(state[0], problem))
                visited += [state[0]]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
