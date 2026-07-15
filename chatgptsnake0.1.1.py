# ==========================================
# ChatGPT's Snake Engine v0.3
# Atari Speed Edition
# Files = OFF
# Python + Pygame
# 60 FPS Retro Engine
# ==========================================

import pygame
import random
import sys
import array

pygame.init()
pygame.mixer.init()


# -------------------------
# Built-in SFX
# -------------------------

def make_tone(freq, duration):
    rate = 44100
    samples = int(rate * duration)
    data = array.array("h")

    for i in range(samples):
        value = 14000 if (i * freq // rate) % 2 == 0 else -14000
        data.append(value)

    return pygame.mixer.Sound(buffer=data)


SFX_MENU = make_tone(700, 0.05)
SFX_EAT = make_tone(1000, 0.08)
SFX_DEATH = make_tone(200, 0.25)


# -------------------------
# Window
# -------------------------

WIDTH = 640
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatGPT's Snake Engine")

clock = pygame.time.Clock()


# -------------------------
# Colors
# -------------------------

BLACK = (0,0,0)
BLUE = (0,180,255)
DARK_BLUE = (0,35,90)
GREEN = (0,255,80)
RED = (255,50,50)


font = pygame.font.SysFont("Courier",28)
bigfont = pygame.font.SysFont("Courier",42)


# Atari style speed
MOVE_DELAY = 140


# -------------------------
# Button
# -------------------------

def button(text,y):

    rect = pygame.Rect(170,y,300,55)

    pygame.draw.rect(
        screen,
        BLACK,
        rect
    )

    label = font.render(
        text,
        True,
        BLUE
    )

    screen.blit(
        label,
        (
            rect.centerx-label.get_width()/2,
            rect.centery-label.get_height()/2
        )
    )

    return rect



# -------------------------
# Snake Game
# -------------------------

def play_game():

    snake=[(320,240)]

    direction=(20,0)

    food=(
        random.randrange(0,WIDTH,20),
        random.randrange(0,HEIGHT,20)
    )

    score=0

    last_move=pygame.time.get_ticks()


    while True:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_UP:
                    direction=(0,-20)

                if event.key == pygame.K_DOWN:
                    direction=(0,20)

                if event.key == pygame.K_LEFT:
                    direction=(-20,0)

                if event.key == pygame.K_RIGHT:
                    direction=(20,0)



        now=pygame.time.get_ticks()


        # Retro movement timer
        if now-last_move >= MOVE_DELAY:

            last_move=now

            head=(
                snake[0][0]+direction[0],
                snake[0][1]+direction[1]
            )

            snake.insert(0,head)


            if head == food:

                score+=1
                SFX_EAT.play()

                food=(
                    random.randrange(0,WIDTH,20),
                    random.randrange(0,HEIGHT,20)
                )

            else:
                snake.pop()



            if (
                head[0]<0 or
                head[0]>=WIDTH or
                head[1]<0 or
                head[1]>=HEIGHT or
                head in snake[1:]
            ):

                SFX_DEATH.play()
                return



        screen.fill(DARK_BLUE)


        for part in snake:

            pygame.draw.rect(
                screen,
                GREEN,
                (
                    part[0],
                    part[1],
                    20,
                    20
                )
            )


        pygame.draw.rect(
            screen,
            RED,
            (
                food[0],
                food[1],
                20,
                20
            )
        )


        score_text=font.render(
            f"SCORE {score}",
            True,
            BLUE
        )

        screen.blit(
            score_text,
            (10,10)
        )


        pygame.display.flip()



# -------------------------
# About
# -------------------------

def about():

    while True:

        screen.fill(DARK_BLUE)

        t=bigfont.render(
            "CHATGPT SNAKE",
            True,
            BLUE
        )

        screen.blit(
            t,
            (90,100)
        )


        info=font.render(
            "ATARI SPEED EDITION",
            True,
            BLUE
        )

        screen.blit(
            info,
            (80,180)
        )


        back=button(
            "BACK",
            300
        )


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if back.collidepoint(event.pos):
                    SFX_MENU.play()
                    return



# -------------------------
# Main Menu
# -------------------------

def main_menu():

    while True:

        screen.fill(DARK_BLUE)


        title=bigfont.render(
            "CHATGPT'S",
            True,
            BLUE
        )

        screen.blit(
            title,
            (160,50)
        )


        title2=bigfont.render(
            "SNAKE ENGINE",
            True,
            BLUE
        )

        screen.blit(
            title2,
            (90,100)
        )


        play=button("PLAY GAME",210)
        aboutb=button("ABOUT",280)
        exitb=button("EXIT GAME",350)


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN:


                if play.collidepoint(event.pos):
                    SFX_MENU.play()
                    play_game()


                if aboutb.collidepoint(event.pos):
                    SFX_MENU.play()
                    about()


                if exitb.collidepoint(event.pos):
                    SFX_MENU.play()
                    pygame.quit()
                    sys.exit()



main_menu()
