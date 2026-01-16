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

from game import Actions
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
        MAX = 999999
        if actions is None:
            return MAX

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x = int(x + dx)
            y = int(y + dy)

            if self.walls[x][y]:
                return MAX

        return len(actions)


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()  # obținem starea de start

    # dacă startul este deja o stare goal (țintă), returnăm lista goală
    if problem.isGoalState(start):
        return []

    frontier = util.Stack()  # stiva frontieră (conține stări de explorat)
    # fiecare element din frontieră este un tuplu: (stare_curentă, listă_acțiuni)
    frontier.push((start, []))
    explored = set()  # mulțime pentru a ține evidența stărilor deja vizitate

    # cât timp avem stări neexplorate în frontieră
    while not frontier.isEmpty():
        state, path = frontier.pop()  # extragem ultima stare adăugată (LIFO)

        # dacă am mai vizitat această stare, o ignorăm
        if state in explored:
            continue
        explored.add(state)  # marcăm starea ca vizitată

        # verificăm dacă am ajuns la scop
        if problem.isGoalState(state):
            return path  # returnăm calea acțiunilor până aici

        # pentru fiecare succesor al stării curente
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in explored:
                # adăugăm succesorul în frontieră, cu calea actualizată
                frontier.push((successor, path + [action]))

    # dacă nu s-a găsit niciun drum
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []

    frontier = util.Queue()  # coadă pentru explorare strat cu strat
    frontier.push((start, []))  # adăugăm starea de start și calea goală
    explored = set()  # stări deja vizitate
    frontier_set = {start}  # ținem o copie a frontierii pentru eficiență

    while not frontier.isEmpty():
        state, path = frontier.pop()  # extragem prima stare adăugată (FIFO)
        frontier_set.discard(state)   # o eliminăm din setul frontierii

        if state in explored:
            continue
        explored.add(state)

        if problem.isGoalState(state):
            return path  # am găsit drumul către scop

        for successor, action, stepCost in problem.getSuccessors(state):
            # adăugăm doar stările care nu sunt vizitate sau deja în frontieră
            if successor not in explored and successor not in frontier_set:
                frontier.push((successor, path + [action]))
                frontier_set.add(successor)

    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []

    frontier = util.PriorityQueue()
    # în frontieră reținem tupluri: (stare, cale, cost_total)
    frontier.push((start, [], 0), 0)  # prioritatea este costul total (g)
    best_cost = {start: 0}  # dicționar pentru costul minim cunoscut al fiecărei stări

    while not frontier.isEmpty():
        state, path, cost = frontier.pop()  # extragem starea cu cost minim

        # dacă avem deja un drum mai ieftin către această stare, o ignorăm
        if state in best_cost and cost > best_cost[state]:
            continue

        # dacă am ajuns la scop, returnăm calea
        if problem.isGoalState(state):
            return path

        # generăm succesorii stării curente
        for successor, action, stepCost in problem.getSuccessors(state):
            new_cost = cost + stepCost  # actualizăm costul total până la succesor

            # verificăm dacă avem un drum mai bun (mai ieftin) către succesor
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost  # actualizăm costul minim cunoscut
                # inserăm succesorul în frontieră cu prioritate = cost_total
                frontier.push((successor, path + [action], new_cost), new_cost)

    # dacă nu s-a găsit nicio soluție
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []

    frontier = util.PriorityQueue()
    g_start = 0  # costul de la start până la nodul curent
    f_start = g_start + heuristic(start, problem)  # valoarea totală f = g + h
    # fiecare element: (stare, cale, cost_g)
    frontier.push((start, [], g_start), f_start)

    best_g = {start: 0}  # dicționar cu cel mai bun cost g pentru fiecare stare

    while not frontier.isEmpty():
        state, path, g = frontier.pop()

        # dacă am găsit un drum mai ieftin ulterior, ignorăm acest nod
        if state in best_g and g > best_g[state]:
            continue

        # verificăm dacă am ajuns la scop
        if problem.isGoalState(state):
            return path

        # explorăm succesorii
        for successor, action, stepCost in problem.getSuccessors(state):
            new_g = g + stepCost  # noul cost g pentru succesor

            # verificăm dacă e o cale mai ieftină decât cea cunoscută
            if successor not in best_g or new_g < best_g[successor]:
                best_g[successor] = new_g  # actualizăm costul g minim
                f = new_g + heuristic(successor, problem)  # calculăm noul f = g + h
                # inserăm succesorul cu prioritate egală cu f
                frontier.push((successor, path + [action], new_g), f)

    return []  # dacă nu am găsit soluție


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
