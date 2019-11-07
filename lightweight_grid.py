import math

class LightweightGrid:
    grid_cells = None
    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_cells = self.setup_board()

    def setup_board(self):
        grid = []
        for i in range(self.height):
            gridline = []
            for j in range(self.width):
                gridline.append(" ")
            grid.append(gridline)

        return grid

    def insert_coords(self, row_index, col_index, token_type):
        if self.grid_cells[row_index][col_index] == " ":
            self.grid_cells[row_index][col_index] = token_type
            return True
        else:
            return False

    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid_cells[i][j] = " "

    def is_occupied(self, row_index, col_index):
        return not self.grid_cells[row_index][col_index] == " "

    def get_cell_state(self, row_index, col_index):
        return self.grid_cells[row_index][col_index]

    def move_token(self, from_row, from_col, to_row, to_col):
        self.grid_cells[to_row][to_col] = self.grid_cells[from_row][from_col]
        self.grid_cells[from_row][from_col] = " "

    def is_valid_adjacent_cell(self, row_index, col_index, move_row_index, move_col_index):    
        # top-left
        if row_index - 1 == move_row_index and col_index - 1 == move_col_index:
            return True

        # top-middle
        if row_index - 1 == move_row_index and col_index == move_col_index:
            return True

        # top-right
        if row_index - 1 == move_row_index and col_index + 1 == move_col_index:
            return True
        
        # left
        if row_index == move_row_index and col_index - 1 == move_col_index:
            return True

        # right
        if row_index == move_row_index and col_index + 1 == move_col_index:
            return True

        # bottom-left
        if row_index + 1 == move_row_index and col_index - 1 == move_col_index:
            return True

        # bottom-middle
        if row_index + 1 == move_row_index and col_index == move_col_index:
            return True

        # bottom-right
        if row_index + 1 == move_row_index and col_index + 1 == move_col_index:
            return True

        return False

    def check_for_x(self, player_token, opponent_token, row_index, col_index):
        if not self.is_section_within_grid(row_index, col_index):
            return False

        # If cell is empty, then don't bother continuing to check for X
        center_cell = self.grid_cells[row_index][col_index]
        if center_cell == " ":
            return False

        # Check if crossed out
        right_cell_state = self.grid_cells[row_index][col_index - 1]
        left_cell_state = self.grid_cells[row_index][col_index + 1]
        if right_cell_state is opponent_token and left_cell_state is opponent_token:
            return False

        # Check if win condition
        top_left_cell_state = self.grid_cells[row_index - 1][col_index - 1]
        top_right_cell_state = self.grid_cells[row_index - 1][col_index + 1]
        center_cell_state = center_cell
        bottom_left_cell_state = self.grid_cells[row_index + 1][col_index - 1]
        bottom_right_cell_state = self.grid_cells[row_index + 1][col_index + 1]

        cell_states = [center_cell_state, top_left_cell_state, top_right_cell_state, bottom_left_cell_state, bottom_right_cell_state]

        return all(state == player_token for state in cell_states)

    def is_section_within_grid(self, row_index, col_index):
        # Check edge cases
        if row_index - 1 < 0 or row_index + 1 >= self.height:
            return False
        if col_index - 1 < 0 or col_index + 1 >= self.width:
            return False
        return True
    
    def get_section_score(self, player_token, opponent_token, row_index, col_index):
        num_player_tokens = 0
        num_opponent_tokens = 0
        
        # Center
        center_cell_state = self.grid_cells[row_index][col_index]
        if center_cell_state == player_token:
            num_player_tokens += 1
        elif center_cell_state == opponent_token:
            num_opponent_tokens += 1
        
        # Top-left
        top_left_cell_state = None
        if col_index - 1 >= 0 and row_index - 1 >= 0:
            top_left_cell_state = self.grid_cells[row_index - 1][col_index - 1]
            if top_left_cell_state == player_token:
                num_player_tokens += 1
            elif top_left_cell_state == opponent_token:
                num_opponent_tokens += 1

        # Top-right
        top_right_cell_state = None
        if col_index + 1 < self.width and row_index - 1 >= 0:
            top_right_cell_state = self.grid_cells[row_index - 1][col_index + 1]
            if top_right_cell_state == player_token:
                num_player_tokens += 1
            elif top_right_cell_state == opponent_token:
                num_opponent_tokens += 1

        # Bottom-left
        bottom_left_cell_state = None
        if col_index - 1 >= 0 and row_index + 1 < self.height:
            bottom_left_cell_state = self.grid_cells[row_index + 1][col_index - 1]
            if bottom_left_cell_state == player_token:
                num_player_tokens += 1
            elif bottom_left_cell_state == opponent_token:
                num_opponent_tokens += 1

        # Bottom-right
        bottom_right_cell_state = None
        if col_index + 1 < self.width and row_index + 1 < self.height:
            bottom_right_cell_state = self.grid_cells[row_index + 1][col_index + 1]
            if bottom_right_cell_state == player_token:
                num_player_tokens += 1
            elif bottom_right_cell_state == opponent_token:
                num_opponent_tokens += 1

        cell_states = [center_cell_state, top_left_cell_state, top_right_cell_state, bottom_left_cell_state, bottom_right_cell_state]
        
        # If player has a X, set score to infinity
        has_won = False
        if all(state == player_token for state in cell_states):
            has_won = True

        # Check if crossed out
        is_left_state_occupied = False
        if col_index - 1 >= 0:
            left_cell_state = self.grid_cells[row_index][col_index - 1]
            is_left_state_occupied = True if left_cell_state == opponent_token else False

        is_right_state_occupied = False
        if col_index + 1 < self.width:
            right_cell_state = self.grid_cells[row_index][col_index + 1]
            is_right_state_occupied = True if right_cell_state == opponent_token else False
        
        # If player has made X pattern but it is crossed out, return -infinity
        is_crossed_out = is_left_state_occupied and is_right_state_occupied
        if has_won and is_crossed_out:
            return -math.inf
        elif has_won:
            return math.inf
        
        # If the X pattern is filled but doesn't form a winning X, return 0 score for this pattern        
        if all(state == player_token or state == opponent_token for state in cell_states):
            return 0 

        return math.factorial(num_player_tokens) - math.factorial(num_opponent_tokens)

    def get_score(self, player_token, opponent_token, row_index, col_index):
        # Center section
        center_score = -1
        if self.is_section_within_grid(row_index, col_index):
            if self.get_cell_state(row_index, col_index) != opponent_token:
                center_score = self.get_section_score(player_token, opponent_token, row_index, col_index)
                if center_score == math.inf or center_score == -math.inf:
                    return center_score

        # Top-left section
        top_left_score = -1
        if self.is_section_within_grid(row_index - 1, col_index - 1):
            if self.get_cell_state(row_index - 1, col_index - 1) != opponent_token:
                top_left_score = self.get_section_score(player_token, opponent_token, row_index - 1, col_index - 1)
                if top_left_score == math.inf or top_left_score == -math.inf:
                    return top_left_score
            
        # Top-right section
        top_right_score = -1
        if self.is_section_within_grid(row_index - 1, col_index + 1):
            if self.get_cell_state(row_index - 1, col_index + 1) != opponent_token:
                top_right_score = self.get_section_score(player_token, opponent_token, row_index - 1, col_index + 1)
                if top_right_score == math.inf or top_right_score == -math.inf:
                    return top_right_score

        # Bottom-left section
        bottom_left_score = -1
        if self.is_section_within_grid(row_index + 1, col_index - 1):
            if self.get_cell_state(row_index + 1, col_index - 1) != opponent_token:   
                bottom_left_score = self.get_section_score(player_token, opponent_token, row_index + 1, col_index - 1)
                if bottom_left_score == math.inf or bottom_left_score == -math.inf:
                    return bottom_left_score

        # Bottom-right section
        bottom_right_score = -1
        if self.is_section_within_grid(row_index + 1, col_index + 1):            
            if self.get_cell_state(row_index + 1, col_index + 1) != opponent_token:
                bottom_right_score = self.get_section_score(player_token, opponent_token, row_index + 1, col_index + 1)
                if bottom_right_score == math.inf or bottom_right_score == -math.inf:
                    return bottom_right_score

        return center_score + top_left_score + top_right_score + bottom_left_score + bottom_right_score
