import os


def setup_board(width, height):
  gridline = []
  for i in range(height):
    gridline.append("[ ]")

  grid = []
  for i in range(width):
    grid.append(list(gridline))
  
  return grid

def parseUserInput(user_input):
  letter = user_input[0]
  number = int(user_input[1:])

  input_coords = {}
  input_coords['letter'] = letter
  input_coords['number'] = number

  return input_coords
  
def display_grid(grid):
  width = len(grid)
  height = len(grid[0])

  for i in range(height):
    print(str(height - i).ljust(3), end = '')
    for j in range(width):
      print(grid[j][i] + " ", end = '')
    print()

  print(" ".ljust(4), end = '')
  for i in range(width):
    print(chr(65 + i).ljust(4), end = '')
  print()

def insert_coords(grid, input_coords, token_type):
  height = len(grid[0])
  row_index = height - input_coords.get("number")
  col_index = ord(input_coords.get("letter")) - 65

  grid[col_index][row_index] = "[" + token_type + "]"

def main():
  width = 12
  height = 10

  grid = setup_board(width, height)
  display_grid(grid)

  while True:
    user_input = input("\nPlease enter coord: ")
    input_coords = parseUserInput(user_input)
    print("(" + input_coords.get("letter") + ", " + str(input_coords.get("number")) + ")\n")
    insert_coords(grid, input_coords, "X")
    display_grid(grid)

if __name__ == '__main__':
    main()