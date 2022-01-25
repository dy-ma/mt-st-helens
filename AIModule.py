from codecs import getincrementalencoder
from copy import deepcopy
from queue import PriorityQueue
from sys import maxsize
from Point import Point
import math

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''
class AIModule:

	def createPath(self, map_):
		pass

'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''
class StupidAI(AIModule):

	def createPath(self, map_):
		path = []
		explored = []
		# Get starting point
		path.append(map_.start)
		current_point = deepcopy(map_.start)

		# Keep moving horizontally until we match the target
		while(current_point.x != map_.goal.x):
			# If we are left of goal, move right
			if current_point.x < map_.goal.x:
				current_point.x += 1
			# If we are right of goal, move left
			else:
				current_point.x -= 1
			path.append(deepcopy(current_point))

		# Keep moving vertically until we match the target
		while(current_point.y != map_.goal.y):
			# If we are left of goal, move right
			if current_point.y < map_.goal.y:
				current_point.y += 1
			# If we are right of goal, move left
			else:
				current_point.y -= 1
			path.append(deepcopy(current_point))

		# We're done!
		return path

class Djikstras(AIModule):

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarExp(AIModule):
	def h(self, map_, start):
		# get goal
		goal = map_.goal
		# get distances
		y_dist = abs(goal.y - start.y)
		x_dist = abs(goal.x - start.x)
		# get height difference
		goal_height = map_.getTile(goal.x, goal.y)
		start_height = map_.getTile(start.x, start.y)
		delta_h = goal_height - start_height
		# min steps
		s = min(x_dist, y_dist) + abs(y_dist - x_dist)
		if goal_height > start_height: # going up
			# h = l * s
			# 2^l * h/l = total cost
			m_diff = 1/math.log(2)
			m_cost = 2 ** m_diff 
			return (delta_h / m_diff) * m_cost
		elif goal_height < start_height: # going down
			return s * 2**((delta_h)/s) if s != 0 else 0
		else: # same level
			return s

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		# explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				# explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			# if explored[str(v.x)+','+str(v.y)]:
				# continue
			# explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					# My changes Add h(n)
					# hn = self.hExp(map_, neighbor)
					neighbor.comparator = alt + self.h(map_, neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarDiv(AIModule):
	def h(self, map_, start):
		# get goal
		goal = map_.goal
		# get distances
		y_dist = abs(goal.y - start.y)
		x_dist = abs(goal.x - start.x)
		# min steps
		s = min(x_dist, y_dist) + abs(y_dist - x_dist)
		# get height
		start_height = map_.getTile(start.x, start.y)
		v = math.log(2, start_height)
		return max( (s - v)/2, 0 )

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		# explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				# explored[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			# if explored[str(v.x)+','+str(v.y)]:
			# 	continue
			# explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + self.h(map_, neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

		path = []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		path.append(map_.getStartPoint())
		path.reverse()
		return path

class AStarMSH(AIModule):
	def h(self, map_, start, end):
		# get goal
		# goal = map_.goal
		# get distances
		y_dist = abs(end.y - start.y)
		x_dist = abs(end.x - start.x)
		# get height difference
		end_height = map_.getTile(end.x, end.y)
		start_height = map_.getTile(start.x, start.y)
		delta_h = end_height - start_height
		# min steps
		s = min(x_dist, y_dist) + abs(y_dist - x_dist)
		if end_height > start_height: # going up
			# h = l * s
			# 2^l * h/l = total cost
			m_diff = 1/math.log(2)
			m_cost = 2 ** m_diff 
			return (delta_h / m_diff) * m_cost
		elif end_height < start_height: # going down
			return s * 2**((delta_h)/s) if s != 0 else 0
		else: # same level
			return s

	# def createPath(self, map_):
	# 	q = PriorityQueue()
	# 	cost = {}
	# 	prev = {}
	# 	for i in range(map_.width):
	# 		for j in range(map_.length):
	# 			cost[str(i)+','+str(j)] = math.inf
	# 			prev[str(i)+','+str(j)] = None
	# 	current_point = deepcopy(map_.start)
	# 	current_point.comparator = 0
	# 	cost[str(current_point.x)+','+str(current_point.y)] = 0
	# 	q.put(current_point)
	# 	while q.qsize() > 0:
	# 		# Get new point from PQ
	# 		v = q.get()
	# 		# Check if popping off goal
	# 		if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
	# 			break
	# 		# Evaluate neighbors
	# 		neighbors = map_.getNeighbors(v)
	# 		for neighbor in neighbors:
	# 			alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
	# 			if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
	# 				cost[str(neighbor.x)+','+str(neighbor.y)] = alt
	# 				neighbor.comparator = alt + self.h(map_, neighbor)
	# 				prev[str(neighbor.x)+','+str(neighbor.y)] = v
	# 			q.put(neighbor)

	# 	path = []
	# 	while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
	# 		path.append(v)
	# 		v = prev[str(v.x)+','+str(v.y)]
	# 	path.append(map_.getStartPoint())
	# 	path.reverse()
	# 	return path

	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}

		q2 = PriorityQueue()
		cost2 = {}
		prev2 = {}
		explored2 = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				cost2[str(i)+','+str(j)] = math.inf
				prev2[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
				explored2[str(i)+','+str(j)] = False
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)

		current_point2 = deepcopy(map_.goal)
		current_point2.comparator = 0
		cost2[str(current_point2.x)+','+str(current_point2.y)] = 0
		q2.put(current_point2)
		middle = 0
		while q.qsize() > 0:
			# print(2)
			# Get new point from PQ
			v = q.get()
			explored[str(v.x)+','+str(v.y)] = True
			v2 = q2.get()
			explored2[str(v2.x)+','+str(v2.y)] = True
			# Check if hit middle
			if explored2[str(v.x) + ',' + str(v.y)] == True:
				middle = v
				break
			if explored[str(v2.x) + ',' + str(v2.y)] == True:
				middle = v2
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			neighbors2 = map_.getNeighbors(v2)
			for neighbor, neighbor2 in zip(neighbors, neighbors2):
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				alt2 = map_.getCost(neighbor2, v2) + cost2[str(v2.x)+','+str(v2.y)]

				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					neighbor.comparator = alt + self.h(map_, neighbor, map_.goal)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
				q.put(neighbor)

				if alt2 < cost2[str(neighbor2.x)+','+str(neighbor2.y)]:
					cost2[str(neighbor2.x)+','+str(neighbor2.y)] = alt2
					neighbor2.comparator = alt2 + self.h(map_, map_.start, neighbor2)
					prev2[str(neighbor2.x)+','+str(neighbor2.y)] = v2
				q2.put(neighbor2)
		# da merge
		path = []
		path2 = []
		v = middle
		while not (v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
		v2 = middle
		while not (v2.x == map_.getEndPoint().x and v2.y == map_.getEndPoint().y):
			path2.append(v2)
			v2 = prev2[str(v2.x)+','+str(v2.y)]
			# print(v2.x,v2.y)
		# path2.reverse()
		path.append(map_.getStartPoint())
		path.reverse()
		path.pop()
		path.extend(path2)
		path.append(map_.getEndPoint())
		
		return path


