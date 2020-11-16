# Space Invader game using python turtle module
# Created by Meezan malek

import pygame
import random
import math
from pygame import mixer

# initialize game
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800, 600))  # passing width and height

# title and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

# Background image
backgroungImg = pygame.image.load("background.png")

#Background sound
mixer.music.load("background.wav")
mixer.music.play(-1) #play background music on loop

# defining our player
player_icon = pygame.image.load('player.png')
playerX = 370
playerY = 480
changedX = 0
playerSpeed = 9

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def showing_score(x,y):
    score = font.render("Score  : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

#game over
def game_over():
    overfont = pygame.font.Font('freesansbold.ttf',64)
    gamefont = overfont.render("GAME OVER",True,(255,255,255))
    screen.blit(gamefont,(200,250))

def meezan(x,y):
    font2 = pygame.font.Font('freesansbold.ttf',16)
    score = font2.render("Developed by Meezan malik",True,(255,255,255))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(player_icon, (playerX, playerY))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# defining our bullet
bullet_icon = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_changed = 15  #bullet speed
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet_icon, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
# main game loop
while running:

    screen.fill((0, 0, 0))  # background
    screen.blit(backgroungImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player movement functionally
        if event.type == pygame.KEYDOWN:
            # print("you preesed a key")

            if event.key == pygame.K_LEFT:
                # print("left key pressed")
                changedX = -playerSpeed

            if event.key == pygame.K_RIGHT:
                # print("right key pressed")
                changedX = playerSpeed

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_state = "fired"

        if event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            changedX = 0

    # player movement
    playerX += changedX
    # restricting the player inside the window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            meezan(300,350)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            mixer.Sound("explosion.wav").play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fired":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_changed

    showing_score(10,10)

    player(playerX, playerY)
    pygame.display.update()
