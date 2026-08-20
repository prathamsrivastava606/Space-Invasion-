import pygame
import sys
import random

from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.enemy_bullet import EnemyBullet

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 64)


def create_enemies():
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


def reset_game():

    global player
    global enemies
    global enemy_speed
    global score
    global lives
    global enemy_bullets
    global game_over

    player = Player()
    enemies = create_enemies()

    enemy_speed = 2

    score = 0
    lives = 3
    enemy_bullets = []
    game_over = False


player = Player()
enemies = create_enemies()

enemy_speed = 2
enemy_drop = 40

score = 0
lives = 3
game_over = False

enemy_bullets = []

ENEMY_SHOOT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 1000)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and len(enemies) > 0 and not game_over:
                player.shoot()

            if event.key == pygame.K_r:
                reset_game()

        if event.type == ENEMY_SHOOT_EVENT and len(enemies) > 0 and not game_over:

            shooter = random.choice(enemies)

            x, y = shooter.shoot()

            enemy_bullets.append(
                EnemyBullet(x, y)
            )

    if len(enemies) > 0 and not game_over:

        player.update()

        for bullet in enemy_bullets[:]:

            bullet.update()

            if bullet.off_screen():
                enemy_bullets.remove(bullet)

        player_rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )

        for bullet in enemy_bullets[:]:

            if bullet.get_rect().colliderect(player_rect):

                enemy_bullets.remove(bullet)

                lives -= 1

                if lives <= 0:
                    lives = 0
                    game_over = True
                    break

        for enemy in enemies:
            enemy.update(enemy_speed)

        hit_edge = False

        for enemy in enemies:

            if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
                hit_edge = True
                break

        if hit_edge:

            enemy_speed *= -1

            for enemy in enemies:
                enemy.y += enemy_drop

        for bullet in player.bullets[:]:

            for enemy in enemies[:]:

                if bullet.get_rect().colliderect(enemy.get_rect()):

                    if bullet in player.bullets:
                        player.bullets.remove(bullet)

                    if enemy in enemies:
                        enemies.remove(enemy)

                    score += 10
                    break

    screen.fill(BLACK)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    for bullet in enemy_bullets:
        bullet.draw(screen)

    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    lives_text = font.render(f"Lives : {'❤' * lives}", True, WHITE)
    screen.blit(lives_text, (20, 60))

    if len(enemies) == 0 and not game_over:

        win_text = big_font.render("YOU WIN!", True, (0, 255, 0))
        restart_text = font.render("Press R to Restart", True, WHITE)

        screen.blit(
            win_text,
            (
                WIDTH // 2 - win_text.get_width() // 2,
                HEIGHT // 2 - 70
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )

    if game_over:

        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, WHITE)

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - game_over_text.get_width() // 2,
                HEIGHT // 2 - 70
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                HEIGHT // 2 + 10
            )
        )

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()