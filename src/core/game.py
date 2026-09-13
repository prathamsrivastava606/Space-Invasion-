import pygame
import random

from settings import *

from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.entities.explosion import Explosion

from src.core.background import SpaceBackground
from src.core.hud import HUD
from src.core.audio import Audio

from src.core.formation import (
    create_grid,
    create_triangle,
    create_diamond,
    create_v,
    create_cross,
    create_arrow,
    create_hollow_rectangle,
    SHIP_TYPES
)

from src.core.difficulty import (
    get_enemy_speed,
    get_shoot_interval,
    get_max_shooters
)


class Game:

    def __init__(self):

        pygame.init()

        # =================================================
        # AUDIO
        # =================================================

        self.audio = Audio()
        self.audio.play_music()

        # =================================================
        # WINDOW
        # =================================================

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.RESIZABLE | pygame.SCALED
        )

        pygame.display.set_caption(TITLE)

        # Start maximized while keeping
        # the normal Windows title bar
        try:
            window = pygame._sdl2.Window.from_display_module()
            window.maximize()
        except:
            pass

        self.clock = pygame.time.Clock()

        # =================================================
        # FONTS
        # =================================================

        self.font = pygame.font.SysFont(
            "Arial",
            32
        )

        self.big_font = pygame.font.SysFont(
            "Arial",
            64
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            24
        )

        # =================================================
        # BACKGROUND
        # =================================================

        self.background = SpaceBackground(
            WIDTH,
            HEIGHT
        )

        # =================================================
        # HUD
        # =================================================

        self.hud = HUD(
            WIDTH,
            HEIGHT
        )

        # =================================================
        # GAME SETTINGS
        # =================================================

        self.enemy_speed = get_enemy_speed(1)

        self.enemy_drop = 40

        self.score = 0
        self.lives = 3
        self.wave = 1

        self.game_over = False

        # =================================================
        # BULLETS / EFFECTS
        # =================================================

        self.enemy_bullets = []
        self.explosions = []

        # =================================================
        # PLAYER / ENEMIES
        # =================================================

        self.enemies = create_grid(
            "enemyBlack3"
        )

        self.player = Player()

        # =================================================
        # ENEMY SHOOTING TIMER
        # =================================================

        self.ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1

        pygame.time.set_timer(
            self.ENEMY_SHOOT_EVENT,
            get_shoot_interval(self.wave)
        )

        # =================================================
        # WAVE TRANSITION
        # =================================================

        self.wave_transition = True

        self.wave_transition_time = 2000

        self.wave_start_time = pygame.time.get_ticks()

        # =================================================
        # GAME LOOP
        # =================================================

        self.running = True

    # =====================================================
    # RESET GAME
    # =====================================================

    def reset_game(self):

        self.player = Player()

        self.wave = 1

        self.enemies = create_grid(
            "enemyBlack3"
        )

        self.enemy_speed = get_enemy_speed(1)

        self.score = 0
        self.lives = 3

        self.enemy_bullets = []
        self.explosions = []

        self.game_over = False

        pygame.time.set_timer(
            self.ENEMY_SHOOT_EVENT,
            get_shoot_interval(self.wave)
        )

        self.wave_transition = True

        self.wave_start_time = pygame.time.get_ticks()

    # =====================================================
    # CREATE WAVE
    # =====================================================

    def create_wave(self):

        # -----------------------------
        # WAVE 1
        # -----------------------------

        if self.wave == 1:

            return create_grid(
                "enemyBlack3"
            )

        # -----------------------------
        # WAVE 2
        # -----------------------------

        if self.wave == 2:

            return create_triangle(
                "enemyBlue3"
            )

        # -----------------------------
        # WAVE 3
        # -----------------------------

        if self.wave == 3:

            return create_diamond(
                "enemyGreen3"
            )

        # -----------------------------
        # WAVE 4
        # -----------------------------

        if self.wave == 4:

            return create_v(
                "enemyRed3"
            )

        # -----------------------------
        # WAVE 5+
        # -----------------------------

        formations = [
            create_cross,
            create_arrow,
            create_hollow_rectangle
        ]

        formation = formations[
            (self.wave - 5) % len(formations)
        ]

        return formation(
            SHIP_TYPES
        )

    # =====================================================
    # HANDLE EVENTS
    # =====================================================

    def handle_events(self):

        for event in pygame.event.get():

            # -----------------------------
            # WINDOW CLOSE
            # -----------------------------

            if event.type == pygame.QUIT:

                self.running = False

            # -----------------------------
            # KEYBOARD
            # -----------------------------

            if event.type == pygame.KEYDOWN:

                # Player shooting
                if (
                    event.key == pygame.K_SPACE
                    and len(self.enemies) > 0
                    and not self.game_over
                    and not self.wave_transition
                ):

                    self.player.shoot()

                # Restart
                if event.key == pygame.K_r:

                    self.reset_game()

            # -----------------------------
            # ENEMY SHOOTING
            # -----------------------------

            if (
                event.type == self.ENEMY_SHOOT_EVENT
                and len(self.enemies) > 0
                and not self.game_over
                and not self.wave_transition
            ):

                shooters = []

                # Find enemies that are not blocked
                for enemy in self.enemies:

                    enemy_rect = enemy.get_rect()

                    blocked = False

                    for other in self.enemies:

                        if other == enemy:
                            continue

                        other_rect = other.get_rect()

                        if other_rect.y > enemy_rect.y:

                            if (
                                enemy_rect.right > other_rect.left
                                and enemy_rect.left < other_rect.right
                            ):

                                blocked = True

                                break

                    if not blocked:

                        shooters.append(enemy)

                # Select shooters
                if len(shooters) > 0:

                    max_shooters = get_max_shooters(
                        self.wave
                    )

                    selected_shooters = random.sample(
                        shooters,
                        min(
                            max_shooters,
                            len(shooters)
                        )
                    )

                    for shooter in selected_shooters:

                        x, y = shooter.shoot()

                        self.enemy_bullets.append(
                            EnemyBullet(x, y)
                        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        # =================================================
        # UPDATE BACKGROUND
        # =================================================

        self.background.update()

        # =================================================
        # WAVE TRANSITION
        # =================================================

        if self.wave_transition:

            if (
                pygame.time.get_ticks()
                - self.wave_start_time
                >= self.wave_transition_time
            ):

                self.wave_transition = False

            return

        # =================================================
        # NEXT WAVE
        # =================================================

        if (
            len(self.enemies) == 0
            and not self.game_over
        ):

            self.wave += 1

            self.enemies = self.create_wave()

            self.enemy_speed = get_enemy_speed(
                self.wave
            )

            pygame.time.set_timer(
                self.ENEMY_SHOOT_EVENT,
                get_shoot_interval(self.wave)
            )

            self.wave_transition = True

            self.wave_start_time = pygame.time.get_ticks()

            self.enemy_bullets = []

            self.explosions = []

            return

        # =================================================
        # GAMEPLAY
        # =================================================

        if (
            len(self.enemies) > 0
            and not self.game_over
        ):

            # -----------------------------
            # PLAYER
            # -----------------------------

            self.player.update()

            # -----------------------------
            # ENEMY BULLETS
            # -----------------------------

            for bullet in self.enemy_bullets[:]:

                bullet.update()

                if bullet.off_screen():

                    self.enemy_bullets.remove(
                        bullet
                    )

            # -----------------------------
            # PLAYER COLLISION
            # -----------------------------

            player_rect = pygame.Rect(
                self.player.x,
                self.player.y,
                self.player.width,
                self.player.height
            )

            for bullet in self.enemy_bullets[:]:

                if bullet.get_rect().colliderect(
                    player_rect
                ):

                    self.enemy_bullets.remove(
                        bullet
                    )

                    self.lives -= 1

                    if self.lives <= 0:

                        self.lives = 0

                        self.game_over = True

                        break

            # -----------------------------
            # ENEMY MOVEMENT
            # -----------------------------

            for enemy in self.enemies:

                enemy.update(
                    self.enemy_speed
                )

            # -----------------------------
            # EDGE DETECTION
            # -----------------------------

            hit_edge = False

            for enemy in self.enemies:

                if (
                    enemy.x <= 0
                    or enemy.x + enemy.width >= WIDTH
                ):

                    hit_edge = True

                    break

            # -----------------------------
            # CHANGE DIRECTION
            # -----------------------------

            if hit_edge:

                self.enemy_speed *= -1

                for enemy in self.enemies:

                    enemy.y += self.enemy_drop

            # -----------------------------
            # PLAYER BULLETS
            # -----------------------------

            for bullet in self.player.bullets[:]:

                for enemy in self.enemies[:]:

                    if bullet.get_rect().colliderect(
                        enemy.get_rect()
                    ):

                        # Remove bullet
                        if bullet in self.player.bullets:

                            self.player.bullets.remove(
                                bullet
                            )

                        # Remove enemy
                        if enemy in self.enemies:

                            self.enemies.remove(
                                enemy
                            )

                            # Explosion
                            self.explosions.append(
                                Explosion(
                                    enemy.x
                                    + enemy.width // 2,

                                    enemy.y
                                    + enemy.height // 2,

                                    max(
                                        enemy.width,
                                        enemy.height
                                    )
                                )
                            )

                        # Score
                        self.score += 10

                        break

        # =================================================
        # EXPLOSIONS
        # =================================================

        for explosion in self.explosions[:]:

            explosion.update()

            if explosion.finished:

                self.explosions.remove(
                    explosion
                )

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        # =================================================
        # BACKGROUND
        # =================================================

        self.background.draw(
            self.screen
        )

        # =================================================
        # ENEMIES
        # =================================================

        for enemy in self.enemies:

            enemy.draw(
                self.screen
            )

        # =================================================
        # PLAYER
        # =================================================

        self.player.draw(
            self.screen
        )

        # =================================================
        # ENEMY BULLETS
        # =================================================

        for bullet in self.enemy_bullets:

            bullet.draw(
                self.screen
            )

        # =================================================
        # EXPLOSIONS
        # =================================================

        for explosion in self.explosions:

            explosion.draw(
                self.screen
            )

        # =================================================
        # HUD
        # =================================================

        self.hud.draw(
            self.screen,
            self.score,
            self.lives,
            self.wave,
            self.game_over,
            self.wave_transition
        )

        # =================================================
        # WAVE TRANSITION
        # =================================================

        if (
            self.wave_transition
            and not self.game_over
        ):

            elapsed = (
                pygame.time.get_ticks()
                - self.wave_start_time
            )

            progress = (
                elapsed
                / self.wave_transition_time
            )

            if progress > 1:

                progress = 1

            if progress < 0.5:

                fade = progress * 2

            else:

                fade = (1 - progress) * 2

            alpha = int(
                255 * fade
            )

            wave_text = self.big_font.render(
                f"WAVE {self.wave}",
                True,
                WHITE
            )

            ready_text = self.small_font.render(
                "GET READY...",
                True,
                WHITE
            )

            wave_text.set_alpha(
                alpha
            )

            ready_text.set_alpha(
                alpha
            )

            self.screen.blit(
                wave_text,
                (
                    WIDTH // 2
                    - wave_text.get_width() // 2,

                    HEIGHT // 2 - 70
                )
            )

            self.screen.blit(
                ready_text,
                (
                    WIDTH // 2
                    - ready_text.get_width() // 2,

                    HEIGHT // 2 + 10
                )
            )

        # =================================================
        # GAME OVER
        # =================================================

        if self.game_over:

            # Dark overlay
            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 100)
            )

            self.screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = self.big_font.render(
                "GAME OVER",
                True,
                (255, 80, 80)
            )

            restart_text = self.font.render(
                "Press R to Restart",
                True,
                WHITE
            )

            self.screen.blit(
                game_over_text,
                (
                    WIDTH // 2
                    - game_over_text.get_width() // 2,

                    HEIGHT // 2 - 70
                )
            )

            self.screen.blit(
                restart_text,
                (
                    WIDTH // 2
                    - restart_text.get_width() // 2,

                    HEIGHT // 2 + 10
                )
            )

        # =================================================
        # DISPLAY
        # =================================================

        pygame.display.flip()

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        # Stop background music before quitting
        self.audio.stop_music()

        pygame.quit()