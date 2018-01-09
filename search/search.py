#coding:UTF-8
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

def depthFirstSearch(problem):
    actions = []                 #存储路径
    visited = set()              #标记已访问结点
    travel = util.Stack()        #访问的过程
    succ = {}                    #存储调用getSuccessors的结果
    currentState = problem.getStartState()
    travel.push((currentState,None,0))
    visited.add(currentState)
    while(not problem.isGoalState(currentState)):
        if currentState not in succ:
            successors = problem.getSuccessors(currentState)
        else:
            successors = succ[currentState]
        unvisitedNode = [success for success in successors if success[0] not in visited]
        succ[currentState] = unvisitedNode
        while(len(unvisitedNode)==0):
            travel.pop()
            if travel.isEmpty():        #not find the way
                raise Exception("can not find the way to the goal.")
            currentNode = travel.pop()
            travel.push(currentNode)
            if currentNode[0] not in succ:
                successors = problem.getSuccessors(currentNode[0])
            else :
                successors = succ[currentNode[0]]
            unvisitedNode = [success for success in successors if success[0] not in visited]
            succ[currentNode[0]] = unvisitedNode
        currentState = unvisitedNode[0][0]
        travel.push(unvisitedNode[0])
        visited.add(currentState)
    currentAction = travel.pop()[1]
    while(not travel.isEmpty()):
        actions.append(currentAction)
        currentAction = travel.pop()[1]
    actions.reverse()
    return actions

def breadthFirstSearch(problem):
    currentState = problem.getStartState()
    connection = {}               #存储路径
    visited = set()               #存储已访问结点
    travel = util.Queue()         #存储访问的过程
    visited.add(currentState)
    while(not problem.isGoalState(currentState)):
        successors = problem.getSuccessors(currentState)
        for success in successors:
            if success[0] not in visited:      #处理每一个未访问的临结点
                travel.push(success[0])
                connection[success[0]] = (currentState, success[1])
                visited.add(success[0])
        if travel.isEmpty():
            raise Exception("can not find the way to the goal.")
        currentState = travel.pop()
    #find the way
    actions =[]
    while(currentState != problem.getStartState()):
        currentNode = connection[currentState]
        actions.append(currentNode[1])
        currentState = currentNode[0]
    actions.reverse()
    return actions

def uniformCostSearch(problem):
    queue = util.PriorityQueue()     #优先队列存储待访问结点
    connect = {}                     #存储路径
    visited = set()                  #存储已访问结点
    currentState = problem.getStartState()
    connect[currentState] = (0,0,0)
    queue.push(currentState, 0)
    while(not queue.isEmpty()):
        currentState = queue.pop()
        if currentState not in visited:            #处理当前带访问结点中权值最小的，且未访问的节点
            visited.add(currentState)
            if problem.isGoalState(currentState):     #找到目标结点
                break
            successors = problem.getSuccessors(currentState)
            for success in successors:
                if success[0] not in visited:     #处理此节点邻接未被访问的结点
                    if success[0] not in connect:    #更新结点路径信息
                        connect[success[0]] = (currentState, success[1], success[2]+connect[currentState][2])
                    elif connect[success[0]][2] > (connect[currentState][2] + success[2]):
                        connect[success[0]] = (currentState, success[1], connect[currentState][2]+success[2])
                    queue.update(success[0], connect[success[0]][2])
    if not problem.isGoalState(currentState):
        raise Exception("can no t find the way to the goal.")
    #find the way
    actions = []
    while currentState != problem.getStartState():
        actions.append(connect[currentState][1])
        currentState = connect[currentState][0]
    actions.reverse()
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    queue = util.PriorityQueue()     #优先队列存储待访问的节点
    visited = set()                  #存储已访问节点
    path = {}                        #存储路径
    currentState = problem.getStartState()
    queue.push(currentState, heuristic(currentState, problem))    #处理初始状态
    path[currentState] = (0,0,0)
    while not queue.isEmpty():
        currentState = queue.pop()
        if currentState not in visited:
            visited.add(currentState)
            if problem.isGoalState(currentState):
                break
            successors = problem.getSuccessors(currentState)
            for successor in successors:
                if successor[0] not in visited:
                    currentCost = path[currentState][2] + successor[2] + heuristic(successor[0], problem)
                    if successor[0] not in path:    #更新结点路径信息
                        path[successor[0]] = (currentState, successor[1], successor[2]+path[currentState][2],currentCost)
                    elif path[successor[0]][3] > currentCost:
                        path[successor[0]] = (currentState, successor[1], path[currentState][2]+successor[2], currentCost)
                    queue.update(successor[0], path[successor[0]][3])
    if not problem.isGoalState(currentState):
        raise Exception("can not fing the way to the goal.")
    actions = []
    while currentState != problem.getStartState():
        actions.append(path[currentState][1])
        currentState = path[currentState][0]
    actions.reverse()
    return actions




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
