from mesa import Agent, Model
from abm_project.attractor import Attractor
from mesa.time import *
from mesa.space import *
from mesa.datacollection import *

import random

class BuildingModel(Model):
	"""
	A model representing a building with some number of rooms(agents)
	"""

	description = ("A model representing a building with some number of different types of rooms (agents)"
	+" being attracted to each other based on some set of complicated rules."
	+"The result of the model is the best possible plan view of the building according to these rules.")

	def __init__(
		self,
		width=20,
		height=20,
		N=500,
		sl1_rooms=1,
		sl_rooms=2,
		sl_width=5.14,
		sl_height=3.5,
		wc1_rooms=1,
		wc_rooms=1,
		wc_width=4,
		wc_height=1.5,
		liv_rooms=1,
		liv_width=7.77,
		liv_height=4.5,
		entry_rooms=1,
		entry_width=2.66,
		entry_height=1.5,
		kit_rooms=1,
		kit_width=4.5,
		kit_height=4,
		off_rooms=1,
		off_width=3,
		off_height=3.33,
		corr_rooms=1,
		corr_width=1,
		corr_height=12,
		bath_rooms=1,
		bath_width=4,
		bath_height=2,
	):
		# Set parameters
		self.N = N
		self.sl1_rooms = sl1_rooms
		self.sl_rooms = sl_rooms
		self.sl_width = sl_width
		self.sl_height = sl_height
		self.wc1_rooms = wc1_rooms
		self.wc_rooms = wc_rooms
		self.wc_width = wc_width
		self.wc_height = wc_height
		self.liv_rooms = liv_rooms
		self.liv_width = liv_width
		self.liv_height = liv_height
		self.entry_rooms = entry_rooms
		self.entry_width = entry_width
		self.entry_height = entry_height
		self.kit_rooms = kit_rooms
		self.kit_width = kit_width
		self.kit_height = kit_height
		self.off_rooms = off_rooms
		self.off_width = off_width
		self.off_height = off_height
		self.corr_rooms = corr_rooms
		self.corr_width = corr_width
		self.corr_height = corr_height
		self.bath_rooms = bath_rooms
		self.bath_width = bath_width
		self.bath_height = bath_height
		self.width = width
		self.height = height
		self.torus = False
		self.reset_const = 1
		self.c = 0
		self.num_agents = (sl_rooms + wc_rooms
						+ sl1_rooms + wc1_rooms
						+ liv_rooms + entry_rooms
						+ kit_rooms + off_rooms
						+ corr_rooms + bath_rooms)
		self.agents = []
		self.current_id = 0
		self.grid = SingleGrid(width, height, self.torus)
		self.schedule = SimultaneousActivation(self)
		self.stable_pos = 0
		self.datacollector = DataCollector(
			model_reporters={
				"Number of Rooms": lambda x: x.num_agents,
				"SL Rooms": lambda x: x.sl_rooms,
				"SL1 Rooms": lambda x: x.sl1_rooms,
				"WC Rooms": lambda x: x.wc_rooms,
				"WC1 Rooms": lambda x: x.wc1_rooms,
			},
			agent_reporters={
				"SL Posistion": lambda x: x.pos,
				"SL1 Position": lambda x: x.pos
			},
		)
		self.reset = False
		self.make_agents()
		self.running = True
		self.datacollector.collect(self)

	def make_agents(self):
	# Create Sleeping Rooms(1)
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.sl1_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.sl_width / 2), self.grid.width - int(self.sl_width / 2), 1)
			y = self.random.randrange(int(self.sl_height / 2), self.grid.height - int(self.sl_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.sl_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.sl_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.sl_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.sl_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.sl_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.sl_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				sl1room = SL1RoomAgent(self.next_id(), pos, self, True, self.sl1_rooms, self.sl_width, self.sl_height)
				self.agents.append(sl1room)
				self.schedule.add(sl1room)
				self.grid.place_agent(sl1room, pos)
				i += 1
			if len(self.agents) == 0:
				sl1room = SL1RoomAgent(self.next_id(), pos, self, True, self.sl1_rooms, self.sl_width, self.sl_height)
				self.agents.append(sl1room)
				self.schedule.add(sl1room)
				self.grid.place_agent(sl1room, pos)
				i += 1
	# Create Sleeping Rooms
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.sl_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.sl_width / 2), self.grid.width - int(self.sl_width / 2), 1)
			y = self.random.randrange(int(self.sl_height / 2), self.grid.height - int(self.sl_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.sl_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.sl_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.sl_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.sl_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.sl_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.sl_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				slroom = SLRoomAgent(self.next_id(), pos, self, True, self.sl_rooms, self.sl_width, self.sl_height)
				self.agents.append(slroom)
				self.schedule.add(slroom)
				self.grid.place_agent(slroom, pos)
				i += 1
			if len(self.agents) == 0:
				slroom = SLRoomAgent(self.next_id(), pos, self, True, self.sl_rooms, self.sl_width, self.sl_height)
				self.agents.append(slroom)
				self.schedule.add(slroom)
				self.grid.place_agent(slroom, pos)
				i += 1
	# Create WC Rooms
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.wc_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.wc_width / 2), self.grid.width - int(self.wc_width / 2), 1)
			y = self.random.randrange(int(self.wc_height / 2), self.grid.height - int(self.wc_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.wc_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.wc_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.wc_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.wc_height / 2)
							and y <= agent.y + int(agent.agent_height / 2) + int(self.wc_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.wc_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				wcroom = WCRoomAgent(self.next_id(), pos, self, True, self.wc_rooms, self.wc_width, self.wc_height)
				self.agents.append(wcroom)
				self.schedule.add(wcroom)
				self.grid.place_agent(wcroom, pos)
				i += 1
			if len(self.agents) == 0:
				wcroom = WCRoomAgent(self.next_id(), pos, self, True, self.wc_rooms, self.wc_width, self.wc_height)
				self.agents.append(wcroom)
				self.schedule.add(wcroom)
				self.grid.place_agent(wcroom, pos)
				i += 1
	# Create WC Rooms(1)
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.wc1_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.wc_width / 2), self.grid.width - int(self.wc_width / 2), 1)
			y = self.random.randrange(int(self.wc_height / 2), self.grid.height - int(self.wc_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.wc_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.wc_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.wc_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.wc_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.wc_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.wc_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				wc1room = WC1RoomAgent(self.next_id(), pos, self, True, self.wc1_rooms, self.wc_width, self.wc_height)
				self.agents.append(wc1room)
				self.schedule.add(wc1room)
				self.grid.place_agent(wc1room, pos)
				i += 1
			if len(self.agents) == 0:
				wc1room = WC1RoomAgent(self.next_id(), pos, self, True, self.wc1_rooms, self.wc_width, self.wc_height)
				self.agents.append(wc1room)
				self.schedule.add(wc1room)
				self.grid.place_agent(wc1room, pos)
				i += 1
	# Create Living Rooms
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.liv_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.liv_width / 2), self.grid.width - int(self.liv_width / 2), 1)
			y = self.random.randrange(int(self.liv_height / 2), self.grid.height - int(self.liv_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.liv_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.liv_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.liv_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.liv_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.liv_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.liv_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				livroom = LivRoomAgent(self.next_id(), pos, self, True, self.liv_rooms, self.liv_width, self.liv_height)
				self.agents.append(livroom)
				self.schedule.add(livroom)
				self.grid.place_agent(livroom, pos)
				i += 1
			if len(self.agents) == 0:
				livroom = LivRoomAgent(self.next_id(), pos, self, True, self.liv_rooms, self.liv_width, self.liv_height)
				self.agents.append(livroom)
				self.schedule.add(livroom)
				self.grid.place_agent(livroom, pos)
				i += 1
	# Create Entries
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.entry_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.entry_width / 2), self.grid.width - int(self.entry_width / 2), 1)
			y = self.random.randrange(int(self.entry_height / 2), self.grid.height - int(self.entry_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.entry_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.entry_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.entry_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.entry_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.entry_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.entry_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				entryroom = EntryRoomAgent(self.next_id(), pos, self, True, self.entry_rooms, self.entry_width, self.entry_height)
				self.agents.append(entryroom)
				self.schedule.add(entryroom)
				self.grid.place_agent(entryroom, pos)
				i += 1
			if len(self.agents) == 0:
				entryroom = EntryRoomAgent(self.next_id(), pos, self, True, self.entry_rooms, self.entry_width, self.entry_height)
				self.agents.append(entryroom)
				self.schedule.add(entryroom)
				self.grid.place_agent(entryroom, pos)
				i += 1
	# Create Kitchens
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.kit_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.kit_width / 2), self.grid.width - int(self.kit_width / 2), 1)
			y = self.random.randrange(int(self.kit_height / 2), self.grid.height - int(self.kit_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.kit_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.kit_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.kit_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.kit_height / 2)
							and y <= agent.y + int(agent.agent_height / 2) + int(self.kit_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.kit_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				kitroom = KitRoomAgent(self.next_id(), pos, self, True, self.kit_rooms, self.kit_width, self.kit_height)
				self.agents.append(kitroom)
				self.schedule.add(kitroom)
				self.grid.place_agent(kitroom, pos)
				i += 1
			if len(self.agents) == 0:
				kitroom = KitRoomAgent(self.next_id(), pos, self, True, self.kit_rooms, self.kit_width, self.kit_height)
				self.agents.append(kitroom)
				self.schedule.add(kitroom)
				self.grid.place_agent(kitroom, pos)
				i += 1
	# Create Office Rooms
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.off_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.off_width / 2), self.grid.width - int(self.off_width / 2), 1)
			y = self.random.randrange(int(self.off_height / 2), self.grid.height - int(self.off_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.off_width / 2)
							and x <= agent.x + int(agent.agent_width / 2) + int(self.off_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.off_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.off_height / 2)
							and y <= agent.y + int(agent.agent_height / 2) + int(self.off_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.off_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				offroom = OffRoomAgent(self.next_id(), pos, self, True, self.off_rooms, self.off_width, self.off_height)
				self.agents.append(offroom)
				self.schedule.add(offroom)
				self.grid.place_agent(offroom, pos)
				i += 1
			if len(self.agents) == 0:
				offroom = OffRoomAgent(self.next_id(), pos, self, True, self.off_rooms, self.off_width, self.off_height)
				self.agents.append(offroom)
				self.schedule.add(offroom)
				self.grid.place_agent(offroom, pos)
				i += 1
	# Create Corridors
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.corr_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.corr_width / 2), self.grid.width - int(self.corr_width / 2), 1)
			y = self.random.randrange(int(self.corr_height / 2), self.grid.height - int(self.corr_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.corr_width / 2)
							and x <= agent.x + int(agent.agent_width / 2) + int(self.corr_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.corr_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.corr_height / 2)
						and y <= agent.y + int(agent.agent_height / 2) + int(self.corr_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.corr_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				corrroom = CorrRoomAgent(self.next_id(), pos, self, True, self.corr_rooms, self.corr_width, self.corr_height)
				self.agents.append(corrroom)
				self.schedule.add(corrroom)
				self.grid.place_agent(corrroom, pos)
				i += 1
			if len(self.agents) == 0:
				corrroom = CorrRoomAgent(self.next_id(), pos, self, True, self.corr_rooms, self.corr_width, self.corr_height)
				self.agents.append(corrroom)
				self.schedule.add(corrroom)
				self.grid.place_agent(corrroom, pos)
				i += 1
	# Create Baths
		# Place agents with dimensions
		i = 0
		while 1:
			if i == self.bath_rooms:
				break
			# Add the agent to a random grid cell
			x = self.random.randrange(int(self.bath_width / 2), self.grid.width - int(self.bath_width / 2), 1)
			y = self.random.randrange(int(self.bath_height / 2), self.grid.height - int(self.bath_height / 2), 1)
			pos = (x, y)
			# Check position
			check_pos = 0
			for agent in self.agents:
				if self.grid.is_cell_empty(pos):
					if (x >= agent.x - int(agent.agent_width / 2) - int(self.bath_width / 2)
						and x <= agent.x + int(agent.agent_width / 2) + int(self.bath_width / 2)):
						if abs(y - agent.y) > int(agent.agent_height / 2) + int(self.bath_height / 2):
							check_pos += 1
					elif (y >= agent.y - int(agent.agent_height / 2) - int(self.bath_height / 2)
							and y <= agent.y + int(agent.agent_height / 2) + int(self.bath_height / 2)):
						if abs(x - agent.x) > int(agent.agent_width / 2) + int(self.bath_width / 2):
							check_pos += 1
					else:
						check_pos += 1
			if check_pos == len(self.agents):
				bathroom = BathRoomAgent(self.next_id(), pos, self, True, self.bath_rooms, self.bath_width, self.bath_height)
				self.agents.append(bathroom)
				self.schedule.add(bathroom)
				self.grid.place_agent(bathroom, pos)
				i += 1
			if len(self.agents) == 0:
				bathroom = BathRoomAgent(self.next_id(), pos, self, True, self.bath_rooms, self.bath_width, self.bath_height)
				self.agents.append(bathroom)
				self.schedule.add(bathroom)
				self.grid.place_agent(bathroom, pos)
				i += 1

	def step(self):
		"""
		Run one step of the model. If All agents are stable, halt the model.
		"""
		# Reset counter of stable_pos
		self.stable_pos = 0
		# tell all the agents in the model to run their step function
		self.schedule.step()
		# collect data
		self.datacollector.collect(self)
		print("--stable_pos : ", self.stable_pos)
		# stabilize the model if counter reaches the total number of agents
		if self.stable_pos == self.schedule.get_agent_count():
			self.running = False
		# each N steps reset model if it is not yet stabilized
		if self.schedule.steps / self.N == self.reset_const:
			print(self.schedule.steps)
			self.reset = True

class SL1RoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""
	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore=True, sl1_rooms=1, agent_width=6, agent_height=3, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.sl1_rooms = sl1_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_sl1 = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.sl1_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.sl1_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.south_pole()
				if random.randint(1,1) == 1:
					self.east_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is WCRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_sl1 = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is WCRoomAgent:
		# 		self.stable_sl1 += 1
		# 	if type(i) is CorrRoomAgent:
		# 		self.stable_sl1 += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is WCRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_sl1 += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_sl1 += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is CorrRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_sl1 += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_sl1 += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_sl1 == 2:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class SLRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore=True, sl_rooms=2, agent_width=6, agent_height=3, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.sl_rooms = sl_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_sl = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.sl_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.sl_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.south_pole()
				if random.randint(1,1) == 1:
					self.east_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_sl = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is CorrRoomAgent:
		# 		self.stable_sl += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is CorrRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_sl += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_sl += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_sl == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class WC1RoomAgent(Attractor):
	"""
	An agent representing a WC room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, wc1_rooms=1, agent_width=3, agent_height=2, init_state=STABLED):

		super().__init__(unique_id, pos, model, moore=moore)
		self.wc1_rooms = wc1_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_wc1 = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.wc1_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.wc1_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is OffRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_wc1 = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is OffRoomAgent:
		# 		self.stable_wc1 += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is OffRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_wc1 += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_wc1 += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_wc1 == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class WCRoomAgent(Attractor):
	"""
	An agent representing a WC room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, wc_rooms=1, agent_width=3, agent_height=2, init_state=STABLED):

		super().__init__(unique_id, pos, model, moore=moore)
		self.wc_rooms = wc_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_wc = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.wc_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.wc_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SL1RoomAgent:
						self.agent_attraction(agent)
			# General attraction			
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_wc = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is SL1RoomAgent:
		# 		self.stable_wc += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is SL1RoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_wc += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_wc += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_wc == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class LivRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, liv_rooms=1, agent_width=7, agent_height=5, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.liv_rooms = liv_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_liv = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.liv_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.liv_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.east_pole()
				if random.randint(1,2) == 2:
					self.west_pole()
				if random.randint(1,1) == 1:
					self.south_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is KitRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is EntryRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is BathRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is OffRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_liv = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is EntryRoomAgent:
		# 		self.stable_liv += 1
		# 	if type(i) is BathRoomAgent:
		# 		self.stable_liv += 1
		# 	if type(i) is OffRoomAgent:
		# 		self.stable_liv += 1
		# 	if type(i) is CorrRoomAgent:
		# 		self.stable_liv += 1
		# 	if type(i) is KitRoomAgent:
		# 		self.stable_liv += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is EntryRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_liv += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_liv += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is BathRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_liv += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_liv += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is OffRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_liv += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_liv += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is CorrRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_liv += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_liv += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is KitRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_liv += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_liv += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_liv == 5:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class EntryRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, entry_rooms=1, agent_width=2, agent_height=2, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.entry_rooms = entry_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_entry = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.entry_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.entry_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.east_pole()
				if random.randint(1,2) == 2:
					self.west_pole()
				if random.randint(1,1) == 1:
					self.south_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_entry = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is LivRoomAgent:
		# 		self.stable_entry += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is LivRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_entry += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_entry += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

		if self.stable_entry == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class KitRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, kit_rooms=1, agent_width=6, agent_height=3, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.kit_rooms = kit_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_kit = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.kit_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.kit_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.south_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.west_pole()
			# Agents attraction
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is BathRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_kit = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is LivRoomAgent:
		# 		self.stable_kit += 1
		# 	# if type(i) is CorrRoomAgent:
		# 	# 	self.stable_kit += 1
		# 	# if type(i) is BathRoomAgent:
		# 	# 	self.stable_kit += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is LivRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_kit += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_kit += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)

			# elif type(agent) is CorrRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_kit += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_kit += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)
			# elif type(agent) is BathRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_kit += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_kit += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)

		if self.stable_kit == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class OffRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, off_rooms=1, agent_width=4, agent_height=3, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.off_rooms = off_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_off = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.off_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.off_rooms > 0:
				if random.randint(1,4) == 4:
					self.west_pole()
				if random.randint(1,3) == 3:
					self.south_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()
			# Agents attraction
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is WC1RoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_off = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is LivRoomAgent:
		# 		self.stable_off += 1
		# 	if type(i) is WC1RoomAgent:
		# 		self.stable_off += 1
		# 	# if type(i) is CorrRoomAgent:
		# 	# 	self.stable_off += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is LivRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_off += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_off += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is WC1RoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_off += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_off += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			# elif type(agent) is CorrRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_off += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_off += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)

		if self.stable_off == 2:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class CorrRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, corr_rooms=1, agent_width=1, agent_height=12, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.corr_rooms = corr_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_corr = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.corr_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.corr_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()
			# Agents attraction
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SLRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SL1RoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is KitRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is OffRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_corr = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is SL1RoomAgent:
		# 		self.stable_corr += 1
		# 	if type(i) is SLRoomAgent:
		# 		self.stable_corr += 1
		# 	if type(i) is LivRoomAgent:
		# 		self.stable_corr += 1
		# 	# if type(i) is KitRoomAgent:
		# 	# 	self.stable_corr += 1
		# 	# if type(i) is OffRoomAgent:
		# 	# 	self.stable_corr += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is SL1RoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_corr += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_corr += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is SLRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_corr += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_corr += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			elif type(agent) is LivRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_corr += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_corr += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			# elif type(agent) is KitRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_corr += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_corr += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)
			# elif type(agent) is OffRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_corr += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_corr += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)

		if self.stable_corr == 4:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED

class BathRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True
	STABLED = 0
	MOVED = 1

	def __init__(self, unique_id, pos, model, moore = True, bath_rooms=1, agent_width=4, agent_height=2, init_state=STABLED):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.bath_rooms = bath_rooms
		self.agent_width = agent_width
		self.agent_height = agent_height
		self.pos = pos
		self.x, self.y = pos
		self.moore = moore
		self.state = init_state
		self.next_state = None
		self.moved = 0
		self.stable_bath = 0
		self.astar_path = []

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):
		self.next_state = self.state
		if self.next_state == self.MOVED:
			# Grid attraction
			if self.bath_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()
			# Poles attraction
			if self.bath_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()
			# Agents attraction
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is KitRoomAgent:
						self.agent_attraction(agent)
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)
			# General attraction
			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

	# Apply the changes made in step()
	def advance(self):
		self.stable_bath = 0
		# Stabilize agents without dimensions
		# neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		# for i in neighbors:
		# 	if type(i) is LivRoomAgent:
		# 		self.stable_bath += 1
		# 	# if type(i) is KitRoomAgent:
		# 	# 	self.stable_bath += 1

		# Stabilize agents with dimensions
		for agent in self.model.agents:
			if type(agent) is LivRoomAgent:
				if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
					and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
					if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
						self.stable_bath += 1
				elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2)
					and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2)):
					if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
						self.stable_bath += 1
				# shortest path finder algorithm
				self.astar_algorithm(agent)
				self.astar_attraction(agent)
			# elif type(agent) is KitRoomAgent:
			# 	if (self.y >= agent.y - int(agent.agent_height / 2) - int(self.agent_height / 2)
			# 		and self.y <= agent.y + int(agent.agent_height / 2) + int(self.agent_height / 2)):
			# 		if abs(agent.x - self.x) == int(agent.agent_width / 2) + int(self.agent_width / 2) + 1:
			# 			self.stable_bath += 1
			# 	elif (self.x >= agent.x - int(agent.agent_width / 2) - int(self.agent_width / 2))
			# 		and self.x <= agent.x + int(agent.agent_width / 2) + int(self.agent_width / 2):
			# 		if abs(agent.y - self.y) == int(agent.agent_height / 2) + int(self.agent_height / 2) + 1:
			# 			self.stable_bath += 1
			# 	# shortest path finder algorithm
			# 	print(self.astar_algorithm(agent))
			# 	for i in self.astar_path:
			# 		self.move_agent_with_dimensions(i)

		if self.stable_bath == 1:
			self.model.stable_pos += 1
			self.state = self.STABLED
		else:
			self.state = self.MOVED
