#!/usr/bin/env python3
"""Run the Space Invaders game."""

import os
import sys
import pygame

# Set up paths to import from src
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(base_dir, "src"))

from game import Game


def main():
    pygame.init()
    print("Starting Space Invaders - Retro Arcade Game")
    print("Controls: LEFT/RIGHT to move, SPACE to shoot")
    print("Press ESC to pause, SPACE to start game")

    game = Game()
    game.run()

    pygame.quit()
    print("Game ended.")


if __name__ == "__main__":
    main()
