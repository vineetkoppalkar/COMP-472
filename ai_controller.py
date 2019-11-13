import math
import copy
from lightweight_grid import LightweightGrid
import random


class AIController:
  player_one = None
  player_two = None
  game_end_status = None
  number_of_moves = None

  def __init__(self, player_one, player_two, number_of_moves):
    self.player_one = player_one
    self.player_two = player_two
    self.number_of_moves = number_of_moves

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

    self.game_end_status = "Game has not ended"
    return False

  def minimax(self, grid, depth, alpha, beta, is_max_player):
    has_game_ended = self.has_game_ended(grid)
    if depth == 0 or has_game_ended:
      return OptimalChoice(-1, -1, -1, -1, self.calculate_grid_score(grid, is_max_player))

    if is_max_player:
      optimal_choice = OptimalChoice(-1, -1, -1, -1, -math.inf)
      should_prune = False
      
      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if should_prune:
            break
          
          current_cell_state = grid.get_cell_state(i, j)
          if current_cell_state == self.player_one.token:
            continue
          
          if current_cell_state == self.player_two.token:
            # Handle move
            adjacent_cells = grid.get_all_adjacent_cells(i, j)
            for cell in adjacent_cells:
              grid_copy = copy.deepcopy(grid)

              # Move here
              move_to_row_index = cell[0]
              move_to_col_index = cell[1]

              grid_copy.move_token(i, j, move_to_row_index, move_to_col_index)
              new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, False)

              if new_optimal_choice.value > optimal_choice.value:
                optimal_choice.from_x = i
                optimal_choice.from_y = j
                optimal_choice.to_x = move_to_row_index
                optimal_choice.to_y = move_to_col_index
                optimal_choice.value = new_optimal_choice.value

              alpha = max(alpha, optimal_choice.value)
              if alpha >= beta:
                should_prune = True
                break

          elif self.player_two.number_of_tokens > 0:
            # Handle place
            grid_copy = copy.deepcopy(grid)
            grid_copy.insert_coords(i, j, self.player_two.token)
            new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, False)

            if new_optimal_choice.value > optimal_choice.value:
              optimal_choice.from_x = i
              optimal_choice.from_y = j
              optimal_choice.to_x = -1
              optimal_choice.to_y = -1

              optimal_choice.value = new_optimal_choice.value

            alpha = max(alpha, optimal_choice.value)
            if alpha >= beta:
              should_prune = True
              break
        
      return optimal_choice

    else:
      optimal_choice = OptimalChoice(-1, -1, -1, -1, math.inf)
      should_prune = False

      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if should_prune:
            break
          
          current_cell_state = grid.get_cell_state(i, j)
          if current_cell_state == self.player_two.token:
            continue
          
          if current_cell_state == self.player_one.token:
            # Hanles moving a token
            adjacent_cells = grid.get_all_adjacent_cells(i, j)
            for cell in adjacent_cells:
              grid_copy = copy.deepcopy(grid)

              # Move here
              move_to_row_index = cell[0]
              move_to_col_index = cell[1]

              grid_copy.move_token(i, j, move_to_row_index, move_to_col_index)
              new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, True)

              if new_optimal_choice.value <  optimal_choice.value:
                optimal_choice.from_x = i
                optimal_choice.from_y = j
                optimal_choice.to_x = move_to_row_index
                optimal_choice.to_y = move_to_col_index
                optimal_choice.value = new_optimal_choice.value

              alpha = min(alpha,  optimal_choice.value)
              if alpha >= beta:
                should_prune = True
                break
          elif self.player_one.number_of_tokens > 0:
            # Handles placing a token
            grid_copy = copy.deepcopy(grid)
            grid_copy.insert_coords(i, j, self.player_one.token)

            new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, True)

            if new_optimal_choice.value < optimal_choice.value:
              optimal_choice.from_x = i
              optimal_choice.from_y = j
              optimal_choice.to_x = -1
              optimal_choice.to_y = -1
              optimal_choice.value = new_optimal_choice.value

            beta = min(beta, optimal_choice.value)
            if alpha >= beta:
              should_prune = True
              break

      return optimal_choice
       
  def calculate_grid_score(self, grid, is_max_player):
    player_one_score = 0
    player_two_score = 0

    for i in range(grid.height):
      for j in range(grid.width):
        if grid.get_cell_state(i, j) == self.player_one.token:
          player_one_score += grid.get_cell_score(self.player_one.token, self.player_two.token, i, j)
        elif grid.get_cell_state(i, j) == self.player_two.token:
          player_two_score += grid.get_cell_score(self.player_two.token, self.player_one.token, i, j)

    if player_two_score == math.inf and player_one_score == math.inf:
        print("both player scores are inf")
        return math.inf 

    return player_two_score - player_one_score

  def random_optimal_choice(self, grid, value):
      row_index = -1
      col_index = -1

      is_coordinate_valid = False
      while not is_coordinate_valid:
          # Don't pick coordinates at the edges of the grid
          row_index = random.randint(1, grid.height - 2)
          col_index = random.randint(1, grid.width - 2)

          is_coordinate_valid = True if not grid.is_occupied(row_index, col_index) else False

      return OptimalChoice(row_index, col_index, -1, -1, value)

class OptimalChoice:
  from_x = 0
  from_y = 0
  to_x = 0
  to_y = 0
  value = 0

  def __init__(self, from_x, from_y, to_x, to_y, value):
      self.from_x = from_x
      self.from_y = from_y
      self.to_x = to_x
      self.to_y = to_y
      self.value = value