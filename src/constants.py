"""
Game constants for Space Invaders-style game.

This module defines all game-wide constants for easy configuration and
maintainable code.
"""

# ============================================================================
# SCREEN CONSTANTS
# ============================================================================
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
FPS: int = 60
TARGET_FPS: int = 60

# ============================================================================
# PLAYER CONSTANTS
# ============================================================================
PLAYER_WIDTH: int = 36
PLAYER_HEIGHT: int = 30
PLAYER_SPEED: float = 10  # pixels per frame
PLAYER_SHOOT_COOLDOWN: int = 15  # frames between shots
PLAYER_BULLET_SPEED: float = 10
PLAYER_BULLET_HEIGHT: int = 4

# ============================================================================
# ENEMY CONSTANTS
# ============================================================================
ENEMY_ROWS: int = 4
ENEMY_COLS: int = 11
ENEMY_WIDTH: int = 36
ENEMY_HEIGHT: int = 30
ENEMY_BASE_SPEED: float = 1.0  # Starts at this, scales linearly
ENEMY_MAX_SPEED: float = 3.5
ENEMY_DROP_DISTANCE: int = 25
ENEMY_SHOOT_CHANCE: float = 0.01  # 1% per frame

# ============================================================================
# ENEMY COUNT PER LEVEL (Linear scaling)
# ============================================================================
BASE_ENEMY_COUNT: int = 30  # Level 1
ENEMIES_PER_LEVEL_INCREMENT: int = 10  # Add 10 enemies per level

# ============================================================================
# POWERUP TYPES
# ============================================================================
POWERUP_TYPES = [
    {"name": "SPREAD_SHOT", "emoji": "⭐", "points": 50},
    {"name": "RAPID_FIRE", "emoji": "⚡", "points": 40},
    {"name": "DOUBLE_SHOT", "emoji": "☢", "points": 35},
    {"name": "BOMB", "emoji": "💣", "points": 25},
    {"name": "HEALTH", "emoji": "❤", "points": 10},
]

# ============================================================================
# BOMB CONSTANTS
# ============================================================================
BOMB_RADIUS: int = 200
BOMB_COOLDOWN: float = 300  # frames (5 seconds at 60 FPS)

# ============================================================================
# LEVEL CONFIGURATION
# ============================================================================
LEVELS: dict[int, dict] = {
    1: {"enemy_count": 30, "difficulty_multiplier": 1.0},
    2: {"enemy_count": 40, "difficulty_multiplier": 1.05},
    3: {"enemy_count": 50, "difficulty_multiplier": 1.1},
    4: {"enemy_count": 60, "difficulty_multiplier": 1.15},
    5: {"enemy_count": 70, "difficulty_multiplier": 1.2},
    6: {"enemy_count": 80, "difficulty_multiplier": 1.25},
    7: {"enemy_count": 90, "difficulty_multiplier": 1.3},
    8: {"enemy_count": 100, "difficulty_multiplier": 1.35},
    9: {"enemy_count": 110, "difficulty_multiplier": 1.4},
    10: {"enemy_count": 120, "difficulty_multiplier": 1.45, "boss_level": True},
}

# ============================================================================
# SCORING SYSTEM
# ============================================================================
POINTS_PER_ENEMY_LEVEL_1_8: int = 10  # 1-2 rows remaining
POINTS_PER_ENEMY_LEVEL_9_10: int = 15  # 3+ rows remaining or boss
BOSS_POINTS_MULTIPLIER: float = 2.0
LEVEL_MULTIPLIER: dict[str, int] = {
    "1ROW": 10,
    "2ROW": 15,
    "3ROW": 20,
    "4ROW": 25,
    "HALF": 5,
    "NONE": 10,
}

BOSS_LEVELS = [10]  # Boss only appears at level 10 for now
BOSS_HP: int = 100
BOSS_MAX_WIDTH: int = 600
BOSS_HEIGHT: int = 100
BOSS_DAMAGE: int = 50

# ============================================================================
# GAME STATES
# ============================================================================
GAME_STATE = {
    "MENU": "menu",
    "PLAYING": "playing",
    "PAUSED": "paused",
    "GAME_OVER": "game_over",
}

# ============================================================================
# AUDIO CONSTANTS
# ============================================================================
MAX_VOLUME: float = 1.0
MUSIC_VOLUME: float = 0.4
SFX_VOLUME: float = 0.6

# ============================================================================
# UTILITY MATH
# ============================================================================
PI: float = 3.1415926535897932
