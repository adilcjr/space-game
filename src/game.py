"""
Main Game Class for Space Invaders-style game.

Coordinates game loop, state management, and entity management.
"""

import pygame
from player import Player
from game_state import GameState
from enemies import EnemyManager
from bullet import BulletManager
import constants


class Game:
    """
    Main game class that manages all game components.

    Coordinates:
        - Game loop
        - State transitions
        - Entity management
        - Score tracking
        - Level progression
    """

    def __init__(self):
        """Initialize game with all components."""
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders - Retro Arcade Game")

        # Create game components FIRST
        self.game_state = GameState()
        self.player = Player(
            x=constants.SCREEN_WIDTH // 2 - constants.PLAYER_WIDTH // 2,
            y=constants.SCREEN_HEIGHT - constants.PLAYER_HEIGHT - 10,
        )
        self.enemy_manager = EnemyManager(level=1)
        self.bullet_manager = BulletManager()

        # NOW set state
        self.game_state.state = constants.GAME_STATE["PLAYING"]

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Game settings
        self.enemy_speed = constants.ENEMY_BASE_SPEED
        self.enemy_move_timer = 0
        self.enemy_move_interval = 10
        self.frame_count = 0
        self.running = True

    def run(self):
        """Run the main game loop."""
        self.running = True

        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(constants.FPS)

    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _update(self):
        """Update all game entities."""
        # Only update if playing
        if self.game_state.state != constants.GAME_STATE["PLAYING"]:
            return

        self.keys = pygame.key.get_pressed()
        self.player.update()
        self.player.move(self.keys)

        # Handle shooting
        if self.keys[pygame.K_SPACE] and self.player.shot == 0:
            self.player.shoot(self.bullet_manager.bullets)

        # Update bullets
        self.bullet_manager.update()

        # Update enemies with formation movement
        self.enemy_manager.update(self.enemy_speed)

        # Enemy shooting (very low chance - 1 per 10 seconds at 60fps)
        import random

        enemy_count = self.enemy_manager.count_enemies()
        if enemy_count > 0:
            shoot_chance = 0.00005  # Very low chance
            for enemy in self.enemy_manager.enemies:
                if enemy.get("active", True) and random.random() < shoot_chance:
                    self.bullet_manager.fire_enemy_shot(
                        enemy["x"] + enemy["width"] // 2,
                        enemy["y"] + enemy["height"],
                        self.player.x + self.player.width // 2,
                    )

        # Check collisions
        self._check_collisions()

        # Check level completion
        if self.enemy_manager.count_enemies() == 0:
            self._check_level_complete()

    def _check_collisions(self):
        """Check all collisions between entities."""
        # Player bullets vs enemies
        for bullet in self.bullet_manager.bullets[:]:
            if bullet.get("type") == "player" and bullet.get("active", True):
                for enemy in self.enemy_manager.enemies:
                    if (
                        enemy.get("active", True)
                        and bullet["x"] < enemy["x"] + enemy["width"]
                        and bullet["x"] + bullet.get("width", 4) > enemy["x"]
                        and bullet["y"] < enemy["y"] + enemy["height"]
                        and bullet["y"] + bullet.get("height", 4) > enemy["y"]
                    ):
                        # Hit only the first enemy and break
                        enemy["active"] = False
                        bullet["active"] = False
                        self.game_state.add_score(enemy.get("points", 10))
                        break

        # Remove inactive bullets after collision checks
        self.bullet_manager.bullets = [b for b in self.bullet_manager.bullets if b.get("active", True)]

        # Enemy bullets vs player
        for bullet in self.bullet_manager.bullets[:]:
            if bullet.get("type") == "enemy":
                if (
                    bullet["x"] < self.player.x + self.player.width
                    and bullet["x"] + bullet.get("width", 4) > self.player.x
                    and bullet["y"] < self.player.y + self.player.height
                    and bullet["y"] + bullet.get("height", 4) > self.player.y
                ):
                    # Hit player!
                    bullet["active"] = False
                    self.game_state.lives -= 1
                    print(f"💔 Player hit! Lives remaining: {self.game_state.lives}")

                    if self.game_state.lives <= 0:
                        self.game_state.state = constants.GAME_STATE["GAME_OVER"]
                        print("💀 Game Over!")

    def _check_level_complete(self):
        """Check if level is complete and advance."""
        if self.enemy_manager.count_enemies() == 0:
            self.game_state.level += 1
            if self.game_state.level <= 10:
                self.enemy_manager = EnemyManager(level=self.game_state.level)
                print(f"✓ Level {self.game_state.level} started!")
            else:
                print("✓ All levels complete!")

    def _draw(self):
        """Draw all game elements."""
        # Always draw background
        self.screen.fill((0, 0, 30))  # Dark blue space

        # Draw game elements regardless of state for now
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)

        # Draw bullets
        for bullet in self.bullet_manager.bullets:
            if bullet.get("active", True):
                color = (255, 255, 200) if bullet.get("type") == "player" else (255, 0, 0)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        bullet.get("x", 0),
                        bullet.get("y", 0),
                        bullet.get("width", 4),
                        bullet.get("height", 4),
                    ),
                )
        # Draw UI elements (score, lives, level)
        self._draw_ui()
        # Update the display
        pygame.display.flip()

    def _draw_ui(self):
        """Draw user interface."""
        font = pygame.font.Font(None, 24)
        score_diff = 0
        # Calculate score difference for display if necessary, otherwise use direct f-string
        score_text = font.render(f"Score: {self.game_state.score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {self.game_state.lives}", True, (255, 100, 100))
        level_text = font.render(f"Level: {self.game_state.level}", True, (200, 200, 0))

        # Positioning coordinates based on screen dimensions
        SCORE_X, SCORE_Y = constants.SCREEN_WIDTH - 100, 10
        LIVES_X, LIVES_Y = 10, 10
        LEVEL_X, LEVEL_Y = (constants.SCREEN_WIDTH - 100) // 2, 10

        # Blit the text surfaces at calculated positions
        pygame.display.get_surface().blit(score_text, (SCORE_X, SCORE_Y))
        pygame.display.get_surface().blit(lives_text, (LIVES_X, LIVES_Y))
        pygame.display.get_surface().blit(level_text, (LEVEL_X, LEVEL_Y))
