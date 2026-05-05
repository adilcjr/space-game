"""
Player Entity for Space Invaders-style game.

This module handles player movement, shooting, and collision detection.
"""

import pygame
from typing import List
import constants


class Player:
    """
    Player ship entity with movement, shooting, and collision handling.

    Attributes:
        width: Player sprite width
        height: Player sprite height
        speed: Movement speed in pixels per frame
        cooldown: Frames between shots
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize player at given position.

        Args:
            x: Starting X coordinate
            y: Starting Y coordinate
        """
        self.width = constants.PLAYER_WIDTH
        self.height = constants.PLAYER_HEIGHT
        self.speed = constants.PLAYER_SPEED
        self.cooldown = constants.PLAYER_SHOOT_COOLDOWN
        self.x = x
        self.y = y
        self.shot = 0  # Frames since last shot
        self.on_screen = True

    def update(self) -> None:
        """Update player state."""
        # Reduce cooldown
        if self.shot > 0:
            self.shot -= 1

    def move(self, keys) -> None:
        """
        Move player based on key input.

        Args:
            keys: Pygame key pressed dict
        """
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < constants.SCREEN_WIDTH - self.width:
            self.x += self.speed

    def shoot(self, bullets: List[dict]) -> None:
        """
        Fire a bullet if cooldown allows.

        Args:
            bullets: List of all bullets to add new bullet to
        """
        if self.shot == 0:
            bullet_x = self.x + self.width // 2 - constants.PLAYER_BULLET_HEIGHT // 2
            bullets.append({"x": bullet_x, "y": self.y, "type": "player"})
            self.shot = self.cooldown

    def handle_collision(self, other: object) -> bool:
        """
        Check collision with other entity.

        Args:
            other: Entity to check collision with

        Returns:
            True if collision occurred
        """
        if isinstance(other, (list, tuple)):
            # Check against list of entities (enemies)
            return any(
                self.x < e["x"] + constants.ENEMY_WIDTH
                and self.x + self.width > e["x"]
                and self.y < e["y"] + constants.ENEMY_HEIGHT
                and self.y + self.height > e["y"]
                for e in other
            )

        # Check single entity
        other_x = other.x if hasattr(other, "x") else other["x"]
        other_y = other.y if hasattr(other, "y") else other["y"]
        other_w = other.width if hasattr(other, "width") else other.get("width", 0)
        other_h = other.height if hasattr(other, "height") else other.get("height", 0)

        return (
            self.x < other_x + other_w
            and self.x + self.width > other_x
            and self.y < other_y + other_h
            and self.y + self.height > other_y
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render player to screen.

        Args:
            screen: Pygame surface to draw on
        """
        self._draw_rectangle(screen)

    def _draw_rectangle(self, screen: pygame.Surface) -> None:
        """Draw player as blue rectangle."""
        pygame.draw.rect(screen, (0, 150, 255), (self.x, self.y, self.width, self.height))
        # Draw cockpit/detail
        pygame.draw.rect(screen, (0, 200, 255), (self.x + 4, self.y + 4, self.width - 8, 8))

    def __repr__(self) -> str:
        return (
            f"Player({self.x=}, {self.y=}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"shot={self.shot}, "
            f"on_screen={self.on_screen})"
        )
