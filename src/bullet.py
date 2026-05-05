"""
Bullet system for Space Invaders-style game.

Handles player bullets, enemy bullets, and projectiles.
"""

import pygame

# Removed unused 'typing' import for type-hinting cleanup in future runs
import constants


def create_player_bullet(x: int, y: int) -> dict:
    """
    Create player bullet at given position.

    Args:
        x: X position
        y: Y position

    Returns:
        Dictionary with bullet state
    """
    return {
        "x": x,
        "y": y,
        "width": constants.PLAYER_BULLET_HEIGHT,
        "height": 8,
        "type": "player",
        "speed": constants.PLAYER_BULLET_SPEED,
        "active": True,
    }


def create_enemy_bullet(x: int, y: int, target_x: int) -> dict:
    """
    Create enemy bullet targeting player at given position.

    Args:
        x: Enemy X position
        y: Enemy Y position
        target_x: Target player X position

    Returns:
        Dictionary with enemy bullet state with trajectory
    """
    # Calculate trajectory towards player
    direction = 1 if target_x > x else -1

    return {
        "x": x,
        "y": y + constants.ENEMY_HEIGHT,
        "width": 6,
        "height": 12,
        "type": "enemy",
        "direction": direction,
        "target_x": target_x,
        "speed": 6,
        "delta_x": direction * (target_x - x) / 10,  # Track towards player
        "active": True,
    }


def create_bomb() -> dict:
    """
    Create bomb powerup.

    Returns:
        Dictionary with bomb state
    """
    return {
        "x": 0,
        "y": 0,
        "width": 32,
        "height": 32,
        "type": "bomb",
        "active": False,  # Not spawned yet
    }


class BulletManager:
    """
    Manages all bullets in the game.

    Handles player bullets, enemy shot, collision detection,
    and powerup drops.
    """

    def __init__(self) -> None:
        """Initialize bullet manager."""
        self.bullets: List[dict] = []
        self.particles: List[dict] = []
        self.bomb_cooldown_timer: int = 0
        self.bomb_cooldown = constants.BOMB_COOLDOWN // 60  # Convert to seconds

    def update(self) -> None:
        """Update all bullets and list."""
        # Update bullet positions
        for bullet in self.bullets:
            if bullet.get("type") == "player":
                bullet["y"] -= bullet.get("speed", 10)
            else:
                bullet["y"] += bullet.get("speed", 6)
                # Move horizontally towards target
                if "target_x" in bullet:
                    if bullet["x"] < bullet["target_x"]:
                        bullet["x"] += 1
                    elif bullet["x"] > bullet["target_x"]:
                        bullet["x"] -= 1

        # Remove bullets that went off screen
        self.bullets = [b for b in self.bullets if 0 <= b.get("y", 0) <= constants.SCREEN_HEIGHT]

        # Update bomb timer
        if self.bomb_cooldown_timer > 0:
            self.bomb_cooldown_timer -= 1

    def fire_player_bullet(self, x: int, y: int) -> None:
        """
        Fire a bullet.

        Args:
            x: X position of bullet spawn
            y: Y position of bullet spawn
        """
        self.bullets.append(create_player_bullet(x, y))

    def fire_enemy_shot(self, x: int, y: int, target_x: int) -> None:
        """
        Fire enemy shot.

        Args:
            x: X position
            y: Y position
            target_x: Where enemy is targeting
        """
        self.bullets.append(create_enemy_bullet(x, y, target_x))

    def spawn_particles(self, position: tuple[int, int]) -> None:
        """
        Spawn particles at given position, for visual effect.

        Args:
            position: (x, y) spawn position
        """
        self.particles = [{"x": x, "y": y, "velocity": -3, "active": True} for x, y in [position] for _ in range(5)]
