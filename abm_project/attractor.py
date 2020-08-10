"""
Generalized behavior for the grid-poles-relationships attraction.
"""

from mesa import Agent
from queue import PriorityQueue
import math

class Attractor(Agent):
	"""
	Class implementing the general rules of the grid, poles and relationships between agents attraction.

	Not intended to be used on its own, but to inherit its medthod to
	multiple other agents.
	"""
	grid = None
	x = None
	y = None
	moore = True

	def __init__(self, unique_id, pos, model, moore=True):
		"""
		grid: The SingleGrid object in which the agent lives.
		x: The agent's current x coordinate
		y: The agent's current y coordinate
		moore: If True, may move in all 8 directions.
			Otherwise, only up, down, left, right.
		"""
		super().__init__(unique_id, model)
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore

	def get_distance(self, pos_1, pos_2):
		""" Get the distance between two points
		Args:
		pos_1, pos_2: Coordinate tuples for both points.

		"""
		x1, y1 = pos_1
		x2, y2 = pos_2
		dx = x1 - x2
		dy = y1 - y2
		return math.sqrt(dx ** 2 + dy ** 2)

	def get_rect_dist(self, agent):
		"""
		Get the Manhattan distance between two rectangles
		"""
		# overlaps in x
		if abs(self.x - agent.x) <= (self.agent_width / 2 + agent.agent_width / 2):
			dx = 0
		else:
			dx = abs(self.x - agent.x) - (self.agent_width / 2 + agent.agent_width / 2)
		# overlaps in y
		if abs(self.y - agent.y) <= (self.agent_height / 2 + agent.agent_height / 2):
			dy = 0
		else:
			dy = abs(self.y - agent.y) - (self.agent_height / 2 + agent.agent_height / 2)
		return int(dx + dy)

	def move_agent_without_dimensions(self, pos):

		if self.x <= self.model.width - 1 and self.x >= 0 and self.y <= self.model.height - 1 and self.y >= 0:
			if self.model.grid.is_cell_empty(pos):
				self.model.grid.move_agent(self, pos)
				return True
		else:
			return False

	def move_agent_with_dimensions(self, pos):
		check_pos_y = 0
		for agent in self.model.agents:
			if agent is not self:
				if (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(self.y - agent.y) > int(agent.agent_height / 2) + int(self.agent_height / 2):
						check_pos_y += 1
				else:
					check_pos_y += 1
		check_pos_x = 0
		for agent in self.model.agents:
			if agent is not self:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(self.x - agent.x) > int(agent.agent_width / 2) + int(self.agent_width / 2):
						check_pos_x += 1
				else:
					check_pos_x += 1

		if (self.x < self.model.width - int(self.agent_width / 2) and self.x >= int(self.agent_width / 2)
			and self.y < self.model.height - int(self.agent_height / 2) and self.y >= int(self.agent_height / 2)):
			if check_pos_x == check_pos_y == len(self.model.agents) - 1 and self.model.grid.is_cell_empty(pos):
				self.model.grid.move_agent(self, pos)
				return True
			if len(self.model.agents) == 1:
				self.model.grid.move_agent(self, pos)
				return True
		else:
			return False

	def east_pole(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		self.x += 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def west_pole(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		self.x -= 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def north_pole(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		self.y += 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def south_pole(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		self.y -= 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def grid_attraction_70(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		width = self.model.width
		height = self.model.height
		centerx = self.model.width / 2
		centery = self.model.height / 2
		half_centerx = self.model.width / 4
		half_centery = self.model.height / 4
		if (self.x >= half_centerx and self.x <= width - half_centerx
			and self.y >= half_centery and self.y <= height - half_centery):
			if self.x >= half_centerx and self.x < centerx:
				self.x -= 1
			if self.x <= width - half_centerx and self.x >= centerx:
				self.x += 1
			if self.y >= half_centery and self.y < centery:
				self.y -= 1
			if self.y <= height - half_centery and self.y >= centery:
				self.y += 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def grid_attraction_25(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		width = self.model.width
		height = self.model.height
		centerx = self.model.width / 2
		centery = self.model.height / 2
		half_centerx = self.model.width / 4
		half_centery = self.model.height / 4
		if (self.x < half_centerx and self.x >= 0 and self.x > width - half_centerx and self.x <= width - 1
			and self.y < half_centery and self.y >= 0 and self.y < height - half_centery and self.y <= height - 1
			and self.x >= centerx - 2 and self.x <= centerx + 1 
			and self.y >= centery - 2 and self.y <= centery + 1):
			if self.x < half_centerx and self.x >= 0:
				self.x += 1
			if self.x > width - half_centerx and self.x <= width - 1:
				self.x -= 1
			if self.x >= centerx - (width / 10) and self.x <= centerx - 1:
				self.x -= 1
			if self.x <= centerx + (width / 10) - 1 and self.x >= centerx:
				self.x += 1
			if self.y < half_centery and self.y >= 0:
				self.y += 1
			if self.y > height - half_centery and self.y <= height - 1:
				self.y -= 1
			if self.y >= centery - (height / 10) and self.y <= centery - 1:
				self.y -= 1
			if self.y <= centery + (height / 10) - 1 and self.y >= centery:
				self.y += 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def grid_attraction_5(self):
		self.moved = 0
		init_pos = (self.x, self.y)
		width = self.model.width
		height = self.model.height
		centerx = self.model.width / 2
		centery = self.model.height / 2
		if (self.x < centerx - 2 and self.x >= 0 and self.x > centerx + 1 and self.x <= width - 1
			and self.y < centery - 2 and self.y >= 0 and self.y > centerx + 1 and self.y <= height - 1):
			if self.x < centerx - (width / 10) and self.x >= 0:
				self.x += 1
			if self.x > centerx + (width / 10) - 1 and self.x <= width - 1:
				self.x -= 1
			if self.y < centery - (height / 10) and self.y >= 0:
				self.y += 1
			if self.y > centery + (height / 10) - 1 and self.y <= height - 1:
				self.y -= 1
		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def move_cost(self, neighbor):
		for agent in self.model.agents:
			if agent is not self:
				if (neighbor[1] <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2) 
					and neighbor[1] >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)):
					if abs(neighbor[0] - agent.x) <= int(agent.agent_width / 2) + int(self.agent_width / 2):
						return 100 # Extremely high cost to enter barrier squares
				elif (neighbor[0] <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)
					and neighbor[0] >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)):
					if abs(neighbor[1] - agent.y) <= int(agent.agent_height / 2) + int(self.agent_height / 2):
						return 100 # Extremely high cost to enter barrier squares
		return 1 # Normal movement cost

	def astar_algorithm(self, agent):
		"""
		A* algorithm in order to find the shortest path between
		two attracted agents avoiding obstacles(other agents) in their way.
		"""

		self.astar_path = []

		G = {} #Actual movement cost to each position from the start position
		F = {} #Estimated movement cost of start to end going via this position

		start = self.pos
		end = agent.pos

		#Initialize starting values
		G[start] = 0
		F[start] = self.get_distance(start, end)

		closedVertices = set()
		openVertices = set([start])
		cameFrom = {}

		while len(openVertices) > 0:
			#Get the vertex in the open list with the lowest F score
			current = None
			currentFscore = None
			for pos in openVertices:
				if current is None or F[pos] < currentFscore:
					currentFscore = F[pos]
					current = pos

			#Check if we have reached the goal
			goal = 0
			if (current[1] <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2) 
				and current[1] >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)):
				if abs(current[0] - agent.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
					goal += 1
			elif (current[0] <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)
				and current[0] >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)):
				if abs(current[1] - agent.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
					goal += 1

			# if current == end:
			if goal == 1:
				#Retrace our route backward
				path = [current]
				while current in cameFrom:
					current = cameFrom[current]
					path.append(current)
				path.reverse()
				self.astar_path = path
				return path #Done!

			#Mark the current vertex as closed
			openVertices.remove(current)
			closedVertices.add(current)

			neighbors = self.model.grid.get_neighborhood(current, moore=True, include_center=False, radius=1)

			#Update scores for vertices near the current position
			for neighbor in neighbors:
				if neighbor in closedVertices: 
					continue #We have already processed this node exhaustively
				
				candidateG = G[current] + self.move_cost(neighbor)

				if neighbor not in openVertices:
					openVertices.add(neighbor) #Discovered a new vertex
				elif candidateG >= G[neighbor]:
					continue #This G score is worse than previously found

				#Adopt this G score
				cameFrom[neighbor] = current
				G[neighbor] = candidateG
				H = self.get_distance(neighbor, end)
				F[neighbor] = G[neighbor] + H

		return False

	def agent_attraction(self, agent):
		self.moved = 0
		init_pos = (self.x, self.y)

		if self.x - agent.x >= (int(self.agent_width / 2) + int(agent.agent_width / 2)):
			self.x -= 1
		if agent.x - self.x >= (int(self.agent_width / 2) + int(agent.agent_width / 2)):
			self.x += 1
		if self.y - agent.y >= (int(self.agent_height / 2) + int(agent.agent_height / 2)):
			self.y -= 1
		if agent.y - self.y >= (int(self.agent_height / 2) + int(agent.agent_height / 2)):
			self.y += 1

		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1

	def astar_attraction(self, agent):
		self.moved = 0
		init_pos = (self.x, self.y)

		for item in self.astar_path:
			if self.x < item[0]:
				self.x = 1
			if item[0] < self.x:
				self.x -= 1
			if self.y < item[1]:
				self.y += 1
			if item[1] < self.y:
				self.y -= 1

		new_pos = (self.x, self.y)
		if not self.move_agent_with_dimensions(new_pos):
			self.x, self.y = init_pos
		else:
			self.moved = 1
