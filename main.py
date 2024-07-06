import pygame
from random import randrange
import math
import sys
from player import Player
from colors import color_dict 
from boxes import Box
from button import Button
from difficulty import *

# Pygame setup
pygame.init()
HEIGHT = 500
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create sprite groups for player and boxes
player_group = pygame.sprite.Group()
p = Player(250, 400)
player_group.add(p)

box_group = pygame.sprite.Group()
time_last_spawn = 0

# Create target rectangle and border
target_rectangle = pygame.Rect(10, 10, 100, 100)
target_color = list(color_dict.values())[randrange(0, len(color_dict) - 2)]
target_rectangle_border = pygame.Rect(6, 6, 108, 108)
target_color_border = (0,0,0)

# Create font
f = pygame.font.Font(size = 72)
f2 = pygame.font.Font(size = 50)

# Create buttons for main_menu() function
start_button = Button('Start', f, (0,0,0), (WIDTH//2, HEIGHT//3))
difficulty_button = Button('Difficulty', f, (0,0,0), (WIDTH//2, HEIGHT//2))

# Create buttons for difficulty_menu() function
easy_button = Button('Easy', f, (0,0,0), (WIDTH//2, HEIGHT//5 * 1))
medium_button = Button('Medium', f, (0,0,0), (WIDTH//2, HEIGHT//5 * 2))
hard_button = Button('Hard', f, (0,0,0), (WIDTH//2, HEIGHT//5 * 3))
nightmare_button = Button('Nightmare', f, (0,0,0), (WIDTH//2, HEIGHT//5 * 4))

# Create buttons for game_over_menu() function
main_menu_button = Button('Main Menu', f, (0,0,0), (WIDTH//5 * 1, HEIGHT//5 * 4))
play_again_button = Button('Play Again', f, (0,0,0), (WIDTH//5 * 4, HEIGHT//5 * 4))

# Get difficulty data
difficulty_data = Difficulty(my_dict = difficulty_dict, level = 'easy')

# Create an event - the target_color of target_rectangle will change every n seconds depending on difficulty_data
CHANGECOLOR = pygame.event.custom_type()
pygame.time.set_timer(CHANGECOLOR, difficulty_data.subset_dict['target_color_duration'])

lives = 3
player_score = 0
time_last_color = 0

def main_menu(difficulty_data):
    pygame.mouse.set_visible(True)
    while True:

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_for_click(pos):
                    pygame.time.wait(1000)
                    play(difficulty_data)
                if difficulty_button.check_for_click(pos):
                    difficulty_menu()

        screen.fill((221, 221, 221))
        start_button.update(screen)
        difficulty_button.update(screen)
        pygame.display.flip()
        clock.tick(30)

def difficulty_menu():
    pygame.mouse.set_visible(True)
    while True:

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.check_for_click(pos):
                    difficulty_data.update_difficulty('easy')
                    main_menu(difficulty_data)
                if medium_button.check_for_click(pos):
                    difficulty_data.update_difficulty('medium')
                    main_menu(difficulty_data)
                if hard_button.check_for_click(pos):
                    difficulty_data.update_difficulty('hard')
                    main_menu(difficulty_data)
                if nightmare_button.check_for_click(pos):
                    difficulty_data.update_difficulty('nightmare')            
                    main_menu(difficulty_data)


        screen.fill((221, 221, 221))
        easy_button.update(screen)
        medium_button.update(screen)
        hard_button.update(screen)
        nightmare_button.update(screen)

        pygame.display.flip()
        clock.tick(30)

def play(difficulty_data):

    global color_dict
    global time_last_spawn
    global time_since_start
    global target_color
    global player_score
    global lives

    pygame.mouse.set_visible(False)

    while True:
        time_since_start = pygame.time.get_ticks() # Time since start of play()
        screen.fill(list(color_dict.values())[len(color_dict)-1]) # Background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

            # If CHANGECOLOR event occurs, update the color of the target_rectangle
            if event.type == CHANGECOLOR:
                target_color = list(color_dict.values())[randrange(0, len(color_dict) - 2)]

        # If time since the last box spawned, is greater than 'enemy_spawn_time', add a new box the box_group
        if pygame.time.get_ticks() - time_last_spawn > difficulty_data.subset_dict['enemy_spawn_time']:
                time_last_spawn = pygame.time.get_ticks()
                b = Box(randrange(30, WIDTH), randrange(-10, difficulty_data.subset_dict['enemy_spawn_location']), color_dict, difficulty_data.subset_dict['enemy_speed'])
                box_group.add(b)

        # Move/update the player and box groups.  Draw functions come from Sprite class
        player_group.update()
        player_group.draw(screen)

        box_group.update()
        box_group.draw(screen)

        # Check for collissions between groups
        collisions = pygame.sprite.groupcollide(player_group, box_group, dokilla = 0, dokillb = 1) # Output is a dictionary

        # If collision exists and box color is the same as the target_color of the target_rectangle, increase score, else decrease score
        for player in collisions:
            for box in collisions[player]:
                if box.color == target_color:
                    player_score += difficulty_data.subset_dict['score_increase']
                else:
                    player_score -= difficulty_data.subset_dict['score_decrease']
                    lives -= 1
                    if lives == 0:
                        box_group.empty()
                        game_over_menu()


        # Turn player score into a string and blit to screen. Do this towards the end so that boxes are not shown in front of the player_score_suface.
        player_score_str = str(player_score) 
        player_score_surface = f.render(player_score_str, 'AA', (0, 0, 0))
        screen.blit(player_score_surface, (WIDTH - 100, 25))

        # Draw target rectangle and border. Do this after updating the box_group so that boxes are not shown in front of the target_rectangle.
        pygame.draw.rect(screen, target_color_border, target_rectangle_border)
        pygame.draw.rect(screen, target_color, target_rectangle)

        pygame.display.flip()
        clock.tick(30)

def game_over_menu():

    global player_score
    global lives

    pygame.mouse.set_visible(True)
    while True:

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_for_click(pos):
                    lives = 3
                    player_score = 0
                    main_menu(difficulty_data)
                if play_again_button.check_for_click(pos):
                    lives = 3
                    player_score = 0
                    play(difficulty_data)


        screen.fill((221, 221, 221))
        # Turn player score into a string and blit to screen. Do this towards the end so that boxes are not shown in front of the player_score_suface.
        player_score_str = "Game over.  Your score is " + str(player_score) + "."
        player_score_surface = f2.render(player_score_str, 'AA', (0, 0, 0))
        text_width, text_height = player_score_surface.get_size()
        x_position = (WIDTH - text_width) // 2
        y_position = (HEIGHT - text_height) // 2
        screen.blit(player_score_surface, (x_position, y_position))

        main_menu_button.update(screen)
        play_again_button.update(screen)
        
        pygame.display.flip()
        clock.tick(30)
        
main_menu(difficulty_data)