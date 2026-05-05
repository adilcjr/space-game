"""
Basic tests for Space Invaders game components.
Run: poetry run python test_basic.py
"""

import sys

sys.path.insert(0, "src")

from player import Player
from constants import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    PLAYER_SHOOT_COOLDOWN,
)


def test_player_creation():
    print("✓ Test: Player creation")
    player = Player(100, 550)
    assert player.x == 100
    assert player.y == 550
    assert player.width == PLAYER_WIDTH
    assert player.height == PLAYER_HEIGHT
    print(f"  Created player at ({player.x}, {player.y})")


def test_player_update():
    print("✓ Test: Player update")
    player = Player(100, 550)
    player.update()
    player.shoot([])
    assert player.shot == PLAYER_SHOOT_COOLDOWN
    print(f"  After shoot, cooldown is {player.shot} frames")


def test_player_movement():
    print("✓ Test: Player movement")
    # Create a simple key dict
    keys = {pygame.K_LEFT: True, pygame.K_RIGHT: False}
    player = Player(100, 550)
    player.move(keys)
    assert player.x == 90
    print(f"  Moved left from 100 to {player.x}")
    keys = {pygame.K_LEFT: False, pygame.K_RIGHT: True}
    player.move(keys)
    assert player.x == 100
    print(f"  Moved right back to {player.x}")


def test_constants():
    print("✓ Test: Constants")
    assert PLAYER_WIDTH == 36
    assert SCREEN_WIDTH == 800
    assert FPS == 60
    print(f"  SCREEN_WIDTH={SCREEN_WIDTH}, FPS={FPS}")


if __name__ == "__main__":
    import pygame

    pygame.init()

    print("\n=== Space Invaders Basic Tests ===\n")
    test_player_creation()
    test_player_update()
    test_player_movement()
    test_constants()

    print("\n✓ All basic tests passed!")
