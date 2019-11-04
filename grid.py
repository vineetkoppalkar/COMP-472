import math

class Grid:
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
                gridline.append(Cell())
            grid.append(gridline)

        return grid

    def display(self):
        for i in range(self.height):
            # Adding the row numbers from 1 to 10
            print(str(self.height - i).ljust(3), end = '')
            for j in range(self.width):
                # Printing the states of the cells in the grid
                cell = self.grid_cells[i][j]
                print("[" + cell.state + "] ", end = '')
            print()

        # Adding the column letters at the bottom from A to L
        print(" ".ljust(4), end = '')
        for i in range(self.width):
            print(chr(65 + i).ljust(4), end = '')
        print()

    def insert_coords(self, row_index, col_index, token_type):
        cell = self.grid_cells[row_index][col_index]
        if cell.is_empty():
            cell.state = token_type
            return True
        else:
            return False


    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.grid_cells[i][j]
                cell.clear()

    def is_occupied(self, row_index, col_index):
        cell = self.grid_cells[row_index][col_index]
        return not cell.is_empty()

    def get_cell_state(self, row_index, col_index):
        cell = self.grid_cells[row_index][col_index]
        return cell.state

    def move_token(self, from_row, from_col, to_row, to_col):
        from_cell = self.grid_cells[from_row][from_col]
        to_cell = self.grid_cells[to_row][to_col]

        to_cell.state = from_cell.state
        from_cell.clear()

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
        # Check edge cases
        if row_index - 1 < 0 or row_index + 1 >= self.height:
            return False
        if col_index - 1 < 0 or col_index + 1 >= self.width:
            return False

        # If cell is empty, then don't bother continuing to check for X
        center_cell = self.grid_cells[row_index][col_index]
        if center_cell.is_empty():
            return False

        # Check if crossed out
        right_cell_state = self.grid_cells[row_index][col_index - 1].state
        left_cell_state = self.grid_cells[row_index][col_index + 1].state
        if right_cell_state is opponent_token and left_cell_state is opponent_token:
            return False

        # Check if win condition
        top_left_cell_state = self.grid_cells[row_index - 1][col_index - 1].state
        top_right_cell_state = self.grid_cells[row_index - 1][col_index + 1].state
        center_cell_state = center_cell.state
        bottom_left_cell_state = self.grid_cells[row_index + 1][col_index - 1].state
        bottom_right_cell_state = self.grid_cells[row_index + 1][col_index + 1].state

        cell_states = [center_cell_state, top_left_cell_state, top_right_cell_state, bottom_left_cell_state, bottom_right_cell_state]

        return all(state == player_token for state in cell_states)
    
    def get_section_score(self, player_token, opponent_token, row_index, col_index):
        # Ensure that row and col in within grid
        # if not ((row_index >= 0 and row_index < self.height) and (col_index >= 0 and col_index < self.width)):
        #     return 0

        total_score = 0
        
        # Center
        center_cell_state = self.grid_cells[row_index][col_index].state
        if center_cell_state == player_token:
            total_score += 5
        elif center_cell_state == opponent_token:
            return 0
        
        # Top-left
        if col_index - 1 >= 0 and row_index - 1 >= 0:
            top_left_cell_state = self.grid_cells[row_index - 1][col_index - 1].state
            has_top_left = True if top_left_cell_state == player_token else False
            total_score += 5 if has_top_left else 0

        # Top-right
        if col_index + 1 < self.width and row_index - 1 >= 0:
            top_right_cell_state = self.grid_cells[row_index - 1][col_index + 1].state
            has_top_right = True if top_right_cell_state == player_token else False
            total_score += 5 if has_top_right else 0 

        # Bottom-left
        if col_index - 1 >= 0 and row_index + 1 < self.height:
            bottom_left_cell_state = self.grid_cells[row_index + 1][col_index - 1].state
            has_bottom_left = True if bottom_left_cell_state == player_token else False
            total_score += 5 if has_bottom_left else 0

        # Bottom-right
        if col_index + 1 < self.width and row_index + 1 < self.height:
            bottom_right_cell_state = self.grid_cells[row_index + 1][col_index + 1].state
            has_bottom_right = True if bottom_right_cell_state == player_token else False
            total_score += 5 if has_bottom_right else 0

        has_won = False
        # If player has a X
        if total_score == 25:
            has_won = True
            total_score = math.inf

        # Check if crossed out
        is_left_state_occupied = False
        if col_index - 1 >= 0:
            left_cell_state = self.grid_cells[row_index][col_index - 1].state
            is_left_state_occupied = True if left_cell_state == opponent_token else False

        is_right_state_occupied = False
        if col_index + 1 < self.width:
            right_cell_state = self.grid_cells[row_index][col_index + 1].state
            is_right_state_occupied = True if right_cell_state == opponent_token else False

        is_crossed_out = is_left_state_occupied and is_right_state_occupied
        if has_won and is_crossed_out:
            return -math.inf
        
        return total_score


    def get_score(self, player_token, opponent_token, row_index, col_index):
        # Center section
        center_score = self.get_section_score(player_token, opponent_token, row_index, col_index)
        if center_score == math.inf:
            return center_score
        elif center_score == -math.inf:
            return center_score

        # Top-left section
        if row_index - 1 >= 0 and col_index - 1 >= 0:
            top_left_score = self.get_section_score(player_token, opponent_token, row_index - 1, col_index - 1)
            if top_left_score == math.inf:
                return top_left_score
            elif top_left_score == -math.inf:
                return top_left_score
            
        # Top-right section
        if row_index - 1 >= 0 and col_index + 1 < self.width:
            top_right_score = self.get_section_score(player_token, opponent_token, row_index - 1, col_index + 1)
            if top_right_score == math.inf:
                return top_right_score
            elif top_right_score == -math.inf:
                return top_right_score

        # Bottom-left section
        if row_index + 1 < self.height and col_index - 1 >= 0:
            bottom_left_score = self.get_section_score(player_token, opponent_token, row_index + 1, col_index - 1)
            if bottom_left_score == math.inf:
                return bottom_left_score
            elif bottom_left_score == -math.inf:
                return bottom_left_score

        # Bottom-right section
        if row_index + 1 < self.height and col_index + 1 < self.width:
            bottom_right_score = self.get_section_score(player_token, opponent_token, row_index + 1, col_index + 1)
            if bottom_right_score == math.inf:
                return bottom_right_score
            elif bottom_right_score == -math.inf:
                return bottom_right_score

        return center_score
                

class Cell:
    state = " "

    def insert_token(self, token):
        self.state = token

    def clear(self):
        self.state = " "

    def is_empty(self):
        return self.state is " "
