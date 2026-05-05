"""
Enemy management for Space Invaders-style game.

Handles enemy formation, spawning, and patterns.
"""

import pygame
from typing import List
import constants


class Enemy:
    """
    Single enemy entity.

    Each enemy tracks its position and state.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize enemy at position.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.width = constants.ENEMY_WIDTH
        self.height = constants.ENEMY_HEIGHT
        self.x = x
        self.y = y
        self.speed = constants.ENEMY_BASE_SPEED
        self.active = True
        self.points = 10
        self.shoot_chance = constants.ENEMY_SHOOT_CHANCE


class EnemyManager:
    """
    Manages all enemies in the game.

    Handles formation spawning, movement, and collision detection.
    """

    def __init__(self, level: int = 1) -> None:
        """
        Initialize enemy manager for given level.

        Args:
            level: Current level (affects enemy count and speed)
        """
        self.enemies: List[dict] = []
        self.direction = 1  # 1 = right, -1 = left
        self.move_timer = 0
        self.move_interval = max(3, 8 - level)  # Faster with each level
        self.drop_distance = constants.ENEMY_DROP_DISTANCE
        self.speed = constants.ENEMY_BASE_SPEED + (level - 1) * 0.5

        # Spawn enemies in formation
        self._spawn_formation(level)

    def _spawn_formation(self, level: int) -> None:
        """Spawn enemies in classic Space Invaders formation."""
        enemy_width = constants.ENEMY_WIDTH
        enemy_height = constants.ENEMY_HEIGHT

        # Define formation: 4 rows, 7 columns (classic)
        rows = 4
        cols = 7

        # Calculate spacing
        total_width = cols * enemy_width + (cols - 1) * 10  # 10px spacing
        start_x = (constants.SCREEN_WIDTH - total_width) // 2
        start_y = 50

        # Spawn enemies in grid
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (enemy_width + 10)
                y = start_y + row * (enemy_height + 10)
                self.enemies.append(
                    {
                        "x": x,
                        "y": y,
                        "width": enemy_width,
                        "height": enemy_height,
                        "active": True,
                        "points": 10,
                        "level": level,
                    }
                )

    def update(self, enemy_speed: float) -> None:
        """
        Update all enemies with classic formation movement.

        Args:
            enemy_speed: Speed multiplier for movement
        """
        self.move_timer += 1

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            # Move all enemies horizontally
            move_down = False
            for enemy in self.enemies:
                if not enemy.get("active", True):
                    continue

                enemy["x"] += int(self.direction * self.speed * enemy_speed)

                # Check if any enemy hits the wall
                if (self.direction == 1 and enemy["x"] + enemy["width"] >= constants.SCREEN_WIDTH - 10) or (
                    self.direction == -1 and enemy["x"] <= 10
                ):
                    move_down = True

            # If hitting wall, move down and reverse direction
            if move_down:
                self.direction *= -1  # Reverse direction
                for enemy in self.enemies:
                    if enemy.get("active", True):
                        enemy["y"] += self.drop_distance

    def get_enemies(self) -> List[dict]:
        """
        Get active enemies.

        Returns:
            List of active enemy dictionaries
        """
        return [e for e in self.enemies if e.get("active", True)]

    def count_enemies(self) -> int:
        """
        Count active enemies.

        Returns:
            Number of active enemies
        """
        return len(self.get_enemies())

    def draw(self, screen: pygame.SurfaceType) -> None:
        """
        Draw all enemies.

        Args:
            screen: Pygame surface to draw on
        """
        for enemy in self.enemies:
            if enemy.get("active", True):
                # Draw enemy as red rectangle
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (enemy["x"], enemy["y"], enemy["width"], enemy["height"]),
                )
                # Draw enemy eyes
                pygame.draw.rect(screen, (255, 255, 255), (enemy["x"] + 6, enemy["y"] + 6, 4, 4))
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (enemy["x"] + enemy["width"] - 10, enemy["y"] + 6, 4, 4),
                )
