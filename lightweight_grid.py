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

    def get_all_adjacent_cells(self, row_index, col_index):
        adjacent_cells = []

        # Top left
        if self.is_section_within_grid(row_index - 1, col_index - 1):
            if not self.is_occupied(row_index - 1, col_index - 1):
                adjacent_cells.append([row_index - 1,  col_index - 1])

        # Top center
        if self.is_section_within_grid(row_index - 1, col_index):
            if not self.is_occupied(row_index - 1, col_index):
                adjacent_cells.append([row_index - 1,  col_index])        
        
        # Top right
        if self.is_section_within_grid(row_index - 1, col_index + 1):
            if not self.is_occupied(row_index - 1, col_index + 1):
                adjacent_cells.append([row_index - 1,  col_index + 1])

        # left cell
        if self.is_section_within_grid(row_index, col_index - 1):
            if not self.is_occupied(row_index, col_index - 1):
                adjacent_cells.append([row_index ,  col_index - 1])

        # right
        if self.is_section_within_grid(row_index, col_index + 1):
            if not self.is_occupied(row_index, col_index + 1):
                adjacent_cells.append([row_index,  col_index + 1])

        # bottom left
        if self.is_section_within_grid(row_index + 1, col_index - 1):
            if not self.is_occupied(row_index + 1, col_index - 1):
                adjacent_cells.append([row_index + 1,  col_index - 1])

        # bottom center
        if self.is_section_within_grid(row_index, col_index):
            if not self.is_occupied(row_index, col_index):
                adjacent_cells.append([row_index ,  col_index])
                
        # Bottom right
        if self.is_section_within_grid(row_index + 1, col_index + 1):
            if not self.is_occupied(row_index + 1, col_index + 1):
                adjacent_cells.append([row_index + 1,  col_index + 1])
            
        return adjacent_cells

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

    def get_num_tokens_in_pattern(self, token, row_index, col_index):
        num_tokens = 0
        
        top_left_cell_state = self.grid_cells[row_index - 1][col_index - 1]
        top_right_cell_state = self.grid_cells[row_index - 1][col_index + 1]
        center_cell_state = self.grid_cells[row_index][col_index]
        bottom_left_cell_state = self.grid_cells[row_index + 1][col_index - 1]
        bottom_right_cell_state = self.grid_cells[row_index + 1][col_index + 1]

        cell_states = [center_cell_state, top_left_cell_state, top_right_cell_state, bottom_left_cell_state, bottom_right_cell_state]
        
        for state in cell_states:
            num_tokens += 1 if state == token else 0

        return num_tokens

    def get_num_edge_tokens_in_pattern(self, token, row_index, col_index):
        num_edge_tokens = 0
        if self.grid_cells[row_index][col_index - 1] == token:
            num_edge_tokens += 1
        if self.grid_cells[row_index][col_index + 1] == token:
            num_edge_tokens += 1
        return num_edge_tokens

    def get_section_score(self, player_token, opponent_token, row_index, col_index):
        section_score = 0
        
        if self.is_section_within_grid(row_index, col_index):
            num_player_tokens =  self.get_num_tokens_in_pattern(player_token, row_index, col_index)
            num_opponent_edge_tokens = self.get_num_edge_tokens_in_pattern(opponent_token, row_index, col_index)
            
            if num_player_tokens == 5:
                if not num_opponent_edge_tokens == 2:
                    return math.inf
                elif num_opponent_edge_tokens == 2:
                    return 0
            else:
                if num_opponent_edge_tokens == 2:
                    section_score += -5
                else: 
                    num_opponent_tokens = self.get_num_tokens_in_pattern(opponent_token, row_index, col_index)
                    if num_player_tokens + num_opponent_tokens == 5:
                        return 0
                    
                    num_opponent_tokens += num_opponent_edge_tokens
                    section_score += math.factorial(num_player_tokens) - math.factorial(num_opponent_tokens) 
        else:
            section_score = -1 

        return section_score

    def get_block_score(self, player_token, opponent_token, row_index, col_index):
        if self.is_section_within_grid(row_index, col_index):
            num_player_tokens = self.get_num_tokens_in_pattern(player_token, row_index, col_index)
            num_opponent_tokens = self.get_num_tokens_in_pattern(opponent_token, row_index, col_index)

            is_pattern_blocked = True if num_player_tokens + num_opponent_tokens == 5 else False            
            if not is_pattern_blocked:
                if num_opponent_tokens >= 4:
                    print("I blocked at row: " + str(row_index) + " - col: " + str(col_index))
                    return math.inf
                else:
                    return 0
        return 0

    def get_cell_score(self, player_token, opponent_token, row_index, col_index):
        total_cell_score = 0
        
        # Checking for win/loss

        # Check center 
        total_cell_score += self.get_section_score(player_token, opponent_token, row_index, col_index)

        # Check top left 
        total_cell_score += self.get_section_score(player_token, opponent_token, row_index - 1, col_index - 1)

        # Check top right 
        total_cell_score += self.get_section_score(player_token, opponent_token, row_index -1 , col_index + 1)

        # Check bottom left 
        total_cell_score += self.get_section_score(player_token, opponent_token, row_index + 1, col_index - 1)

        # Check bottom right 
        total_cell_score += self.get_section_score(player_token, opponent_token, row_index + 1, col_index + 1)

        # Checking for crossed out
        # Check right case
        if col_index + 2 < self.width and row_index != 0 and row_index != self.height - 1:
            if self.is_section_within_grid(row_index, col_index + 1):
                num_player_tokens = self.get_num_tokens_in_pattern(player_token, row_index, col_index + 1)
                num_opponent_tokens = self.get_num_tokens_in_pattern(opponent_token, row_index, col_index + 1)
                
                # is_pattern_blocked = False
                # if num_player_tokens > 0 and num_opponent_tokens > 0:
                #     is_pattern_blocked = True if num_player_tokens + num_opponent_tokens == 5 else False
                
                is_pattern_blocked = True if num_player_tokens + num_opponent_tokens == 5 else False

                if not is_pattern_blocked:          
                    other_edge_cell_state = self.get_cell_state(row_index, col_index + 2)
                    if num_opponent_tokens == 5:
                        # Always return infinity if opponent has 5 tokens
                        total_cell_score += math.inf
                    # elif other_edge_cell_state == opponent_token:
                    #     total_cell_score -= 35 * num_opponent_tokens
                    elif num_opponent_tokens >= 4 and not other_edge_cell_state == opponent_token:
                        # print("inside >= 4 Right case, row: " + str(row_index) + "- col: " + str(col_index))
                        total_cell_score += 35 * num_opponent_tokens

        # Check left case
        if col_index - 2 >= 0 and row_index != 0 and row_index != self.height - 1:
            if self.is_section_within_grid(row_index, col_index - 1):
                num_player_tokens = self.get_num_tokens_in_pattern(player_token, row_index, col_index - 1)
                num_opponent_tokens = self.get_num_tokens_in_pattern(opponent_token, row_index, col_index - 1)
                
                # is_pattern_blocked = False
                # if num_player_tokens > 0 and num_opponent_tokens > 0:
                #     is_pattern_blocked = True if num_player_tokens + num_opponent_tokens == 5 else False
                
                is_pattern_blocked = True if num_player_tokens + num_opponent_tokens == 5 else False
                if not is_pattern_blocked:          
                    other_edge_cell_state = self.get_cell_state(row_index, col_index - 2)
                    if num_opponent_tokens == 5:
                        # Always return infinity if opponent has 5 tokens
                        total_cell_score += math.inf
                    # elif other_edge_cell_state == opponent_token:
                    #     total_cell_score -= 35 * num_opponent_tokens
                    elif num_opponent_tokens >= 4 and not other_edge_cell_state == opponent_token:
                        # print("inside >= 4 Left case, row: " + str(row_index) + "- col: " + str(col_index))
                        total_cell_score += 35 * num_opponent_tokens

        # Check for block score
        # Center
        total_cell_score += self.get_block_score(player_token, opponent_token, row_index, col_index)
        
        # Top left
        total_cell_score += self.get_block_score(player_token, opponent_token, row_index - 1,  col_index - 1)
        
        # Top right
        total_cell_score += self.get_block_score(player_token, opponent_token, row_index - 1, col_index + 1)
        
        # Bottom left
        total_cell_score += self.get_block_score(player_token, opponent_token, row_index + 1, col_index - 1)
        
        # Bottom right
        total_cell_score += self.get_block_score(player_token, opponent_token, row_index + 1, col_index + 1)

        return total_cell_score
