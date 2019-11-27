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
    is_first_ai_placement = False

    def __init__(self, player_one, player_two, grid, lightweight_grid, number_of_tokens, number_of_moves):
        self.player_one = player_one
        self.player_two = player_two
        self.grid = grid
        self.lightweight_grid = lightweight_grid
        self.number_of_tokens = number_of_tokens
        self.number_of_moves = number_of_moves

    def welcome_message(self):
        print("====================================== Welcome to X-Rudder ======================================\n")    

    def prompt_gamemode(self):
        is_input_valid = False
        while not is_input_valid:
            print("Gamemodes:\n")
            print("\t1- Player vs Player")
            print("\t2- Player vs AI")
            selected_gamemode = input("\nPlease select gamemode option [1 or 2]: ")

            if selected_gamemode == "1":
                self.play_with_AI = False
                is_input_valid = True
                print("\n\tSelected Player vs Player\n")
            elif selected_gamemode == "2":
                self.play_with_AI = True
                is_input_valid = True
                self.is_first_ai_placement = True
                print("\n\tSelected Player vs AI\n")
            else:
                print("\n\tThat is not a valid gamemode option!\n")

    def prompt_token(self, player, opponent):
        is_input_valid = False
        while not is_input_valid:
            selected_token = input(player.name + ", please enter a character for your token: ")
            
            if selected_token == opponent.token:
                print("\tPlease enter a different token!")
                continue

            player.token = selected_token
            is_input_valid = True

    def prompt_player_order(self):
        is_input_valid = False
        while not is_input_valid:
            print("Players:\n")
            print("\t1- Player")
            print("\t2- AI")
            
            selected_player = input("\nWho should play first? [1 or 2]: ")
            if selected_player == "1":
                self.player_one.name = "Player"
                self.player_two.name = "AI"
                self.player_two.is_ai = True
                is_input_valid = True
                print("\n\tPlayer will play first!")
            elif selected_player == "2":
                self.player_two.name = "Player"
                self.player_one.name = "AI"
                self.player_one.is_ai = True
                is_input_valid = True
                print("\n\tAI will play first!")
            else:
                print("\n\tThat is not a valid player option!\n")
                
        self.ai_controller = AIController(self.player_one, self.player_two, self.number_of_moves)
    
    def exit_program(self, message):
        print("_____________________________________________________")
        print("\t" + message)
        print("_____________________________________________________\n")
        self.grid.display()
        sys.exit()

    def parse_input_coord(self, input_coords, player_token):
        input_coords = input_coords.upper()
        if input_coords == "QUIT" or input_coords == "Q":
            sys.exit()

        output = {}
        coords_array = input_coords.split(" ")
        output["is_move"] = True if len(coords_array) > 1 else False

        is_valid_input = re.match('[A-L]((10)|[1-9])$', coords_array[0])

        if is_valid_input is None:
            print("\tPlease enter a letter [A-L] followed by a number [1-10]\n")
            return None

        letter = coords_array[0][0]
        number = int(coords_array[0][1:])

        row_index = self.grid.height - number
        col_index = ord(letter) - 65

        has_selected_occupied_cell = self.grid.is_occupied(row_index, col_index)
        if not output["is_move"]:
            # Prevent the player from placing a token on an occupied cell
            if has_selected_occupied_cell:
                print("\tCell (" + letter + ", " + str(number) + ") is occupied\n")
                return None
        else:
            # Prevent the player from moving an empty cell
            if not has_selected_occupied_cell:
                print("\tCell (" + letter + ", " + str(number) + ") is empty")
                print("\tPlease select an cell with your token\n")
                return None
            
            # Prevent the player from moving the opponent's token
            cell_state = self.grid.get_cell_state(row_index, col_index)
            if cell_state is not player_token:
                print("\tCell (" + letter + ", " + str(number) + ") does not contain your token")
                print("\tPlease select an cell with your token\n")
                return None

        output['col'] = col_index
        output['row'] = row_index

        if output["is_move"]:
            is_valid_input = re.match('[A-L]((10)|[1-9])$', coords_array[1])

            if is_valid_input is None:
                print("\tPlease enter a letter [A-L] followed by a number [1-10]\n")
                return None

            letter = coords_array[1][0]
            number = int(coords_array[1][1:])

            move_row_index = self.grid.height - number
            move_col_index = ord(letter) - 65

            # return true if move cell is adjacent to first inputted cell
            is_valid_adjacent_cell = self.grid.is_valid_adjacent_cell(row_index, col_index, move_row_index, move_col_index)
            if not is_valid_adjacent_cell:
                print("\tCell (" + letter + ", " + str(number) + ") is not a valid adjacent cell")
                print("\tPlease enter a cell that is up/down/left/right/diagonal to original cell\n")
                return None

            has_selected_occupied_cell = self.grid.is_occupied(move_row_index, move_col_index)
            if has_selected_occupied_cell:
                print("\tCell (" + letter + ", " + str(number) + ") is occupied\n")
                return None

            output['move_col'] = move_col_index
            output['move_row'] = move_row_index

        return output
    
    def format_coordinate(self, x, y):
        letter = chr(y + 65)
        number = x
        return "(" + letter + ", " + str(number) + ")"

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

        self.prompt_token(self.player_one, self.player_two)
        self.prompt_token(self.player_two, self.player_one)

        if self.play_with_AI:
            self.prompt_player_order()

        print("\n\t" + self.player_one.name + " is " + self.player_one.token)
        print("\t" + self.player_two.name + " is " + self.player_two.token + "\n")

        while True:
            current_player = self.player_one if self.is_player_one_turn else self.player_two
            current_opponent = self.player_two if self.is_player_one_turn else self.player_one
            
            if current_player.is_ai and self.play_with_AI:
                optimal_choice = None
                if self.is_first_ai_placement:
                    optimal_choice = self.ai_controller.random_optimal_choice(self.lightweight_grid, 0)
                    self.is_first_ai_placement = False
                else:
                    # Use minimax and alpha-beta pruning to find best action
                    optimal_choice = self.ai_controller.minimax(self.lightweight_grid, 2, -math.inf, math.inf, True)

                if optimal_choice.to_x == -1 and optimal_choice.to_y == -1 and not current_player.number_of_tokens == 0:
                    if optimal_choice.from_y == -1:
                        optimal_choice = self.ai_controller.random_optimal_choice(self.lightweight_grid, 0)
                    
                    # Do placement
                    self.grid.insert_coords(optimal_choice.from_x, optimal_choice.from_y, current_player.token)
                    self.lightweight_grid.insert_coords(optimal_choice.from_x, optimal_choice.from_y, current_player.token)
                    
                    print("\t" + current_player.name + " placed a token at: " + self.format_coordinate(10 - optimal_choice.from_x , optimal_choice.from_y) + "\n")
                    
                    self.win_status_check(current_player.name, current_player.token, current_opponent.token, optimal_choice.from_x, optimal_choice.from_y)
                    self.number_of_tokens -= 1
                    current_player.number_of_tokens -= 1
                else:
                    if optimal_choice.from_y == -1:
                        optimal_choice = self.ai_controller.get_random_move(self.lightweight_grid, current_player.token, self.number_of_tokens//2 - current_player.number_of_tokens)
                    # Do move
                    self.grid.move_token(optimal_choice.from_x, optimal_choice.from_y, optimal_choice.to_x, optimal_choice.to_y)
                    self.lightweight_grid.move_token(optimal_choice.from_x, optimal_choice.from_y, optimal_choice.to_x, optimal_choice.to_y)
                    
                    print("\t" + current_player.name + " moved a token from " + self.format_coordinate(10 - optimal_choice.from_x, optimal_choice.from_y) + " to " + self.format_coordinate(10 - optimal_choice.to_x, optimal_choice.to_y) + "\n")
                    # Checks if current player has won by moving a token to a new cell
                    self.win_status_check(current_player.name, current_player.token, current_opponent.token, optimal_choice.to_x, optimal_choice.to_y)

                    # Checks if opponent won by current player's move action
                    self.win_status_check(current_opponent.name, current_opponent.token, current_player.token, optimal_choice.from_x, optimal_choice.from_y - 1)
                    self.win_status_check(current_opponent.name, current_opponent.token, current_player.token, optimal_choice.from_x, optimal_choice.from_y + 1)
                    self.number_of_moves -= 1
                
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

                    player_input = input("\n" + current_player.name + "'s turn [quit/q to quit]: ")
                    print()
                    input_coords = self.parse_input_coord(player_input, current_player.token)

                    if input_coords is None:
                        continue
                    
                    if not input_coords.get("is_move") and current_player.number_of_tokens == 0:
                        is_move_action = False
                        print("You have ran out of tokens to place. Please make a different move\n")
                        continue
                    elif input_coords.get("is_move"):
                        is_move_action = True
                        row_index = input_coords.get("row")
                        col_index = input_coords.get("col")
                        move_row_index = input_coords.get("move_row")
                        move_col_index = input_coords.get("move_col")
                    else:
                        is_move_action = False
                        row_index = input_coords.get("row")
                        col_index = input_coords.get("col")

                    is_input_valid = True

                if is_move_action:
                    self.grid.move_token(row_index, col_index, move_row_index, move_col_index)
                    self.lightweight_grid.move_token(row_index, col_index, move_row_index, move_col_index)

                    print("\t" + current_player.name + " moved a token from " + self.format_coordinate(10 - row_index, col_index) + " to " + self.format_coordinate(10 - move_row_index, move_col_index) + "\n")

                    # Checks if current player has won by moving a token to a new cell
                    self.win_status_check(current_player.name, current_player.token, current_opponent.token, move_row_index, move_col_index)

                    # Checks if opponent won by current player's move action
                    self.win_status_check(current_opponent.name, current_opponent.token, current_player.token, row_index, col_index - 1)
                    self.win_status_check(current_opponent.name, current_opponent.token, current_player.token, row_index, col_index + 1)
                    self.number_of_moves -= 1
                else:
                    self.grid.insert_coords(row_index, col_index, current_player.token)
                    self.lightweight_grid.insert_coords(row_index, col_index, current_player.token)

                    print("\t" + current_player.name + " placed a token at: " + self.format_coordinate(10 - row_index, col_index) + "\n")

                    self.win_status_check(current_player.name, current_player.token, current_opponent.token, row_index, col_index)
                    self.number_of_tokens -= 1
                    current_player.number_of_tokens -= 1
            
            self.is_player_one_turn = not self.is_player_one_turn

            if self.number_of_tokens is 0 and self.number_of_moves <= 0:
                self.exit_program("You have reached a draw")
