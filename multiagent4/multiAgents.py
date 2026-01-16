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
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = successorGameState.getScore()

        foodList = newFood.asList()
        if foodList:
            minFoodDist = 99999
            for food in foodList:
                dist = manhattanDistance(newPos, food)
                if dist < minFoodDist:
                    minFoodDist = dist
            score += 15.0 / (minFoodDist + 1)

        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            dist = manhattanDistance(newPos, ghostPos)

            if ghostState.scaredTimer > 0:
                score += 8.0 / (dist + 1)
            else:
                if dist <= 1:
                    return -99999
                score -= 3.0 / (dist + 1)

        if action == Directions.STOP:
            score -= 10

        currentPos = currentGameState.getPacmanPosition()
        if newPos == currentPos:
            score -= 5

        reverse = Directions.REVERSE[currentGameState.getPacmanState().getDirection()]
        if action == reverse:
            score -= 3

        return score


def scoreEvaluationFunction(currentGameState: GameState):
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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState: GameState):
        bestScore = -99999
        bestAction = None

        for act in gameState.getLegalActions(0):
            next = gameState.generateSuccessor(0, act)
            val = self.minimax(next, 0, 1)
            if val > bestScore:
                bestScore = val
                bestAction = act
        return bestAction

    def minimax(self, state, depth, agentI):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        numAgents = state.getNumAgents()
        if agentI == 0:
            bestValue = -99999
            for act in state.getLegalActions(0):
                next = state.generateSuccessor(0, act)
                val = self.minimax(next, depth, 1)
                bestValue = max(bestValue, val)
            return bestValue

        else:
            bestValue = 99999
            nextAgent = agentI+ 1

            for action in state.getLegalActions(agentI):
                next = state.generateSuccessor(agentI, action)
                if nextAgent == numAgents:
                    value = self.minimax(next, depth +1, 0)
                else:
                    value = self.minimax(next, depth, nextAgent)
                bestValue = min(bestValue, value)

            return bestValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState: GameState):
        bestScore = -99999
        bestAction = None
        alpha = -99999
        beta = 99999

        for action in gameState.getLegalActions(0):
            next = gameState.generateSuccessor(0, action)
            value = self.alphabeta(next, 0, 1, alpha, beta)

            if value > bestScore:
                bestScore = value
                bestAction = action
            alpha = max(alpha, bestScore)

        return bestAction

    def alphabeta(self, state, depth, agentIndex, alpha, beta):
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        numAgents = state.getNumAgents()

        if agentIndex == 0:
            value = -99999
            for action in state.getLegalActions(0):
                successor = state.generateSuccessor(0, action)
                value = max(value, self.alphabeta(successor, depth, 1, alpha, beta))

                if value > beta:
                    return value
                alpha = max(alpha, value)
            return value

        else:
            value = 99999
            nextAgent = agentIndex +1

            for action in state.getLegalActions(agentIndex):
                next = state.generateSuccessor(agentIndex, action)

                if nextAgent == numAgents:
                    score = self.alphabeta(next, depth +1, 0, alpha, beta)
                else:
                    score = self.alphabeta(next, depth, nextAgent, alpha, beta)

                value = min(value, score)
                if value < alpha:
                    return value
                
                beta = min(beta, value)

            return value

    
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState: GameState):
        bestScore = -99999
        bestAction = None

        for action in gameState.getLegalActions(0):
            next = gameState.generateSuccessor(0, action)
            val = self.expectimax(next, 0,1)
            if val > bestScore:
                bestScore = val
                bestAction = action

        return bestAction
    
    def expectimax(self, state, depth, agentIndex):
        if state.isWin():
            return self.evaluationFunction(state)
        if state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)

        numAgents = state.getNumAgents()

        if agentIndex == 0:
            bestVal = -99999
            for action in state.getLegalActions(0):
                next = state.generateSuccessor(0, action)
                value = self.expectimax(next, depth, 1)
                bestVal = max(bestVal, value)
            return bestVal
        else:
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            probability = 1.0 / len(actions)
            expected = 0
            nextAgent = agentIndex + 1

            for action in actions:
                next = state.generateSuccessor(agentIndex, action)
                if nextAgent == numAgents:
                    value = self.expectimax(next, depth +1, 0)
                else:
                    value = self.expectimax(next, depth, nextAgent)
                expected += probability * value

            return expected


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    def betterEvaluationFunction(currentGameState: GameState):
        if currentGameState.isWin():
            return 99999
        if currentGameState.isLose():
            return -99999

        score = currentGameState.getScore()
        pacmanPos = currentGameState.getPacmanPosition()
        food = currentGameState.getFood().asList()
        ghostStates = currentGameState.getGhostStates()
        capsules = currentGameState.getCapsules()

        if food:
            minFoodDist = min(manhattanDistance(pacmanPos, f) for f in food)
            score += 10.0 / (minFoodDist + 1)

        score -= 4 * len(food)
        score -= 15 * len(capsules)

        for ghost in ghostStates:
            ghostPos = ghost.getPosition()
            dist = manhattanDistance(pacmanPos, ghostPos)

            if ghost.scaredTimer > 0:
                score += 20.0 / (dist + 1)
            else:
                if dist <= 1:
                    return -999999
                score -= 6.0 / (dist + 1)
                
        return score

# Abbreviation
better = betterEvaluationFunction
