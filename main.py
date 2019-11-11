from grid import Grid
from game_controller import GameController
from player import Player
from lightweight_grid import LightweightGrid


def main():
    width = 12
    height = 10

    total_number_of_tokens = 30
    total_number_of_moves = 30

    player_one = Player("Player 1", "X", total_number_of_tokens//2)
    player_two = Player("Player 2", "O", total_number_of_tokens//2)

    grid = Grid(width, height)
    lightweight_grid = LightweightGrid(width, height)

    game_controller = GameController(player_one, player_two, grid, lightweight_grid, total_number_of_tokens, total_number_of_moves)
    game_controller.play()


if __name__ == "__main__":
    main()
