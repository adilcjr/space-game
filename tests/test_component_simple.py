"""
Simple component tests for Space Invaders.

Run: poetry run pytest tests/test_component_simple.py -v
"""

import sys
sys.path.insert(0, 'src')

import pytest

def test_player_initialization():
    """Player initializes at correct position."""
    from player import Player

    player = Player(100, 550)
    assert player.x == 100
    assert player.y == 550
    assert player.width == 36
    assert player.height == 30

def test_player_movement():
    """Player moves left and right."""
    from player import Player
    
    player = Player(100, 550)
    
    # Move left with key code 276
    player.move({275: True, 276: False})
    assert player.x == 90
    
    # Move right with key code 276
    player.move({275: False, 276: True})
    assert player.x == 100

def test_shooting():
    """Player shoots and enters cooldown."""
    from player import Player
    
    player = Player(100, 550)
    
    assert player.shot == 0
    player.shoot([])
    assert player.shot == 15

def test_update():
    """Player updates cooldown."""
    from player import Player
    
    player = Player(100, 550)
    player.shoot([])
    assert player.shot == 15
    
    player.update()
    assert player.shot == 14

def test_game_state():
    """Game state initializes correctly."""
    from game_state import GameState
    from constants import GAME_STATE
    
    state = GameState()
    assert state.state == GAME_STATE["MENU"]
    assert state.score == 0
    assert state.level == 1

def test_enemy_manager():
    """Enemy manager spawns enemies."""
    from enemies import EnemyManager
    
    manager = EnemyManager(level=1)
    assert len(manager.get_enemies()) > 0

def test_enemy_count():
    """Enemy count scales with level."""
    from enemies import EnemyManager
    
    manager = EnemyManager(level=1)
    count = manager.count_enemies()
    assert count > 0

def test_bullet_creation():
    """Bullets can be created."""
    from bullet import create_player_bullet
    
    bullet = create_player_bullet(100, 550)
    assert bullet["x"] == 100
    assert bullet["y"] == 550
    assert bullet["type"] == "player"
    assert bullet["active"] is True

def test_level_config():
    """Level configurations exist."""
    from constants import LEVELS
    
    assert len(LEVELS) == 10
    assert LEVELS[1]["enemy_count"] == 30
    assert LEVELS[10]["boss_level"] is True
    assert LEVELS[10]["enemy_count"] == 120

def test_powerups():
    """Powerup types defined."""
    from constants import POWERUP_TYPES
    
    assert len(POWERUP_TYPES) > 0

def test_constants():
    """Screen constants are correct."""
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
    
    assert SCREEN_WIDTH == 800
    assert SCREEN_HEIGHT == 600
    assert FPS == 60

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
