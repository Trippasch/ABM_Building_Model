from mesa import Agent, Model
from abm_project.attractor import Attractor
from mesa.time import *
from mesa.space import *
from mesa.datacollection import *
from mesa.batchrunner import *
import numpy as np
import pandas as pd
import itertools
import random

# Start of datacollector functions
def get_agent_type(model):

	agent_type = [type(agent) for agent in model.agents]

	return agent_type

def get_agent_pos(model):

	agent_pos = [agent.pos for agent in model.agents]
	
	return agent_pos

class BuildingModelBatch(Model):
	"""
	A model representing a building with some number of rooms(agents)
	"""

	description = ("A model representing a building with some number of different types of rooms (agents)"
	+" being attracted to each other based on some set of complicated rules."
	+"The result of the model is the best possible plan view of the building according to these rules.")

	# id generator to track run number in batch run data
	id_gen = itertools.count(1)

	# grid height
	grid_h = 20
	# grid width
	grid_w = 20

	def __init__(
		self, 
		width=20, 
		height=20, 
		sl1_rooms=1,
		sl_rooms=2,
		wc1_rooms=1, 
		wc_rooms=1, 
		liv_rooms=1, 
		entry_rooms=1, 
		kit_rooms=1, 
		off_rooms=1, 
		corr_rooms=1, 
		bath_rooms=1,
	):
		# Set parameters
		self.sl1_rooms = sl1_rooms
		self.sl_rooms = sl_rooms
		self.wc1_rooms = wc1_rooms
		self.wc_rooms = wc_rooms
		self.liv_rooms = liv_rooms
		self.entry_rooms = entry_rooms
		self.kit_rooms = kit_rooms
		self.off_rooms = off_rooms
		self.corr_rooms = corr_rooms
		self.bath_rooms = bath_rooms
		self.width = width
		self.height = height
		self.torus = False
		self.counter = 1
		self.num_agents = (sl_rooms + wc_rooms
						+ sl1_rooms + wc1_rooms
						+ liv_rooms + entry_rooms
						+ kit_rooms + off_rooms
						+ corr_rooms + bath_rooms)
		self.agents = []
		self.current_id = 0
		self.grid = SingleGrid(width, height, self.torus)
		self.schedule = RandomActivation(self)
		self.stable_pos = 0
		self.stable_sl1 = 0
		self.stable_sl = 0
		self.stable_wc = 0
		self.stable_wc1 = 0
		self.stable_liv = 0
		self.stable_entry = 0
		self.stable_kit = 0
		self.stable_corr = 0
		self.stable_off = 0
		self.stable_bath = 0
		self.datacollector = DataCollector(
			model_reporters={
				# "Number of Rooms": lambda m: m.num_agents,
				# "SL Rooms": lambda m: m.sl_rooms,
				# "SL1 Rooms": lambda m: m.sl1_rooms,
				# "WC Rooms": lambda m: m.wc_rooms,
				# "WC1 Rooms": lambda m: m.wc1_rooms,
				"agent_type": get_agent_type,
				"agent_pos": get_agent_pos,
			},
			agent_reporters={
				"agent_id": "unique_id",
				"agent_pos": "pos",
			},
		)
		self.make_agents()
		self.running = True
		self.reset = False
		self.datacollector.collect(self)

	def make_agents(self):

		# Create Sleeping Rooms(1)
		for i in range(self.sl1_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				sl1room = SL1RoomAgent(self.next_id(), pos, self, True, self.sl1_rooms)
				self.agents.append(sl1room)
				self.schedule.add(sl1room)
				self.grid.place_agent(sl1room, pos)
			else:
				i -= 1

		# Create Sleeping Rooms
		for i in range(self.sl_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				slroom = SLRoomAgent(self.next_id(), pos, self, True, self.sl_rooms)
				self.agents.append(slroom)
				self.schedule.add(slroom)
				self.grid.place_agent(slroom, pos)
			else:
				i -= 1

		# Create WC Rooms
		for i in range(self.wc_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				wcroom = WCRoomAgent(self.next_id(), pos, self, True, self.wc_rooms)
				self.agents.append(wcroom)
				self.schedule.add(wcroom)
				self.grid.place_agent(wcroom, pos)
			else:
				i -= 1

		# Create WC Rooms(1)
		for i in range(self.wc1_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				wc1room = WC1RoomAgent(self.next_id(), pos, self, True, self.wc1_rooms)
				self.agents.append(wc1room)
				self.schedule.add(wc1room)
				self.grid.place_agent(wc1room, pos)
			else:
				i -= 1

		# Create Living Rooms
		for i in range(self.liv_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				livroom = LivRoomAgent(self.next_id(), pos, self, True, self.liv_rooms)
				self.agents.append(livroom)
				self.schedule.add(livroom)
				self.grid.place_agent(livroom, pos)
			else:
				i -= 1

		# Create Entries
		for i in range(self.entry_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				enroom = EntryRoomAgent(self.next_id(), pos, self, True, self.entry_rooms)
				self.agents.append(enroom)
				self.schedule.add(enroom)
				self.grid.place_agent(enroom, pos)
			else:
				i -= 1

		# Create Kitchens
		for i in range(self.kit_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				kitroom = KitRoomAgent(self.next_id(), pos, self, True, self.kit_rooms)
				self.agents.append(kitroom)
				self.schedule.add(kitroom)
				self.grid.place_agent(kitroom, pos)
			else:
				i -= 1

		# Create Office Rooms
		for i in range(self.off_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				offroom = OffRoomAgent(self.next_id(), pos, self, True, self.off_rooms)
				self.agents.append(offroom)
				self.schedule.add(offroom)
				self.grid.place_agent(offroom, pos)
			else:
				i -= 1

		# Create Corridors
		for i in range(self.corr_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				corrroom = CorrRoomAgent(self.next_id(), pos, self, True, self.corr_rooms)
				self.agents.append(corrroom)
				self.schedule.add(corrroom)
				self.grid.place_agent(corrroom, pos)
			else:
				i -= 1

		# Create Baths
		for i in range(self.bath_rooms):
			# Add the agent to a random grid cell
			x = self.random.randrange(self.grid.width)
			y = self.random.randrange(self.grid.height)
			pos = (x, y)
			if self.grid.is_cell_empty(pos):
				bathroom = BathRoomAgent(self.next_id(), pos, self, True, self.bath_rooms)
				self.agents.append(bathroom)
				self.schedule.add(bathroom)
				self.grid.place_agent(bathroom, pos)
			else:
				i -= 1

	def step(self):
		"""
		Run one step of the model. If All agents are stable, halt the model.
		"""
		# Reset counter of stable_pos agents
		self.stable_pos = 0
		self.stable_sl1 = 0
		self.stable_sl = 0
		self.stable_wc = 0
		self.stable_wc1 = 0
		self.stable_liv = 0
		self.stable_entry = 0
		self.stable_kit = 0
		self.stable_corr = 0
		self.stable_off = 0
		self.stable_bath = 0

		# tell all the agents in the model to run their step function
		self.schedule.step()
		# collect data
		self.datacollector.collect(self)

		print("--stable_pos : ", self.stable_pos)
		if self.stable_pos == self.schedule.get_agent_count():
			self.running = False

		if self.schedule.steps / 1000 == self.counter:
			print(self.schedule.steps)
			self.reset = True

	# def run_model(self):
	# 	for i in range(self.run_time):
	# 		self.step()

class SL1RoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""
	moore = True

	def __init__(self, unique_id, pos, model, moore=True, sl1_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.sl1_rooms = sl1_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)
		for i in neighbors:
			if type(i) is WCRoomAgent:
				self.model.stable_sl1 += 1
			if type(i) is CorrRoomAgent:
				self.model.stable_sl1 += 1

		if self.model.stable_sl1 == 2:
			self.model.stable_pos += self.sl1_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is WCRoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.sl1_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.sl1_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.south_pole()
				if random.randint(1,1) == 1:
					self.east_pole()

class SLRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore=True, sl_rooms=2):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.sl_rooms = sl_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is CorrRoomAgent:
				self.model.stable_sl += 1

		if self.model.stable_sl == 2:
			self.model.stable_pos += self.sl_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is CorrRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.sl_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.sl_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.south_pole()
				if random.randint(1,1) == 1:
					self.east_pole()

class WC1RoomAgent(Attractor):
	"""
	An agent representing a WC room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, wc1_rooms=1):

		super().__init__(unique_id, pos, model, moore=moore)
		self.wc1_rooms = wc1_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is OffRoomAgent:
				self.model.stable_wc1 += 1

		if self.model.stable_wc1 == 1:
			self.model.stable_pos += self.wc1_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is OffRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.wc1_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.wc1_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()

class WCRoomAgent(Attractor):
	"""
	An agent representing a WC room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, wc_rooms=1):

		super().__init__(unique_id, pos, model, moore=moore)
		self.wc_rooms = wc_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is SL1RoomAgent:
				self.model.stable_wc += 1

		if self.model.stable_wc == 1:
			self.model.stable_pos += self.wc_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SL1RoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.wc_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.wc_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()

class LivRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, liv_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.liv_rooms = liv_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is EntryRoomAgent:
				self.model.stable_liv += 1
			if type(i) is BathRoomAgent:
				self.model.stable_liv += 1
			if type(i) is OffRoomAgent:
				self.model.stable_liv += 1
			if type(i) is CorrRoomAgent:
				self.model.stable_liv += 1
			if type(i) is KitRoomAgent:
				self.model.stable_liv += 1

		if self.model.stable_liv == 5:
			self.model.stable_pos += self.liv_rooms
		else:
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

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.liv_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.liv_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.east_pole()
				if random.randint(1,2) == 2:
					self.west_pole()
				if random.randint(1,1) == 1:
					self.south_pole()

class EntryRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, entry_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.entry_rooms = entry_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is LivRoomAgent:
				self.model.stable_entry += 1

		if self.model.stable_entry == 1:
			self.model.stable_pos += self.entry_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.entry_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.entry_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.east_pole()
				if random.randint(1,2) == 2:
					self.west_pole()
				if random.randint(1,1) == 1:
					self.south_pole()

class KitRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, kit_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.kit_rooms = kit_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is LivRoomAgent:
				self.model.stable_kit += 1
			# if type(i) is CorrRoomAgent:
			# 	self.model.stable_kit += 1
			# if type(i) is BathRoomAgent:
			# 	self.model.stable_kit += 1

		if self.model.stable_kit == 1:
			self.model.stable_pos += self.kit_rooms
		else:
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

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.kit_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.kit_rooms > 0:
				if random.randint(1,4) == 4:
					self.north_pole()
				if random.randint(1,3) == 3:
					self.south_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.west_pole()

class OffRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, off_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.off_rooms = off_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is LivRoomAgent:
				self.model.stable_off += 1
			if type(i) is WC1RoomAgent:
				self.model.stable_off += 1
			# if type(i) is CorrRoomAgent:
			# 	self.model.stable_off += 1

		if self.model.stable_off == 2:
			self.model.stable_pos += self.off_rooms
		else:
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

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.off_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.off_rooms > 0:
				if random.randint(1,4) == 4:
					self.west_pole()
				if random.randint(1,3) == 3:
					self.south_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()

class CorrRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, corr_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.corr_rooms = corr_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is SL1RoomAgent:
				self.model.stable_corr += 1
			if type(i) is SLRoomAgent:
				self.model.stable_corr += 1
			if type(i) is LivRoomAgent:
				self.model.stable_corr += 1
			# if type(i) is KitRoomAgent:
			# 	self.model.stable_corr += 1
			# if type(i) is OffRoomAgent:
			# 	self.model.stable_corr += 1

		if self.model.stable_corr == 4:
			self.model.stable_pos += self.corr_rooms
		else:
			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SLRoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is SL1RoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is KitRoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is OffRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.corr_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.corr_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()

class BathRoomAgent(Attractor):
	"""
	An agent representing a Sleeping room with some fixed variables
	"""

	moore = True

	def __init__(self, unique_id, pos, model, moore = True, bath_rooms=1):
		
		super().__init__(unique_id, pos, model, moore=moore)
		self.bath_rooms = bath_rooms
		self.pos = pos
		self.unique_id = unique_id
		self.x, self.y = pos
		self.moore = moore

	# step is called for each agent in model.BuildingModel.schedule.step()
	def step(self):

		neighbors = self.model.grid.get_neighbors((self.x, self.y), moore=True, include_center=False, radius=1)		
		for i in neighbors:
			if type(i) is LivRoomAgent:
				self.model.stable_bath += 1
			# if type(i) is KitRoomAgent:
			# 	self.model.stable_bath += 1

		if self.model.stable_bath == 1:
			self.model.stable_pos += self.bath_rooms
		else:
			if random.randint(1, 5) == 5:
				for agent in self.model.agents:
					if type(agent) is KitRoomAgent:
						self.agent_attraction(agent)

			if random.randint(1, 1) == 1:
				for agent in self.model.agents:
					if type(agent) is LivRoomAgent:
						self.agent_attraction(agent)

			if self.model.num_agents > 0:
				if random.randint(1, 7) == 7:
					for agent in self.model.agents:
						if agent is not self:
							self.agent_attraction(agent)

			if self.bath_rooms > 0:
				if random.randint(1, 20) == 20:
					self.grid_attraction_5()
				if random.randint(1, 4) == 4:
					self.grid_attraction_25()
				if random.randint(1, 1) == 1:
					self.grid_attraction_70()

			if self.bath_rooms > 0:
				if random.randint(1,4) == 4:
					self.south_pole()
				if random.randint(1,3) == 3:
					self.west_pole()
				if random.randint(1,2) == 2:
					self.east_pole()
				if random.randint(1,1) == 1:
					self.north_pole()

# parameter lists for each parameter to be tested in batch run
br_params = {
	"sl1_rooms": [1],
	"sl_rooms": [2],
	"wc1_rooms": [1],
	"wc_rooms": [1],
	"liv_rooms": [1],
	"entry_rooms": [1],
	"kit_rooms": [1],
	"off_rooms": [1],
	"corr_rooms": [1],
	"bath_rooms": [1],
}

br = BatchRunner(
	BuildingModelBatch,
	br_params,
	iterations=1,
	max_steps=10000,
	model_reporters={"Data Collector": lambda m: m.datacollector},
	agent_reporters={"agent_pos": "pos"},
)

if __name__ == "__main__":
	br.run_all()
	br_df = br.get_model_vars_dataframe()
	br_adf = br.get_agent_vars_dataframe()
	br_step_data = pd.DataFrame()

	for i in range(len(br_df["Data Collector"])):
		if isinstance(br_df["Data Collector"][i], DataCollector):
			i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
			br_step_data = br_step_data.append(i_run_data, ignore_index=True)
	br_step_data.to_csv("BuildingModelBatch_Step_Data.csv")

	# for i in range(len(br_adf["agent_pos"])):
	# 	if isinstance(br_adf["agent_pos"][i], DataCollector):
	# 		i_run_data = br_adf["agent_pos"][i].get_agent_vars_dataframe()
	# 		br_step_data = br_step_data.append(i_run_data, ignore_index=True)
	# br_step_data.to_csv("BuildingModelBatch_Step_Data.csv")
	