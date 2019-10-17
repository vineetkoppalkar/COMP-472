from grid import Grid
from game_controller import GameController
from player import Player

def parseUserInput(user_input):
  letter = user_input[0]
  number = int(user_input[1:])

  input_coords = {}
  input_coords['letter'] = letter
  input_coords['number'] = number

  return input_coords

def main():
  width = 12
  height = 10

  total_number_of_tokens = 4
  total_number_of_moves = 1

  player_one = Player("Player 1", 'X', total_number_of_tokens//2)
  player_two = Player("Player 2", 'O', total_number_of_tokens//2)
  grid = Grid(width, height)

  game_controller = GameController(player_one, player_two, grid, total_number_of_tokens, total_number_of_moves)
  game_controller.play()

if __name__ == '__main__':
    main()