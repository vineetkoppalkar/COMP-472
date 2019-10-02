from grid import Grid
from player import Player
import re

class GameController:
  player_one = None
  player_two = None
  grid = None
  is_player_one_turn = True
  number_of_tokens = None

  def __init__(self, player_one, player_two, grid, number_of_turns):
    self.player_one = player_one
    self.player_two = player_two 
    self.grid = grid
    self.number_of_turns = number_of_turns

  def parse_input_coord(self, input_coords):
    is_valid_input = re.match('^([A-L]|[a-l])((10)|[1-9])$', input_coords)

    if is_valid_input is None:
      return None

    letter = input_coords[0]
    number = int(input_coords[1:])

    print("(" + letter + ", " + str(number) + ")\n")

    row_index = self.grid.height - number
    col_index = ord(letter) - 65

    input_coords = {}
    input_coords['col'] = col_index
    input_coords['row'] = row_index

    return input_coords
  
  def play(self):
    while True:
      current_player = self.player_one if self.is_player_one_turn else self.player_two  

      input_coords = None     # From
      to_input_coords = None  # To

      is_input_valid = False
      is_move_action = False
      while not is_input_valid:
        self.grid.display()

        player_input = input("\n" + current_player.name + ", please enter coord: ")
        input_coords = self.parse_input_coord(player_input)

        if input_coords is None:
          print("Please enter a letter [A-L] followed by a number [1-10]")
          continue
 
        has_selected_empty_cell = self.grid.is_occupied(input_coords.get("row"), input_coords.get("col"))
        if not has_selected_empty_cell:
          cell_state = self.grid.get_cell_state(input_coords.get("row"), input_coords.get("col"))
          if cell_state is current_player.token:
            is_move_action = True
          else:
            print("This cell is occupied")
            continue

        is_input_valid = True

      if is_move_action:
        is_input_valid = False
        while not is_input_valid:
          self.grid.display()

          player_input = input("\n" + current_player.name + ", where would you like to move this token?: ")
          to_input_coords = self.parse_input_coord(player_input)

          if to_input_coords is None:
            print("Please enter a letter [A-L] followed by a number [1-10]")
            continue

          has_selected_empty_cell = self.grid.is_occupied(to_input_coords.get("row"), to_input_coords.get("col"))
          if not has_selected_empty_cell:
            print("This cell is occupied")
            continue

          is_input_valid = True

      if is_move_action:
        self.grid.move_token(input_coords.get("row"), input_coords.get("col"), to_input_coords.get("row"), to_input_coords.get("col"))
      else:
        self.grid.insert_coords(input_coords.get("row"), input_coords.get("col"), current_player.token)

      self.is_player_one_turn = not self.is_player_one_turn
      self.number_of_turns -= 1

      if self.number_of_turns is 0:
        print("You have reached a draw")
        break  

  def reset_game(self):
    self.grid = self.grid.clear()
    self.number_of_tokens = 30
    self.is_player_one_turn = True
