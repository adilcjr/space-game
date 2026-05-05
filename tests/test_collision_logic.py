import pytest
import pygame
import constants
from unittest.mock import MagicMock, patch
from src.game import Game
from src.player import Player
from src.game_state import GameState
from src.bullet import BulletManager


@pytest.fixture
def mock_pygame_module():
    # Mock necessary pygame components for isolated testing
    pygame.display.set_mode = MagicMock()
    pygame.font.Font = MagicMock()
    pygame.time.Clock = MagicMock()

    # Mocking constants needed for setup verification (assuming these are correct)
    # In a real scenario, we might need to mock the constants module itself.


@pytest.fixture
def game_instance(mock_pygame_module):
    # Setup fixture providing a fresh game instance for each test
    game = Game()
    # Initialize necessary components/mocks if they are not correctly initialized by Game.__init__
    game.game_state = GameState()
    game.player = Player(100, 100)
    game.bullet_manager = BulletManager()

    # Mock enemy manager and enemies to control scene state
    mock_enemy_manager = MagicMock()
    # Provide a mock count_enemies method
    mock_enemy_manager.count_enemies.return_value = 1
    game.enemy_manager = mock_enemy_manager

    return game


def test_player_bullet_hits_one_enemy(game_instance, mock_pygame_module):
    # Arrange: Setup scenario for single hit

    # 1. Create a mock enemy that is hit
    mock_enemy_manager = game_instance.enemy_manager
    mock_enemy = {"active": True, "x": 10, "width": 50, "y": 50, "height": 30}
    mock_enemy_manager.enemies = [mock_enemy]

    # 2. Create a player bullet that intersects the mock enemy
    player_bullet = {
        "x": 15,
        "y": 55,
        "width": 4,
        "height": 10,
        "type": "player",
        "active": True,
    }
    game_instance.bullet_manager.bullets = [player_bullet]

    # 3. Execute the function under test
    game_instance._check_collisions()

    # Assertions
    assert not mock_enemy["active"]  # Enemy should be deactivated
    assert not player_bullet["active"]  # Bullet should be deactivated
    assert game_instance.game_state.score == 10  # Score should increase


def test_player_bullet_hits_multiple_enemies(game_instance, mock_pygame_module):
    # Arrange: Setup scenario for multiple potential hits (testing the 'break' logic)

    # 1. Create two enemies: one hit, one missed (to test breaking)
    mock_enemy_manager = game_instance.enemy_manager
    mock_enemy_manager.enemies = [
        {"active": True, "x": 10, "width": 50, "y": 50, "height": 30},  # Hit Target
        {"active": True, "x": 200, "width": 50, "y": 50, "height": 30},  # Miss Target
    ]

    # 2. Create a bullet that clearly hits the first enemy
    player_bullet = {
        "x": 15,
        "y": 55,
        "width": 4,
        "height": 10,
        "type": "player",
        "active": True,
    }
    game_instance.bullet_manager.bullets = [player_bullet]

    # 3. Execute the function under test
    game_instance._check_collisions()

    # Assertions: Only the first enemy should be hit, and the bullet should be deactivated.
    assert not mock_enemy_manager.enemies[0]["active"]
    assert mock_enemy_manager.enemies[1]["active"]  # Second enemy remains active
    assert not player_bullet["active"]  # Bullet deactivated
    assert game_instance.game_state.score == 10  # Score increased only once


def test_player_bullet_misses_all_enemies(game_instance, mock_pygame_module):
    # Arrange: Setup scenario where the bullet misses entirely
    mock_enemy_manager = game_instance.enemy_manager
    mock_enemy_manager.enemies = [
        {"active": True, "x": 200, "width": 50, "y": 50, "height": 30}
    ]  # Enemy is far to the right

    # Bullet spawns far to the left
    player_bullet = {
        "x": 10,
        "y": 55,
        "width": 4,
        "height": 10,
        "type": "player",
        "active": True,
    }
    game_instance.bullet_manager.bullets = [player_bullet]

    # Execute the function under test
    game_instance._check_collisions()

    # Assertions: No state should change
    for enemy in mock_enemy_manager.enemies:
        assert enemy["active"] == True
    assert player_bullet["active"] == True
    assert game_instance.game_state.score == 0


# Note: Enemy/Player collision testing would require similar fixtures for those entities.
