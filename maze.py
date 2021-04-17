import numpy as np
import random as rand
import matplotlib.pyplot as plt

def plot(x, y):

  plt.plot(x, y, 'k')

class Cell:

  def __init__(self, x, y):

    self.position = (x, y)
    self.visited = False
    self.walls = {x:1 for x in ['N', 'S', 'E', 'W']}
    self.neighbors = {'N': (x, y+1), 'S': (x, y-1), 'E': (x+1, y), 'W': (x-1, y)}
  
  def check_neighbors(self, grid):

    DIRS = ['N', 'S', 'E', 'W']
    rand.shuffle(DIRS)
    for DIR in DIRS:
      if self.neighbors[DIR] in grid.cells and grid.cells[self.neighbors[DIR]].visited == False:
        return DIR, self.neighbors[DIR]
        break
      else:
        continue
  
  def plot(self):

    wall_list = [i for i in self.walls if self.walls[i] == 1]
    if 'N' in wall_list:
      x = [self.position[0] - 0.5, self.position[0] + 0.5]
      y = [self.position[1] + 0.5, self.position[1] + 0.5]
      plot(x, y)
    if 'S' in wall_list:
      x = [self.position[0] - 0.5, self.position[0] + 0.5]
      y = [self.position[1] - 0.5, self.position[1] - 0.5]
      plot(x, y)
    if 'E' in wall_list:
      x = [self.position[0] + 0.5, self.position[0] + 0.5]
      y = [self.position[1] - 0.5, self.position[1] + 0.5]
      plot(x, y)
    if 'W' in wall_list:
      x = [self.position[0] - 0.5, self.position[0] - 0.5]
      y = [self.position[1] - 0.5, self.position[1] + 0.5]
      plot(x, y)


class Grid:

  def __init__(self, x_len, y_len):
    self.x_len = x_len
    self.y_len = y_len

    x = [x for x in range(x_len)]
    y = [y for y in range(y_len)]
    self.cells = {(i, j) : Cell(x[i], y[j]) for j in y for i in x}
  
  def create_maze(self, start_cell):

    self.cells[start_cell].visited = True
    self.stack = [self.cells[start_cell]]

    while len(self.stack) != 0:
      current = self.stack.pop(-1)
      # Check neighbors, pick an unvisited one randomly
      try:
        #DIR = None
        DIR, neighbor_index = current.check_neighbors(self)
        if DIR is None:
          continue
        else:
          DIR_MAP = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
          current.walls[DIR] = 0
          self.stack.append(current)
          self.cells[neighbor_index].walls[DIR_MAP[DIR]] = 0
          self.cells[neighbor_index].visited = True
          self.stack.append(self.cells[neighbor_index])
          # Remove wall between them, mark as visited, push to stack
          # Recurse again until nothing left in stack
      except:
        print('recursing...')
        continue
        # If no neighbors are unvisited, pop again and try once more
    
    # Add code here to determine start and end points, and edit them
    edges = []
    for cell in self.cells:
      if 0 in self.cells[cell].position or self.x_len - 1 in self.cells[cell].position or self.y_len - 1 in self.cells[cell].position:
        edges.append(self.cells[cell])
    
    lst = rand.sample(edges, 2)
    self.start = lst[0]
    self.end = lst[1]
    for i in range(2):
      if self.cells[lst[i].position].position[0] == 0:
        self.cells[lst[i].position].walls['W'] = 0
      elif self.cells[lst[i].position].position[0] == self.x_len - 1:
        self.cells[lst[i].position].walls['E'] = 0
        self.start_dir = 'W'
      elif self.cells[lst[i].position].position[1] == 0:
        self.cells[lst[i].position].walls['S'] = 0
      elif self.cells[lst[i].position].position[1] == self.y_len - 1:
        self.cells[lst[i].position].walls['N'] = 0

  def solve(self):

    print(self.start.position, self.end.position)
    position = self.start

    print(self.start_dir)

    '''while position != self.end:
      pass'''

def main():
  rand.seed(100)

  grid = Grid(10, 10)
  grid.create_maze((0, 0))

  for cell in grid.cells:
    grid.cells[cell].plot()
  
  grid.solve()
  
  plt.gca().set_aspect('equal', adjustable='box')
  plt.show()
  #plt.savefig('fig.png')
  
if __name__ == '__main__':
  main()
