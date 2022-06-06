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

from builtins import object
import util


class SearchProblem(object):
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
	return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):

	# The fringe in DFS is a stack; therefore we define it as such.
	fringe = util.Stack()

	# We also need a stack for to store the paths we traversed to get to a specific node. Since we push into this stack
	# and fringe simultaneously, the path popped from paths_stack is associated to the node we pop.
	paths_stack = util.Stack()

	# We define a set in order to prevent the nodes we have already expanded from expanding again.
	visited = set()

	start_state = problem.getStartState()
	fringe.push(start_state)

	# There is no node before the start node, thus we push an empty list.
	paths_stack.push([])

	while not fringe.isEmpty():
		current_state = fringe.pop()
		actions = paths_stack.pop()

		# We check if the state is already expanded or not.
		if current_state not in visited:
			# If not, we expand it and add it to the set.
			visited.add(current_state)
			# If it is the goal state, we have reached the end; so we return the path we took to get to the goal state.
			if problem.isGoalState(current_state):
				return actions
			# if not, we add its successor to the stack.
			else:
				successors = problem.getSuccessors(current_state)
				for successor_state, successor_action, successor_cost in successors:
					new_action = actions + [successor_action]
					fringe.push(successor_state)
					paths_stack.push(new_action)

	# If we never reached the goal state, we return failure.
	util.raiseNotDefined()


def breadthFirstSearch(problem):

	# The fringe in BFS is a queue; therefore we define it as such.
	fringe = util.Queue()

	# We also need a queue for to store the paths we traversed to get to a specific node. Since we push into this queue
	# and fringe simultaneously, the path popped from paths_queue is associated to the node we pop.
	paths_queue = util.Queue()

	# We define a set in order to prevent the nodes we have already expanded from expanding again.
	visited = set()

	start_state = problem.getStartState()
	fringe.push(start_state)

	# There is no node before the start node, thus we push an empty list.
	paths_queue.push([])
	
	while not fringe.isEmpty():
		current_state = fringe.pop()
		actions = paths_queue.pop()

		# We check if the state is already expanded or not.
		if current_state not in visited:
			# If not, we expand it and add it to the set.
			visited.add(current_state)
			# If it is the goal state, we have reached the end; so we return the path we took to get to the goal state.
			if problem.isGoalState(current_state):
				return actions
			# if not, we add its successor to the fringe.
			else:
				successors = problem.getSuccessors(current_state)
				for successor_state, successor_action, successor_cost in successors:
					new_action = actions + [successor_action]
					fringe.push(successor_state)
					paths_queue.push(new_action)

	# If we never reached the goal state, we return failure.
	util.raiseNotDefined()


def uniformCostSearch(problem, heuristic=None):

	# The fringe in UCS is a heap; therefore we define it as such.
	# But unlike the last two search algorithms, in UCS, we put nodes and their priority into the fringe
	# and do not take multiple instances of a data structure.
	# A node in this case, is a 3-tuple of the state we are at, the path we took to get here, and the cost we paid.
	# Therefore a node is of form (state, path, cost).
	# And each element of fringe is of form (node, cost).
	fringe = util.PriorityQueue()

	# We define a dictionary in order to keep record of the nodes we have visited.
	# This dictionary maps a state to the cost we paid to reach it.
	# Thus it's on form {state: cost}.
	visited = {}

	start_state = problem.getStartState()

	# There is no node before the start node, thus the emtpy list. And no cost neither, thus the zero.
	start_node = (start_state, [], 0)

	# Thus we push the start node into the fringe with priority of its cost, which is zero.
	fringe.push(start_node, 0)
	while not fringe.isEmpty():

		# 'pop' in heaps returns the value with the lowest-priority.
		current_state, actions, current_cost = fringe.pop()

		# Checking if we have not expanded the node OR whether we have reached this state before but the cost of the
		# current path we took to reach it is lower.
		if (current_state not in visited.keys()) or (current_cost < visited[current_state]):
			# If so, we add this node to our dictionary or update its value if it already exists.
			visited[current_state] = current_cost

			# If it is the goal state, we have reached the end; so we return the path we took to get to the goal state.
			if problem.isGoalState(current_state):
				return actions

			# if not, we add its successor to the fringe.
			else:
				successors = problem.getSuccessors(current_state)
				for successor_state, successor_action, successor_cost in successors:
					new_action = actions + [successor_action]
					new_cost = current_cost + successor_cost
					new_node = (successor_state, new_action, new_cost)

					fringe.update(new_node, new_cost)

	# If we never reached the goal state, we return failure.
	util.raiseNotDefined()


def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0


def aStarSearch(problem, heuristic=nullHeuristic):

	# The fringe in A* search is a heap; therefore we define it as such.
	# This is identical to UCS.
	# A node in this case, is a 3-tuple of the state we are at, the path we took to get here, and the cost we paid.
	# Therefore a node is of form (state, path, cost).
	# And each element of fringe is of form (node, cost).
	fringe = util.PriorityQueue()

	# We define a dictionary in order to keep record of the nodes we have visited.
	# This dictionary maps a state to the cost we paid to reach it.
	# Thus it's on form {state: cost}.
	visited = {}

	start_state = problem.getStartState()

	# There is no node before the start node, thus the emtpy list. And no cost neither, thus the zero.
	start_node = (start_state, [], 0)

	# Thus we push the start node into the fringe with priority of its cost, which is zero.
	fringe.push(start_node, 0)
	while not fringe.isEmpty():
		current_state, actions, current_cost = fringe.pop()

		# Checking if we have not expanded the node OR whether we have reached this state before but the cost of the
		# current path we took to reach it is lower.
		if (current_state not in visited.keys()) or (current_cost < visited[current_state]):

			# If so, we add this node to our dictionary or update its value if it already exists.
			visited[current_state] = current_cost

			# If it is the goal state, we have reached the end; so we return the path we took to get to the goal state.
			if problem.isGoalState(current_state):
				return actions

			# if not, we add its successor to the fringe.
			else:
				successors = problem.getSuccessors(current_state)
				for successor_state, successor_action, successor_cost in successors:
					new_action = actions + [successor_action]
					new_cost = current_cost + successor_cost
					new_node = (successor_state, new_action, new_cost)

					# A* uses both cost and heuristic. This is one of the differences between A* and UCS.
					# In A*, priority is g(n) + h(n); where g(n) is the cost and h(n) is the heuristic.
					fringe.push(new_node, new_cost + heuristic(successor_state, problem))

	# If we never reached the goal state, we return failure.
	util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
