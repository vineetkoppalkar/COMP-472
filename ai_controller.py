import math
import copy
import random

class AIController:
  player_one = None
  player_two = None
  game_end_status = None

  def __init__(self, player_one, player_two):
    self.player_one = player_one
    self.player_two = player_two 

  def has_won(self, grid, player_token, opponent_token):
    for i in range(grid.height):
      for j in range(grid.width):
        has_won_game = grid.check_for_x(player_token, opponent_token, i, j)
        if has_won_game:
          return True
        else:
          continue
    
  def has_game_ended(self, grid):
    # check if player won
    if self.has_won(grid, self.player_one.token, self.player_two.token):
      self.game_end_status = "Player won"
      return True

    # check if AI won
    if self.has_won(grid, self.player_two.token, self.player_one.token):
      self.game_end_status = "AI won"
      return True

    # # check if we ran out of tokens
    # self.game_end_status = "Ran out of tokens"

    # # check if we ran out of moves
    # self.game_end_status = "No more moves"

    self.game_end_status = "Game has not ended"
    return False

  def minimax(self, grid, depth, is_max_player):
    has_game_ended = self.has_game_ended(grid)
    if depth is 0 or has_game_ended:
      if has_game_ended:
        if self.game_end_status == "Player won":
          return OptimalChoice(-1, -1, -math.inf)
        elif self.game_end_status == "AI won":
          return OptimalChoice(-1, -1, math.inf)
        else:
          # Ran out of tokens or no more moves
          return OptimalChoice(-1, -1, 0)
      else:
        # Reached depth 0
        return OptimalChoice(-1, -1, self.calculate_grid_score(grid))

    if is_max_player:
      optimal_choice = self.random_optimal_choice(grid, -math.inf)
     
      for i in range(grid.height):
        for j in range(grid.width):
          if grid.is_occupied(i, j):
            continue

          grid_copy = copy.copy(grid)
          grid.insert_coords(i, j, self.player_two.token)

          new_optimal_choice = self.minimax(grid_copy, depth - 1, False)
          if new_optimal_choice.value > optimal_choice.value:
              optimal_choice.x = i
              optimal_choice.y = j
              optimal_choice.value = new_optimal_choice.value
      
      return optimal_choice
      
    else:
      optimal_choice = self.random_optimal_choice(grid, math.inf)

      for i in range(grid.height):
        for j in range(grid.width):
          if grid.is_occupied(i, j):
            continue

          grid_copy = copy.copy(grid)
          grid.insert_coords(i, j, self.player_one.token)

          new_optimal_choice = self.minimax(grid_copy, depth - 1, True)
          if new_optimal_choice.value < optimal_choice.value:
            optimal_choice.x = i
            optimal_choice.y = j
            optimal_choice.value = new_optimal_choice.value

      return optimal_choice

  def calculate_grid_score(self, grid):
    score = 0
    for i in range(grid.height):
      for j in range(grid.width):
        score += grid.get_score(self.player_two.token, self.player_one.token, i, j)
    return score

  def random_optimal_choice(self, grid, value):
    x = -1
    y = -1

    is_coordinate_valid = False
    while not is_coordinate_valid:
      x = random.randint(1, grid.width)
      y = random.randint(1, grid.height)
      is_coordinate_valid = True if not grid.is_occupied(x, y) else False

    return OptimalChoice(x, y, value)

class OptimalChoice:
  x = 0
  y = 0
  value = 0

  def __init__(self, x, y, value):
    self.x = x
    self.y = y 
    self.value = value