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
        return cell.is_empty()

    def get_cell_state(self, row_index, col_index):
        cell = self.grid_cells[row_index][col_index]
        return cell.state

    def move_token(self, from_row, from_col, to_row, to_col):
        from_cell = self.grid_cells[from_row][from_col]
        to_cell = self.grid_cells[to_row][to_col]

        to_cell.state = from_cell.state
        from_cell.clear()

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

class Cell:
    state = " "

    def insert_token(self, token):
        self.state = token

    def clear(self):
        self.state = " "

    def is_empty(self):
        return self.state is " "