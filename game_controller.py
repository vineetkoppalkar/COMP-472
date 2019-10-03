from grid import Grid
from player import Player
import re
import sys

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
    is_valid_input = re.match('([A-L]|[a-l])((10)|[1-9])$', input_coords)

    if is_valid_input is None:
      return None

    letter = input_coords[0].upper()
    number = int(input_coords[1:])

    print("(" + letter + ", " + str(number) + ")\n")

    row_index = self.grid.height - number
    col_index = ord(letter) - 65

    input_coords = {}
    input_coords['col'] = col_index
    input_coords['row'] = row_index

    return input_coords

  def check_for_win(self, player_name, opponent_token, row_index, col_index):
    has_player_won = self.grid.check_for_x(row_index, col_index, opponent_token)
    if has_player_won:
      self.exit_program("\n" + player_name + " You win!")

  def exit_program(self, message):
    print("_____________________________________________________")
    print(message)
    print("_____________________________________________________\n")
    self.grid.display()
    sys.exit()

  def win_status_check(self, player_name, opponent_token, row_index, col_index):
    # Center section
    self.check_for_win(player_name, opponent_token, row_index, col_index)

    # Top-left section
    self.check_for_win(player_name, opponent_token, row_index - 1, col_index - 1)

    # Top-right section
    self.check_for_win(player_name, opponent_token, row_index - 1, col_index + 1)

    # Bottom-left section
    self.check_for_win(player_name, opponent_token, row_index + 1, col_index - 1)

    # Bottom-right section
    self.check_for_win(player_name, opponent_token, row_index + 1, col_index + 1)
  
  def play(self):
    while True:
      current_player = self.player_one if self.is_player_one_turn else self.player_two  
      current_opponent = self.player_two if self.is_player_one_turn else self.player_one

      input_coords = None
      row_index = None
      col_index = None

      move_coords = None
      move_row_index = None
      move_col_index = None

      is_input_valid = False
      is_move_action = False

      while not is_input_valid:
        self.grid.display()

        player_input = input("\n" + current_player.name + ", please enter coord: ")
        input_coords = self.parse_input_coord(player_input)

        if input_coords is None:
          print("Please enter a letter [A-L] followed by a number [1-10]")
          continue
          
        row_index = input_coords.get("row")
        col_index = input_coords.get("col")

        has_selected_empty_cell = self.grid.is_occupied(row_index, col_index)
        if not has_selected_empty_cell:
          cell_state = self.grid.get_cell_state(row_index, col_index)
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
          move_coords = self.parse_input_coord(player_input)

          if move_coords is None:
            print("Please enter a letter [A-L] followed by a number [1-10]")
            continue

          move_row_index = move_coords.get("row")
          move_col_index = move_coords.get("col")

          has_selected_empty_cell = self.grid.is_occupied(move_row_index, move_col_index)
          if not has_selected_empty_cell:
            print("This cell is occupied")
            continue

          is_input_valid = True

      if is_move_action:
        self.grid.move_token(row_index, col_index, move_row_index, move_col_index)  

        # self.win_status_check(current_opponent.name, current_player.token, row_index, col_index - 1)
        # self.win_status_check(current_opponent.name, current_player.token, row_index, col_index + 1)
              
        row_index = move_row_index
        col_index = move_col_index
      else:
        self.grid.insert_coords(row_index, col_index, current_player.token)

      # Check for win condition
      self.win_status_check(current_player.name, current_opponent.token, row_index, col_index)
      
      self.is_player_one_turn = not self.is_player_one_turn
      self.number_of_turns -= 1

      if self.number_of_turns is 0:
        self.exit_program("You have reached a draw")
