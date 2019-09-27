from grid import Grid
from player import Player

class GameController:
  player_one = None
  player_two = None
  grid = None
  is_player_one_turn = True
  number_of_tokens = None

  def __init__(self, player_one, player_two, grid, number_of_tokens):
    self.player_one = player_one
    self.player_two = player_two
    self.grid = grid
    self.number_of_tokens = number_of_tokens

  def parse_input_coord(self, input_coords):
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
    self.grid.display()

    while True:
      current_player = self.player_one if self.is_player_one_turn else self.player_two

      player_input = input("\n" + current_player.name + ", please enter coord: ")
      input_coords = self.parse_input_coord(player_input)
      valid_move = self.grid.insert_coords(input_coords.get("row"), input_coords.get("col"), current_player.token)
      
      while not valid_move:
        self.grid.display()
        player_input = input("\n" + current_player.name + ", this cell is already occupied. Please enter new coord: ")
        input_coords = self.parse_input_coord(player_input)
        valid_move = self.grid.insert_coords(input_coords.get("row"), input_coords.get("col"), current_player.token)
      
      self.grid.display()
      self.is_player_one_turn = not self.is_player_one_turn
      self.number_of_tokens -= 1

      if self.number_of_tokens is 0:
        print("You have reached a draw")
        break

  def reset_game(self):
    self.grid = self.grid.clear()
    self.number_of_tokens = 30
    self.is_player_one_turn = True
