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

  # Pseudo code for move
  # if not num_current_player_tokens == 0:
  # do minimax as usual
  # else:
  # do not check cell that does not have a player token adjacent to it
  # remove that adjacent cell
  
  # def move_minimax(self, grid, depth, alpha, beta, is_max_player):

  def minimax(self, grid, depth, alpha, beta, is_max_player):
    has_game_ended = self.has_game_ended(grid)
    if depth == 0 or has_game_ended:
      return OptimalChoice(-1, -1, self.calculate_grid_score(grid, is_max_player))

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

  def minimax_move(self, grid, depth, alpha, beta, is_max_player):
    has_game_ended = self.has_game_ended(grid)
    if depth == 0 or has_game_ended:
      return OptimalMoveChoice(-1, -1, -1, -1, self.calculate_grid_score(grid, is_max_player))

    if is_max_player:
      optimal_move_choice = OptimalMoveChoice(-1, -1, -1, -1, -math.inf)
       
      should_prune = False
      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if should_prune:
            break
          
          if not grid.get_cell_state(i, j) == self.player_two.token:
            continue

          adjacent_cells = grid.get_all_adjacent_cells(i, j)
          for cell in adjacent_cells:
            grid_copy = copy.deepcopy(grid)

            # Move here
            move_to_row_index = cell[0]
            move_to_col_index = cell[1]

            grid_copy.move_token(i, j, move_to_row_index, move_to_col_index)
            new_optimal_move_choice = self.minimax(grid_copy, depth - 1, alpha, beta, False)

            if new_optimal_move_choice.value > optimal_move_choice.value:
              optimal_move_choice.from_x = i
              optimal_move_choice.from_y = j
              optimal_move_choice.to_x = move_to_row_index
              optimal_move_choice.to_y = move_to_col_index
              optimal_move_choice.value = new_optimal_move_choice.value

            alpha = max(alpha, optimal_move_choice.value)
            if alpha >= beta:
              should_prune = True
              break
            
      return optimal_move_choice
    else:
      optimal_move_choice = OptimalMoveChoice(-1, -1, -1, -1, math.inf)
      should_prune = False
      for i in range(grid.height):
        if should_prune:
          break
        for j in range(grid.width):
          if should_prune:
            break
          
          if not grid.get_cell_state(i, j) == self.player_one.token:
            continue

          adjacent_cells = grid.get_all_adjacent_cells(i, j)
          for cell in adjacent_cells:
            grid_copy = copy.deepcopy(grid)

            # Move here
            move_to_row_index = cell[0]
            move_to_col_index = cell[1]

            grid_copy.move_token(i, j, move_to_row_index, move_to_col_index)
            new_optimal_choice = self.minimax(grid_copy, depth - 1, alpha, beta, True)

            if new_optimal_move_choice.value < optimal_move_choice.value:
              optimal_move_choice.from_x = i
              optimal_move_choice.from_y = j
              optimal_move_choice.to_x = move_to_row_index
              optimal_move_choice.to_y = move_to_col_index
              optimal_move_choice.value = new_optimal_move_choice.value

            alpha = min(alpha, optimal_move_choice.value)
            if alpha >= beta:
              should_prune = True
              break
            
      return optimal_move_choice
       
  def calculate_grid_score(self, grid, is_max_player):
    player_one_score = 0
    player_two_score = 0

    for i in range(grid.height):
      for j in range(grid.width):
        if grid.get_cell_state(i, j) == self.player_one.token:
          player_one_score += grid.get_cell_score(self.player_one.token, self.player_two.token, i, j)
        elif grid.get_cell_state(i, j) == self.player_two.token:
          player_two_score += grid.get_cell_score(self.player_two.token, self.player_one.token, i, j)

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

      return OptimalChoice(row_index, col_index, value)


class OptimalChoice:
    x = 0
    y = 0
    value = 0

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

class OptimalMoveChoice:
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