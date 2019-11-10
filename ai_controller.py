import math
import copy
from lightweight_grid import LightweightGrid
import random


class AIController:
  player_one = None
  player_two = None
  game_end_status = None
  is_first_placement = False

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

  def minimax(self, grid, depth, alpha, beta, is_max_player):
    has_game_ended = self.has_game_ended(grid)
    if depth == 0 or has_game_ended:
      return self.calculate_grid_score(grid, is_max_player)
      # return self.test_calculate_grid_score(grid, is_max_player, row_index, col_index)

    #   if has_game_ended:
    #     if self.game_end_status == "Player won":
    #       return OptimalChoice(-1, -1, -math.inf)
    #     elif self.game_end_status == "AI won":
    #       return OptimalChoice(-1, -1, math.inf)
    #     else:
    #       # Ran out of tokens or no more moves
    #       return OptimalChoice(-1, -1, 0)
    #   else:
    #     # Reached depth 0
    #     return OptimalChoice(-1, -1, self.calculate_grid_score(grid))

    if is_max_player:
      optimal_choice = self.random_optimal_choice(grid, -math.inf)

      should_prune = False
      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if grid.is_occupied(i, j):
            continue

          grid_copy = copy.deepcopy(grid)
          grid_copy.insert_coords(i, j, self.player_two.token)
          new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, False)

          if new_optimal_choice.value > optimal_choice.value:
            optimal_choice.x = i
            optimal_choice.y = j
            optimal_choice.value = new_optimal_choice.value

          alpha = max(alpha, optimal_choice.value)
          if alpha >= beta:
            should_prune = True
            break
        
      return optimal_choice

    else:
      optimal_choice = self.random_optimal_choice(grid, math.inf)
      should_prune = False

      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if grid.is_occupied(i, j):
            continue

          grid_copy = copy.deepcopy(grid)
          grid_copy.insert_coords(i, j, self.player_one.token)

          new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, True)

          if new_optimal_choice.value < optimal_choice.value:
            optimal_choice.x = i
            optimal_choice.y = j
            optimal_choice.value = new_optimal_choice.value

          beta = min(beta, optimal_choice.value)
          if alpha >= beta:
            should_prune = True
            break

      return optimal_choice

  def calculate_grid_score(self, grid, is_max_player):
    player_one_score = 0
    player_two_score = 0

    optimal_choice = OptimalChoice(-1, -1, -1)

    for i in range(grid.height):
      for j in range(grid.width):
        if grid.get_cell_state(i, j) == self.player_one.token:
          player_one_score += grid.get_cell_score(self.player_one.token, self.player_two.token, i, j)
        elif grid.get_cell_state(i, j) == self.player_two.token:
          player_two_score += grid.get_cell_score(self.player_two.token, self.player_one.token, i, j)

    optimal_choice.value = player_two_score - player_one_score
    
    # if is_max_player:
    #   optimal_choice.value = player_two_score - player_one_score
    # else:
    #   optimal_choice.value = player_one_score - player_two_score
      
        # result = grid.get_cell_score(self.player_two.token, self.player_one.token, i, j)
        # if result == math.inf or result == -math.inf:
        #   optimal_choice.value = result 
        #   return optimal_choice
        # # else:
        #   # if is_max_player and result > score:
        #   #   # score += result
        #   #   optimal_choice.value += result 

        #   # elif not is_max_player and result < score:
        #   #   # score -= result
        #   #   optimal_choice.value -= result 

        # else:
        #   if is_max_player and result > optimal_choice.value:
        #     optimal_choice.x = i
        #     optimal_choice.y = j
        #     optimal_choice.value = result 
        #   elif not is_max_player and result < optimal_choice.value:
        #     optimal_choice.x = i
        #     optimal_choice.y = j
        #     optimal_choice.value = result 
    return optimal_choice

  # def test_calculate_grid_score(self, grid, is_max_player, row_index, col_index):
  #   optimal_choice = OptimalChoice(row_index, col_index, 0)

  #   result = grid.get_cell_score(self.player_two.token, self.player_one.token, row_index, col_index)
  #   if result == math.inf or result == -math.inf:
  #     optimal_choice.value = result 
  #     return optimal_choice
  #   else:
  #     if is_max_player and result > optimal_choice.value:
  #       optimal_choice.value = result 
  #     elif not is_max_player and result < optimal_choice.value:
  #       optimal_choice.value = result

  #   return optimal_choice

  # def test_calculate_grid_score(self, grid):
  #   value_grid = Grid(grid.width, grid.height)
  #   highest_score = 0
  #   for i in range(grid.height):
  #     for j in range(grid.width):
  #       new_score = grid.get_score(self.player_two.token, self.player_one.token, i, j)
  #       if new_score == math.inf:
  #         highest_score = new_score
  #         return new_score
  #       elif new_score == -math.inf:
  #         highest_score = new_score
  #         return new_score
  #       elif highest_score < new_score:
  #         highest_score = highest_score 
  #       value_grid.insert_coords(i, j, str(highest_score))
  #   value_grid.display()
  #   return highest_score

  # def test_calculate_grid_score(self, grid):
  #     value_grid = Grid(grid.width, grid.height)
  #     score = 0
  #     for i in range(grid.height):
  #         for j in range(grid.width):
  #             cell_score = grid.get_score(self.player_two.token, self.player_one.token, i, j)
  #             score += cell_score
  #             value_grid.insert_coords(i, j, str(cell_score))
  #     value_grid.display()
  #     return score

  def random_optimal_choice(self, grid, value):
      row_index = -1
      col_index = -1

      is_coordinate_valid = False
      while not is_coordinate_valid:
          # Don't pick coordinates at the edges of the grid
          row_index = random.randint(1, grid.height - 2)
          col_index = random.randint(1, grid.width - 2)

          is_coordinate_valid = True if not grid.is_occupied(row_index, col_index) else False

      return OptimalChoice(row_index, col_index, value)


class OptimalChoice:
    x = 0
    y = 0
    value = 0

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
