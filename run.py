from abm_project.server import server

#-----When in Windows comment out line 4 and 5 -------
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#-----------------------------------------------------

server.launch()
