import pygame
import math

from pygame import mixer

# initialize pygame
pygame.init()

# Create screen
screenX = 800
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))

# Make Icon
title = pygame.display.set_caption("Space Demon")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("space.png")

# Player Icon
player_img = pygame.image.load("spaceship.png")
playerX = 360
playerY = 460
playerX_change = 0
playerY_change = 0

# Enemy Icon
enemy_img = pygame.image.load("pngfuel.com.png")
enemyX = 360
enemyY = 50
enemyX_change = 1.5

# Bullet icon
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bulletY_change = 7
bullet_state = "ready"

# Explosion icon
explosion = pygame.image.load("explosion.png")

# Enemy Health
enemy_hp = 100
enemy_max = 100
font = pygame.font.Font("freesansbold.ttf", 16)

# Game Over Text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (200, 250))


def show_hp():
    eHp = font.render(f"HP : {str(enemy_hp)}/{str(enemy_max)}", True, (255, 255, 255))
    screen.blit(eHp, (10, 10))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 8, y + 5))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    x_axis = enemyX - bulletX
    y_axis = enemyY - bulletY
    distance = math.sqrt((math.pow(x_axis, 2)) + (math.pow(y_axis, 2)))
    if distance < 57:
        return True
    return False


def show_explosion(x, y):
    screen.blit(explosion, (x, y))


# Game Loop
running = True

while running:
    # Background Color
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))
    enemy(enemyX, enemyY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_UP:
                playerY_change = -3
            if event.key == pygame.K_DOWN:
                playerY_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Player Move
    playerX += playerX_change

    # Make X axis boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= screenX - 32:
        playerX = screenX - 32
    playerY += playerY_change

    # Make Y axis boundary
    if playerY <= 0:
        playerY = 0
    elif playerY >= screenY - 32:
        playerY = screenY - 32

    # Enemy Move
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 1.5
    elif enemyX >= screenX - 100:
        enemyX_change = -1.5

    # Bullet Move
    if bulletY < 0:
        bulletY = playerY
        bulletX = playerX
        bullet_state = "ready"
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Check Collision
    if isCollision(enemyX, enemyY, bulletX, bulletY):
        col_sound = mixer.Sound("explosion.wav")
        col_sound.play()
        show_explosion(bulletX, bulletY)
        bulletX = playerX
        bulletY = playerY
        bullet_state = "ready"
        enemy_hp -= 10
    if enemy_hp == 0:
        show_explosion(enemyX, enemyY)
        enemyY = 5000
        game_over()

    show_hp()
    player(playerX, playerY)
    pygame.display.update()
