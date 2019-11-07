from grid import Grid
from lightweight_grid import LightweightGrid
from player import Player
from ai_controller import AIController
import re
import sys
import math


class GameController:
    player_one = None
    player_two = None

    grid = None
    lightweight_grid = None

    is_player_one_turn = True
    number_of_tokens = None
    number_of_moves = None

    ai_controller = None
    play_with_AI = False

    def __init__(self, player_one, player_two, grid, lightweight_grid, number_of_tokens, number_of_moves):
        self.player_one = player_one
        self.player_two = player_two
        self.grid = grid
        self.lightweight_grid = lightweight_grid
        self.number_of_tokens = number_of_tokens
        self.number_of_moves = number_of_moves

    def welcome_message(self):
        print('====================================== Welcome to X-Rudder ======================================')
        print('Each player gets 15 tokens and is allowed 15 actions (placing a token or moving a token)')
        print('To place a token, enter the coordinate of an empty cell')
        print('To move a token, enter the coordinate of a cell containing an existing token followed\nby the coordinate to where the token should be moved')
        print('Disclaimer: you can only move your own token')
        print('=================================================================================================\n')

    def prompt_gamemode(self):
        is_input_valid = False
        while not is_input_valid:
            print("Gamemodes:\n")
            print("\t1- Player vs Player")
            print("\t2- Player vs AI")
            selected_gamemode = input(
                "\nPlease select gamemode option [1 or 2]: ")

            if selected_gamemode == "1":
                self.play_with_AI = False
                is_input_valid = True
                print("\nSelected Player vs Player\n")
            elif selected_gamemode == "2":
                self.play_with_AI = True
                is_input_valid = True
                self.ai_controller = AIController(
                    self.player_one, self.player_two)

                print("\nSelected Player vs AI\n")
            else:
                print("\nThat is not a valid gamemode option!\n")

    def exit_program(self, message):
        print("_____________________________________________________")
        print(message)
        print("_____________________________________________________\n")
        self.grid.display()
        sys.exit()

    def parse_input_coord(self, input_coords):
        input_coords = input_coords.upper()
        if input_coords == "QUIT" or input_coords == "Q":
            sys.exit()

        is_valid_input = re.match('[A-L]((10)|[1-9])$', input_coords)

        if is_valid_input is None:
            return None

        letter = input_coords[0]
        number = int(input_coords[1:])

        print("(" + letter + ", " + str(number) + ")\n")

        row_index = self.grid.height - number
        col_index = ord(letter) - 65

        input_coords = {}
        input_coords['col'] = col_index
        input_coords['row'] = row_index

        return input_coords

    def check_for_win(self, player_name, player_token, opponent_token, row_index, col_index):
        has_player_won = self.grid.check_for_x(
            player_token, opponent_token, row_index, col_index)
        if has_player_won:
            self.exit_program("\n" + player_name + " You win!")

    def win_status_check(self, player_name, player_token, opponent_token, row_index, col_index):
        # Center section
        self.check_for_win(player_name, player_token,
                           opponent_token, row_index, col_index)

        # Top-left section
        self.check_for_win(player_name, player_token,
                           opponent_token, row_index - 1, col_index - 1)

        # Top-right section
        self.check_for_win(player_name, player_token,
                           opponent_token, row_index - 1, col_index + 1)

        # Bottom-left section
        self.check_for_win(player_name, player_token,
                           opponent_token, row_index + 1, col_index - 1)

        # Bottom-right section
        self.check_for_win(player_name, player_token,
                           opponent_token, row_index + 1, col_index + 1)

    def play(self):
        self.welcome_message()
        self.prompt_gamemode()

        while True:
            current_player = self.player_one if self.is_player_one_turn else self.player_two
            current_opponent = self.player_two if self.is_player_one_turn else self.player_one
            
            if current_player is self.player_two and self.play_with_AI:
                is_move = False
                if(self.player_two.number_of_tokens <= 0):
                    is_move = True

                # Use minimax and alpha-beta pruning to find best action
                optimal_choice = self.ai_controller.minimax(self.lightweight_grid, 2, -math.inf, math.inf, True, is_move)
                
                self.grid.insert_coords(optimal_choice.x, optimal_choice.y, current_player.token)
                self.lightweight_grid.insert_coords(optimal_choice.x, optimal_choice.y, current_player.token)
                
                self.win_status_check(current_player.name, current_player.token, current_opponent.token, optimal_choice.x, optimal_choice.y)
                self.number_of_tokens -= 1
                current_player.number_of_tokens -= 1
            else:
                # Prompt player to place/move a token
                input_coords = None
                row_index = None
                col_index = None

                move_coords = None
                move_row_index = None
                move_col_index = None

                is_input_valid = False
                is_move_action = False

                while not is_input_valid:
                    self.grid.display()

                    player_input = input(
                        "\n" + current_player.name + ", please enter a letter [A-L] followed by a number [1-10] [or quit/q to quit]: ")
                    input_coords = self.parse_input_coord(player_input)

                    if input_coords is None:
                        print(
                            "Please enter a letter [A-L] followed by a number [1-10]\n")
                        continue

                    row_index = input_coords.get("row")
                    col_index = input_coords.get("col")

                    has_selected_occupied_cell = self.grid.is_occupied(
                        row_index, col_index)
                    if has_selected_occupied_cell:
                        cell_state = self.grid.get_cell_state(
                            row_index, col_index)
                        if cell_state is current_player.token:
                            is_move_action = True
                        else:
                            print("This cell is occupied\n")
                            continue
                    else:
                        if current_player.number_of_tokens == 0:
                            print(
                                "You have ran out of tokens to place. Please make a different move\n")
                            continue

                    is_input_valid = True

                if is_move_action:
                    is_input_valid = False
                    while not is_input_valid:
                        self.grid.display()

                        player_input = input(
                            "\n" + current_player.name + ", where would you like to move this token? [or quit/q to quit]: ")
                        move_coords = self.parse_input_coord(player_input)

                        if move_coords is None:
                            print(
                                "Please enter a letter [A-L] followed by a number [1-10]\n")
                            continue

                        move_row_index = move_coords.get("row")
                        move_col_index = move_coords.get("col")

                        # return true if move cell is adjacent to first inputted cell
                        is_valid_adjacent_cell = self.grid.is_valid_adjacent_cell(
                            row_index, col_index, move_row_index, move_col_index)
                        if not is_valid_adjacent_cell:
                            print("This is not a valid adjacent cell")
                            print(
                                "Please enter a cell that is up/down/left/right/diagonal to original cell\n")
                            continue

                        has_selected_occupied_cell = self.grid.is_occupied(
                            move_row_index, move_col_index)
                        if has_selected_occupied_cell:
                            print("This cell is occupied\n")
                            continue

                        is_input_valid = True

                if is_move_action:
                    self.grid.move_token(row_index, col_index, move_row_index, move_col_index)
                    self.lightweight_grid.move_token(row_index, col_index, move_row_index, move_col_index)
                    
                    # Checks if current player has won by moving a token to a new cell
                    self.win_status_check(current_player.name, current_player.token,
                                          current_opponent.token, move_row_index, move_col_index)

                    # Checks if opponent won by current player's move action
                    # col_index - 1 to check on the left side and col_inx + 1 to chec on the right side
                    self.win_status_check(
                        current_opponent.name, current_opponent.token, current_player.token, row_index, col_index - 1)
                    self.win_status_check(
                        current_opponent.name, current_opponent.token, current_player.token, row_index, col_index + 1)
                    self.number_of_moves -= 1
                else:
                    self.grid.insert_coords(row_index, col_index, current_player.token)
                    self.lightweight_grid.insert_coords(row_index, col_index, current_player.token)

                    self.win_status_check(
                        current_player.name, current_player.token, current_opponent.token, row_index, col_index)
                    self.number_of_tokens -= 1
                    current_player.number_of_tokens -= 1
            
            self.is_player_one_turn = not self.is_player_one_turn

            if self.number_of_tokens is 0 and self.number_of_moves <= 0:
                self.exit_program("You have reached a draw")
