"""
Game states management for Space Invaders-style game.

Handles transitions between menu, playing, paused, and game over states.
"""

import pygame
from typing import Optional
import constants


class GameState:
    """
    Manages game state transitions and events.

    Handles:
        - Menu to playing transitions
        - Pausing with ESC button
        - Game over detection
        - Level transitions
        - Score tracking
    """

    def __init__(self) -> None:
        """Initialize game state."""
        self.state = constants.GAME_STATE["MENU"]
        self.score: int = 0
        self.level: int = 1
        self.high_score: int = 0
        self.lives: int = 3
        self.last_shot: float = 0

    def update(self, keys) -> Optional[str]:
        """
        Update game state and handle transitions.

        Args:
            keys: Pygame key module to check pressed keys

        Returns:
            New state if transition occurred, None otherwise
        """
        if self.state == constants.GAME_STATE["MENU"]:
            if keys[pygame.K_SPACE]:
                self.state = constants.GAME_STATE["PLAYING"]

        elif self.state == constants.GAME_STATE["PLAYING"]:
            if keys[pygame.K_ESCAPE]:
                self.state = constants.GAME_STATE["PAUSED"]
            elif keys[pygame.K_i]:
                self.state = constants.GAME_STATE["PAUSED"]

        elif self.state == constants.GAME_STATE["PAUSED"]:
            if keys[pygame.K_ESCAPE]:
                self.state = constants.GAME_STATE["PLAYING"]

        elif self.state == constants.GAME_STATE["GAME_OVER"]:
            if keys[pygame.K_SPACE]:
                self.state = constants.GAME_STATE["MENU"]

        return self.state if self.state != self.last_state else None

    def add_score(self, points: int) -> int:
        """
        Add points to score with level scaling.

        Args:
            points: Points to add

        Returns:
            Updated score
        """
        # Higher levels give more points per kill
        multiplier = self.level  # 1x at level 1, 2x at level 2, etc.
        self.score += points * multiplier
        return max(self.score, self.high_score)

    def update_high_score(self) -> int:
        """
        Update high score if surpassed.

        Returns:
            Updated high score
        """
        new_high = max(self.score, self.high_score)
        self.high_score = new_high
        return new_high

    def set_state(self, new_state: str) -> None:
        """
        Set new game state.

        Args:
            new_state: New state name
        """
        self.state = new_state
