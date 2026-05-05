"""Space Invaders-style Game - Entry point"""

import pygame
from game import Game
import constants

# Constants for quick reference
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT
FPS = constants.FPS


def main():
    """
    Main entry point for the game.

    Setup pygame, initialize game, run main loop, then clean up.
    """
    pygame.init()

    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders - Retro Arcade Game")

    # Create and run game
    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
