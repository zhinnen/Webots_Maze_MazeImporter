#!/usr/bin/env python3.8
import math
from controller import Supervisor
from controller import Node
import MazeParser
import os
import signal

# load global variables
supervisor = Supervisor()  
timeStep = int(supervisor.getBasicTimeStep())

# ================ WALL FUNCTIONALITY ============================

# callback function to add a wall to the maze walls
#include intermediate structure in the main call
def add_maze_wall(wall,i):
  # wall shape:
  dx = wall.x2-wall.x1
  dy = wall.y2-wall.y1
  length = math.sqrt(dx*dx+dy*dy)
  size = "size {} {} {}".format(length,0.2,0.02)

  # calculate rotation
  rotation = f'rotation 0 1 0 {math.atan2(dy,dx)}'
  
  # calculate translation
  translation = f'translation {(wall.x1+wall.x2)/2} {0.02} {(wall.y1+wall.y2)/2}'
  
  # generate string to create wall and add it
  wall_def = f'Wall {{ {translation} {rotation} name "extra_wall_{i}" {size} }}'
  print(wall_def)
  maze_walls = supervisor.getFromDef("maze_walls").getField("children")
  maze_walls.importMFNodeFromString(maze_walls.getCount(),wall_def)
  #return AddMazeWallResponse()
  

# callback function to remove the maze wall given by the id
# return true if successful, false otherwise  
def remove_maze_wall(message):
  wall_def = "MAZE_WALL_{}".format(message.id)
  #print('def ', wall_def)
  wall = supervisor.getFromDef(wall_def)
  if wall is not None:
    wall.remove()
    return RemoveMazeWallResponse(True)
  else:
    return RemoveMazeWallResponse(False)
  

# callback function to remove all maze walls
def remove_all_maze_walls(empty_message):
  maze_walls = supervisor.getFromDef("maze_walls").getField("children")
  while maze_walls.getCount() > 0:
    maze_walls.removeMF(0)
  return EmptyResponse()
  
# ================ MAIN FUNCTION ==================================
i=1
walls, feeders, start_positions = MazeParser.parse_maze("M1.xml")
for index, row in walls.iterrows():
      add_maze_wall(row,i)
      i = i+1

while (supervisor.step(timeStep) != -1):
  pass
  
  
