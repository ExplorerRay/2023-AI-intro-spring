from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
         # len(scores) == len(legalMoves)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition() # now position
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)

        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        scores = [self.min_vl(1, 0, gameState.getNextState(0, action)) for action in legalMoves]
        bestScore = max(scores)
        bestIndex = [index for index in range(len(scores)) if scores[index] == bestScore][0]
        return legalMoves[bestIndex]


    def max_vl(self, dep, GS):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)

        ls = []
        act_ls = GS.getLegalActions(0)
        for ac in act_ls:
            ls.append(self.min_vl(1, dep, GS.getNextState(0, ac)))
        return max(ls)

    def min_vl(self, ag, dep, GS):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)

        ls = []
        act_ls = GS.getLegalActions(ag)
        if ag == GS.getNumAgents() - 1: # last ghost
            for ac in act_ls:
                ls.append(self.max_vl(dep+1, GS.getNextState(ag, ac)))
            return min(ls)
        else:
            for ac in act_ls:
                ls.append(self.min_vl(ag+1, dep, GS.getNextState(ag, ac)))
            return min(ls)

         # isWin() means eating all foods
         # isLose() means being hit by the ghost

        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)

        alpha = float('-inf')
        beta = float('inf')
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        bestScore = float('-inf')
        for act in legalMoves:
            bestScore = self.min_ab(1, 0, gameState.getNextState(0, act), alpha, beta)
            if(bestScore > alpha):
                alpha = bestScore
                bestAct = act
        return bestAct
    

    def min_ab(self, ag, dep, GS, alpha, beta):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)
        
        vl = float('inf')
        act_ls = GS.getLegalActions(ag)
        if ag == GS.getNumAgents() - 1:
            for ac in act_ls:
                vl = min(vl, self.max_ab(dep+1, GS.getNextState(ag, ac), alpha, beta))
                beta = min(beta, vl)
                if alpha > beta:
                    break
        else:
            for ac in act_ls:
                vl = min(vl, self.min_ab(ag+1, dep, GS.getNextState(ag, ac), alpha, beta))
                beta = min(beta, vl)
                if alpha > beta:
                    break
        return vl

    def max_ab(self, dep, GS, alpha, beta):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)

        vl = float('-inf')
        act_ls = GS.getLegalActions(0)
        for ac in act_ls:
            vl = max(vl, self.min_ab(1, dep, GS.getNextState(0, ac), alpha, beta))
            alpha = max(alpha, vl)
            if alpha > beta:
                break
        return vl
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)

        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions
        scores = [self.min_ex(1, 0, gameState.getNextState(0, action)) for action in legalMoves]
        bestScore = max(scores)
        bestIndex = [index for index in range(len(scores)) if scores[index] == bestScore][0]
        return legalMoves[bestIndex]

    def max_ex(self, dep, GS):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)

        ls = []
        act_ls = GS.getLegalActions(0)
        for ac in act_ls:
            ls.append(self.min_ex(1, dep, GS.getNextState(0, ac)))
        return max(ls)

    def min_ex(self, ag, dep, GS):
        if GS.isWin() or GS.isLose() or dep == self.depth:
            return self.evaluationFunction(GS)

        sum = 0
        act_ls = GS.getLegalActions(ag)
        if ag == GS.getNumAgents() - 1:
            for ac in act_ls:
                sum = sum + self.max_ex(dep+1, GS.getNextState(ag, ac))
            return sum
        else:
            for ac in act_ls:
                sum = sum + self.min_ex(ag+1, dep, GS.getNextState(ag, ac))
            return sum
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)

    # get all info from current state
    nw_pos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates() 
    foods = currentGameState.getFood()
    capsules = currentGameState.getCapsules()

    # get min dist to capsule
    capDistList = []
    for cp in capsules:
        capDistList.append(manhattanDistance(cp, nw_pos))
    if capDistList != []:
        minCapDist = min(capDistList)
    else:
        minCapDist = 0

    # get min dist to food
    foodDistList = []
    for fd in foods.asList():
        foodDistList.append(manhattanDistance(fd, nw_pos))
    if foodDistList != []:
        minFoodDist = min(foodDistList)
    else:
        minFoodDist = 0
    
    # divide ghosts into not-scared and scared
    ghostDistList = []
    scaredGhostDistList = []
    for gst in ghosts:
        if gst.scaredTimer >= 10:
            scaredGhostDistList.append(manhattanDistance(nw_pos, gst.getPosition()))
        else:
            ghostDistList.append(manhattanDistance(nw_pos, gst.getPosition()))
    # get min dist to ghost and scared ghost
    minGhostDist = 0
    if len(ghostDistList) > 0:
        minGhostDist = min(ghostDistList)
    minScaredGhostDist = 0
    if len(scaredGhostDistList) > 0:
        minScaredGhostDist = min(scaredGhostDistList)

    # init to score now
    score = currentGameState.getScore()

    # determine the weight of dist to closest food
    # more close, score be higher
    score = score + (-1 * minFoodDist)
    score = score + (-1 * minCapDist)

    # determine the weight of dist to closest ghost
    if minGhostDist != 0:
        score = score + (-2 * (1.0 / minGhostDist))
    # determine the weight of dist to closest scared ghost
    score = score + (-1 * minScaredGhostDist)

    # the more remaining food and capsule, the lower the score is
    score = score + (-20 * len(capsules))
    score = score + (-5 * len(foods.asList()))

    return score  
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
