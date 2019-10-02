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

class Cell:
    state = " "

    def insert_token(self, token):
        self.state = token

    def clear(self):
        self.state = " "

    def is_empty(self):
        return self.state is " "