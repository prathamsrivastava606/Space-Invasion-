import pygame
import random

from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet
from src.core.formation import create_grid, create_triangle, create_diamond, create_v, create_cross, create_arrow, create_hollow_rectangle


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("Arial", 64)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.enemy_speed = 2
        self.enemy_drop = 40

        self.score = 0
        self.lives = 3
        self.wave = 1
        self.game_over = False

        self.enemy_bullets = []

        self.enemies = create_grid()
        self.player = Player()

        self.ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ENEMY_SHOOT_EVENT, 1000)

        self.wave_transition = True
        self.wave_transition_time = 2000
        self.wave_start_time = pygame.time.get_ticks()

        self.running = True

    def reset_game(self):

        self.player = Player()
        self.enemies = create_grid()

        self.enemy_speed = 2

        self.score = 0
        self.lives = 3
        self.wave = 1
        self.enemy_bullets = []
        self.game_over = False

        self.wave_transition = True
        self.wave_start_time = pygame.time.get_ticks()

    def create_wave(self):

        formations = [
            create_grid,
            create_triangle,
            create_diamond,
            create_v,
            create_cross,
            create_arrow,
            create_hollow_rectangle
        ]

        formation = formations[(self.wave - 1) % len(formations)]

        return formation()

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and len(self.enemies) > 0 and not self.game_over and not self.wave_transition:
                    self.player.shoot()

                if event.key == pygame.K_r:
                    self.reset_game()

            if event.type == self.ENEMY_SHOOT_EVENT and len(self.enemies) > 0 and not self.game_over and not self.wave_transition:

                shooters = []

                for enemy in self.enemies:

                    enemy_rect = enemy.get_rect()
                    blocked = False

                    for other in self.enemies:

                        if other == enemy:
                            continue

                        other_rect = other.get_rect()

                        if other_rect.y > enemy_rect.y:

                            if enemy_rect.right > other_rect.left and enemy_rect.left < other_rect.right:
                                blocked = True
                                break

                    if not blocked:
                        shooters.append(enemy)

                if len(shooters) > 0:

                    selected_shooters = random.sample(
                        shooters,
                        min(3, len(shooters))
                    )

                    for shooter in selected_shooters:

                        x, y = shooter.shoot()

                        self.enemy_bullets.append(
                            EnemyBullet(x, y)
                        )

    def update(self):

        if self.wave_transition:

            if pygame.time.get_ticks() - self.wave_start_time >= self.wave_transition_time:

                self.wave_transition = False

            return

        if len(self.enemies) == 0 and not self.game_over:

            self.wave += 1
            self.enemies = self.create_wave()
            self.enemy_speed = 2 + (self.wave - 1) * 0.3

            self.wave_transition = True
            self.wave_start_time = pygame.time.get_ticks()

            self.enemy_bullets = []

            return

        if len(self.enemies) > 0 and not self.game_over:

            self.player.update()

            for bullet in self.enemy_bullets[:]:

                bullet.update()

                if bullet.off_screen():
                    self.enemy_bullets.remove(bullet)

            player_rect = pygame.Rect(
                self.player.x,
                self.player.y,
                self.player.width,
                self.player.height
            )

            for bullet in self.enemy_bullets[:]:

                if bullet.get_rect().colliderect(player_rect):

                    self.enemy_bullets.remove(bullet)

                    self.lives -= 1

                    if self.lives <= 0:

                        self.lives = 0
                        self.game_over = True
                        break

            for enemy in self.enemies:
                enemy.update(self.enemy_speed)

            hit_edge = False

            for enemy in self.enemies:

                if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
                    hit_edge = True
                    break

            if hit_edge:

                self.enemy_speed *= -1

                for enemy in self.enemies:
                    enemy.y += self.enemy_drop

            for bullet in self.player.bullets[:]:

                for enemy in self.enemies[:]:

                    if bullet.get_rect().colliderect(enemy.get_rect()):

                        if bullet in self.player.bullets:
                            self.player.bullets.remove(bullet)

                        if enemy in self.enemies:
                            self.enemies.remove(enemy)

                        self.score += 10
                        break

    def draw(self):

        self.screen.fill(BLACK)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)

        score_text = self.font.render(
            f"Score : {self.score}",
            True,
            WHITE
        )

        self.screen.blit(score_text, (20, 20))

        lives_text = self.font.render(
            f"Lives : {'❤' * self.lives}",
            True,
            WHITE
        )

        self.screen.blit(lives_text, (20, 60))

        wave_text = self.font.render(
            f"Wave : {self.wave}",
            True,
            WHITE
        )

        self.screen.blit(wave_text, (20, 100))

        if self.wave_transition and not self.game_over:

            elapsed = pygame.time.get_ticks() - self.wave_start_time
            progress = elapsed / self.wave_transition_time

            if progress > 1:
                progress = 1

            if progress < 0.5:
                fade = progress * 2
            else:
                fade = (1 - progress) * 2

            alpha = int(255 * fade)

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(BLACK)

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

            wave_text.set_alpha(alpha)
            ready_text.set_alpha(alpha)

            self.screen.blit(
                wave_text,
                (
                    WIDTH // 2 - wave_text.get_width() // 2,
                    HEIGHT // 2 - 70
                )
            )

            self.screen.blit(
                ready_text,
                (
                    WIDTH // 2 - ready_text.get_width() // 2,
                    HEIGHT // 2 + 10
                )
            )

        if self.game_over:

            game_over_text = self.big_font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            restart_text = self.font.render(
                "Press R to Restart",
                True,
                WHITE
            )

            self.screen.blit(
                game_over_text,
                (
                    WIDTH // 2 - game_over_text.get_width() // 2,
                    HEIGHT // 2 - 70
                )
            )

            self.screen.blit(
                restart_text,
                (
                    WIDTH // 2 - restart_text.get_width() // 2,
                    HEIGHT // 2 + 10
                )
            )

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()