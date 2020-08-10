from mesa.visualization.ModularVisualization import *
from .model import *
from abm_project.model import BuildingModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import UserSettableParameter

class BuildingElement(TextElement):
	"""
	Display a text count of how many agents(rooms) there are.
	"""

	def __init__(self):
		pass

	def render(self, model):
		return "Number of rooms: " + str(model.num_agents)

def agent_portrayal(agent):
	if agent is None:
		return

	if agent.model.reset == True:
		server.reset_model()

	if agent.model.running == False:
		portrayal = {"Shape": "rect", "Filled": "true"}

		if type(agent) is SLRoomAgent:
			portrayal["Color"] = ["Red"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["red"]
			portrayal["sleeping room"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is SL1RoomAgent:
			portrayal["Color"] = ["DarkRed"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dark red"]
			portrayal["sleeping room(1)"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is WCRoomAgent:
			portrayal["Color"] = ["LightGrey"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["lightgrey"]
			portrayal["wc"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is WC1RoomAgent:
			portrayal["Color"] = ["DimGrey"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dimgrey"]
			portrayal["wc(1)"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is LivRoomAgent:
			portrayal["Color"] = ["Orange"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["orange"]
			portrayal["living room"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is EntryRoomAgent:
			portrayal["Color"] = ["Lime"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["lime"]
			portrayal["entry"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is KitRoomAgent:
			portrayal["Color"] = ["Pink"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["pink"]
			portrayal["kitchen"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is OffRoomAgent:
			portrayal["Color"] = ["Blue"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["blue"]
			portrayal["office"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is CorrRoomAgent:
			portrayal["Color"] = ["Aqua"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["aqua"]
			portrayal["corridor"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

		if type(agent) is BathRoomAgent:
			portrayal["Color"] = ["DarkCyan"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dark cyan"]
			portrayal["bathroom"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height

	else:

		portrayal = {"Shape": "rect", "Filled": "true"}

		if type(agent) is SLRoomAgent:
			portrayal["Color"] = ["Red"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["red"]
			portrayal["sleeping room"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is SL1RoomAgent:
			portrayal["Color"] = ["DarkRed"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dark red"]
			portrayal["sleeping room(1)"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is WCRoomAgent:
			portrayal["Color"] = ["LightGrey"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["lightgrey"]
			portrayal["wc"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is WC1RoomAgent:
			portrayal["Color"] = ["DimGrey"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dimgrey"]
			portrayal["wc(1)"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is LivRoomAgent:
			portrayal["Color"] = ["Orange"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["orange"]
			portrayal["living room"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is EntryRoomAgent:
			portrayal["Color"] = ["Lime"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["lime"]
			portrayal["entry"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is KitRoomAgent:
			portrayal["Color"] = ["Pink"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["pink"]
			portrayal["kitchen"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is OffRoomAgent:
			portrayal["Color"] = ["Blue"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["blue"]
			portrayal["office"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is CorrRoomAgent:
			portrayal["Color"] = ["Aqua"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["aqua"]
			portrayal["corridor"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

		if type(agent) is BathRoomAgent:
			portrayal["Color"] = ["DarkCyan"]
			portrayal["Layer"] = 0
			portrayal["color"] = ["dark cyan"]
			portrayal["bathroom"] = [agent.pos[0], agent.pos[1]]
			portrayal["x"] = agent.pos[0]
			portrayal["y"] = agent.pos[1]
			portrayal["w"] = agent.agent_width
			portrayal["h"] = agent.agent_height
			portrayal["r"] = 0.3

	return portrayal

width = 40
height = 40
pixel_ratio = 18

grid = CanvasGrid(agent_portrayal, width, height, width * pixel_ratio, height * pixel_ratio)
building_element = BuildingElement()

# map data to chart in the ChartModule
chartModel_element = ChartModule(
	[
		{"Label": "Number of Rooms", "Color": "Black"},
		{"Label": "SL Rooms", "Color": "Red"},
		{"Label": "SL1 Rooms", "Color": "DarkRed"},
		{"Label": "WC Rooms", "Color": "DimGrey"},
		{"Label": "WC1 Rooms", "Color": "LightGrey"},
	]
)

model_params = {
	"width": width,
	"height": height,
	"N": UserSettableParameter(
		"number",
		"Reset Model each N steps",
		value=10
	),
	"sl_rooms": UserSettableParameter(
		"slider",
		"Number of Sleeping Rooms --> Red Dots",
		2, 0, 10, 1,
	),
	"sl1_rooms": UserSettableParameter(
		"slider",
		"Number of Sleeping Rooms (1) --> Dark Red Dots",
		1, 0, 10, 1,
	),
	"sl_width": UserSettableParameter(
		"number",
		"Width of Sleeping Rooms",
		# value=5.14,
		value=5
	),
	"sl_height": UserSettableParameter(
		"number",
		"Height of Sleeping Rooms",
		# value=3.5,
		value=3
	),
	"wc_rooms": UserSettableParameter(
		"slider",
		"Number of WCs --> Light Grey Dots",
		1, 0, 10, 1,
	),
	"wc1_rooms": UserSettableParameter(
		"slider",
		"Number of WCs (1) --> Dim Grey Dots",
		1, 0, 10, 1,
	),
	"wc_width": UserSettableParameter(
		"number",
		"Width of WCs",
		# value=4,
		value=3,
	),
	"wc_height": UserSettableParameter(
		"number",
		"Height of WCs",
		# value=1.5,
		value=3,
	),
	"liv_rooms": UserSettableParameter(
		"slider",
		"Number of Living Rooms --> Orange Dots",
		1, 0, 10, 1,
	),
	"liv_width": UserSettableParameter(
		"number",
		"Width of Living Rooms",
		# value=7.77,
		value=7,
	),
	"liv_height": UserSettableParameter(
		"number",
		"Height of Living Rooms",
		# value=4.5,
		value=5,
	),
	"entry_rooms": UserSettableParameter(
		"slider",
		"Number of Entries --> Lime Dots",
		1, 0, 10, 1,
	),
	"entry_width": UserSettableParameter(
		"number",
		"Width of Entries",
		# value=2.66,
		value=3,
	),
	"entry_height": UserSettableParameter(
		"number",
		"Height of Entries",
		# value=1.5,
		value=3,
	),
	"kit_rooms": UserSettableParameter(
		"slider",
		"Number of Kitchens --> Pink Dots",
		1, 0, 10, 1,
	),
	"kit_width": UserSettableParameter(
		"number",
		"Width of Kitchens",
		# value=4.5,
		value=5,
	),
	"kit_height": UserSettableParameter(
		"number",
		"Height of Kitchens",
		# value=4,
		value=5,
	),
	"off_rooms": UserSettableParameter(
		"slider",
		"Number of Offices --> Blue Dots",
		1, 0, 10, 1,
	),
	"off_width": UserSettableParameter(
		"number",
		"Width of Offices",
		# value=3,
		value=3,
	),
	"off_height": UserSettableParameter(
		"number",
		"Height of Offices",
		# value=3.33,
		value=3,
	),
	"corr_rooms": UserSettableParameter(
		"slider",
		"Number of Corridors --> Aqua Dots",
		1, 0, 10, 1,
	),
	"corr_width": UserSettableParameter(
		"number",
		"Width of Corridors",
		value=1,
	),
	"corr_height": UserSettableParameter(
		"number",
		"Height of Corridors",
		value=11,
	),
	"bath_rooms": UserSettableParameter(
		"slider",
		"Number of Baths --> Dark Cyan Dots",
		1, 0, 10, 1,
	),
	"bath_width": UserSettableParameter(
		"number",
		"Width of Baths",
		value=3,
	),
	"bath_height": UserSettableParameter(
		"number",
		"Height of Baths",
		value=5,
	),
}

server = ModularServer(BuildingModel, [grid, building_element], "Building Model", model_params)
# server.max_steps = 1000
server.port = 8521
