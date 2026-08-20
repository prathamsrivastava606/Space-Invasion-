import pygame
import random

from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("Arial", 64)

        self.enemy_speed = 2
        self.enemy_drop = 40

        self.score = 0
        self.lives = 3
        self.game_over = False

        self.enemy_bullets = []

        self.enemies = self.create_enemies()
        self.player = Player()

        self.ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ENEMY_SHOOT_EVENT, 1000)

        self.running = True

    def create_enemies(self):

        enemies = []

        ROWS = 2
        COLUMNS = 7

        START_X = 180
        START_Y = 80

        GAP_X = 100
        GAP_Y = 90

        for row in range(ROWS):
            for col in range(COLUMNS):

                x = START_X + col * GAP_X
                y = START_Y + row * GAP_Y

                enemies.append(Enemy(x, y))

        return enemies

    def reset_game(self):

        self.player = Player()
        self.enemies = self.create_enemies()

        self.enemy_speed = 2

        self.score = 0
        self.lives = 3
        self.enemy_bullets = []
        self.game_over = False

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and len(self.enemies) > 0 and not self.game_over:
                    self.player.shoot()

                if event.key == pygame.K_r:
                    self.reset_game()

            if event.type == self.ENEMY_SHOOT_EVENT and len(self.enemies) > 0 and not self.game_over:

                columns = {}

                for enemy in self.enemies:

                    column = round((enemy.x - 180) / 100)

                    if column not in columns or enemy.y > columns[column].y:
                        columns[column] = enemy

                shooters = random.sample(
                    list(columns.values()),
                    min(3, len(columns))
                )

                for shooter in shooters:

                    x, y = shooter.shoot()

                    self.enemy_bullets.append(
                        EnemyBullet(x, y)
                    )

    def update(self):

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

        if len(self.enemies) == 0 and not self.game_over:

            win_text = self.big_font.render(
                "YOU WIN!",
                True,
                (0, 255, 0)
            )

            restart_text = self.font.render(
                "Press R to Restart",
                True,
                WHITE
            )

            self.screen.blit(
                win_text,
                (
                    WIDTH // 2 - win_text.get_width() // 2,
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