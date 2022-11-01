import pygame
import math
import time
import sys
from Player import *
from pool_table import *
from gameState import *
from config import *
from Collision import *
from Ball import *

pygame.init()

def draw_background():
    gameDisplay.fill(WHITE)
    pygame.draw.rect(gameDisplay, FELT, (200, 150, 1000, 500))
    for wall in walls: 
        pygame.draw.rect(gameDisplay, OAK, wall)
    for hole in holes: 
        pygame.draw.circle(gameDisplay, BLACK, hole, 22)
    p1_colour = player_1.colour
    p2_colour = player_2.colour
    gameDisplay.blit(mainFont.render('PLAYER 1', 1, BLACK), (20, 10))
    gameDisplay.blit(mainFont.render(p1_colour.upper(), 1, BLACK), (20, 50))
    gameDisplay.blit(mainFont.render('PLAYER 2', 1, BLACK), (1260, 10))
    gameDisplay.blit(mainFont.render(p2_colour.upper(), 1, BLACK), (1260, 50))
    gameDisplay.blit(mainFont.render('PLAYER ' + str(player_turn.number) + '\'S TURN', 1, RED), (600, 10))

def game_over():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_background()
        for b in balls:
            if not b.potted:
                gameDisplay.blit(b.sprite, (b.x - 18, b.y - 18))
        gameDisplay.blit(mainFont.render('PLAYER ' + str(winner.colour) + ' WINS!', 1, RED), (615, 390))
        pygame.display.update()


winner = None
while winner is None:
    draw_background()
    draw_potted_balls()
    for ball in balls:
        if not ball.potted:
            gameDisplay.blit(ball.sprite, (ball.x - 18, ball.y - 18))
            if in_play:
                if ball.speed > 0:
                    for i in range(int(ball.speed)):
                        if ball.y - 18 <= 150 or ball.y + 18 >= 650 or ball.x + 18 >= 1200 or ball.x - 18 <= 200:
                            hit_sound.play()
                            if ball.speed > 1:  
                                ball.speed -= 1
                            ball.movement_direction = collision_with_wall(
                                ball.x, ball.y, ball.movement_direction)
                            collision_monitor_reset()
                        ball.x, ball.y = angle_to_coordinates(
                            ball.x, ball.y, ball.movement_direction, 1)
                    if ball_potted(ball.x, ball.y):  
                        sunk_sound.play()
                        recent_potted_balls.append(ball)
                        potted_balls.append(ball)
                        ball.potted = True
                        
                    ball_collided_with = check_collision_with_other_ball(
                        ball.x, ball.y, ball)
                    if ball_collided_with is not None:  
                        hit_sound.play()
                        if first_ball_collided_with is None:  
                            first_ball_collided_with = ball_collided_with
                        ball.movement_direction, ball_collided_with.movement_direction, ball.speed, ball_collided_with.speed = ball_collision_physics(
                            ball.x, ball.y, ball_collided_with.x, ball_collided_with.y, ball.movement_direction, ball.speed)
                        collision_monitor_reset()
                        ball.collision_monitor[balls.index(
                            ball_collided_with)] = True
                        ball_collided_with.collision_monitor[balls.index(
                            ball)] = True

                    # ma sat
                    if ball.frames >= (-30) * math.log10(0.05 * (ball.speed + 1)):
                        ball.speed -= 1
                        ball.frames = 0
                    ball.frames += 1

                    if ball is cue_ball:
                        pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)
               
                if balls_stopped():
                    draw_background()
                    draw_potted_balls()
                    for ball in balls:
                        if not ball.potted:
                            gameDisplay.blit(
                                ball.sprite, (ball.x - 18, ball.y - 18))
                    pygame.display.update()
                    time.sleep(0.5)

                    
                    # kiem tra bong vao lo
                    stripes, solids = 0, 0
                    for ball in recent_potted_balls:
                        if ball.colour == 'stripes':
                            stripes += 1
                            if initial_break:
                                initial_break = False
                                turn_change = False
                                if player_turn.number == 1:
                                    player_1.colour = 'stripes'
                                    player_2.colour = 'solids'
                                elif player_turn.number == 2:
                                    player_2.colour = 'stripes'
                                    player_1.colour = 'solids'
                        elif ball.colour == 'solids':
                            solids += 1
                            if initial_break:
                                initial_break = False
                                turn_change = False
                                if player_turn.number == 1:
                                    player_1.colour = 'solids'
                                    player_2.colour = 'stripes'
                                elif player_turn.number == 2:
                                    player_2.colour = 'solids'
                                    player_1.colour = 'stripes'
                        elif ball.colour == 'eight':
                            if player_turn.only_eight_ball_left:
                                if cue_ball.potted or not first_ball_collided_with.colour == 'eight':
                                    if player_turn.number == 1:
                                        winner = player_2
                                    else:
                                        winner = player_1
                                else:
                                    winner = player_turn
                            else:
                                if player_turn.number == 1:
                                    winner = player_2
                                else:
                                    winner = player_1
                            game_over()
                    recent_potted_balls[:] = []

                    # kiem tra doi turn 
                    if player_turn.only_eight_ball_left:
                        turn_change = True
                        cue_ball_in_hand = False
                        if first_ball_collided_with is not None:
                            if not first_ball_collided_with.colour == 'eight':
                                cue_ball_in_hand = True
                        else:
                            cue_ball_in_hand = True
                    else:
                        if player_turn.colour == 'stripes':
                            if stripes > 0:
                                turn_change = False
                            else:
                                turn_change = True
                        elif player_turn.colour == 'solids':
                            if solids > 0:
                                turn_change = False
                            else:
                                turn_change = True
                        if first_ball_collided_with is not None:
                            if player_turn.colour == 'stripes' and not first_ball_collided_with.colour == 'stripes':
                                turn_change = True
                                cue_ball_in_hand = True
                            elif player_turn.colour == 'solids' and not first_ball_collided_with.colour == 'solids':
                                turn_change = True
                                cue_ball_in_hand = True
                        else:
                            turn_change = True
                            cue_ball_in_hand = True
                        if number_of_balls_potted(player_turn.colour) == 7:
                            player_turn.only_eight_ball_left = True
                    first_ball_collided_with = None
                    if cue_ball.potted:
                        potted_balls.remove(cue_ball)
                        turn_change = True
                        cue_ball.potted = False
                        cue_ball_in_hand = True

                    if turn_change:
                        player_turn = player_turn_switch(player_turn)
                    if cue_ball_in_hand:
                        ball_in_hand()
                        pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)
                        cue_ball_in_hand = False

                    in_play = False

    # AIMING 
    if not in_play:
        if draw_guide:
            pygame.draw.line(gameDisplay, WHITE, (cue_ball.x,
                             cue_ball.y), mouse_hold_coords, 2)
            gameDisplay.blit(pool_cue_rotated, pool_cue_coords)
            pygame.draw.circle(gameDisplay, WHITE, mouse_hold_coords, 16, 1)

        # ve stick
        if mouse_held:
            mouseX, mouseY = pygame.mouse.get_pos(
            )[0], pygame.mouse.get_pos()[1]
            temporary_angle = cue_direction + 180
            if temporary_angle > 360:
                temporary_angle -= 360
            strike_distance = distance_between_points(
                mouse_hold_coords[0], mouse_hold_coords[1], mouseX, mouseY)
            if strike_distance > 210:
                strike_distance = 210
            pool_cue_coords = angle_to_coordinates(
                cue_ball.x - 462, cue_ball.y - 450, temporary_angle, strike_distance)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not in_play:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_hold_coords = pygame.mouse.get_pos()
                mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
                if strike_distance > 16:
                    cue_ball.speed = round((strike_distance - 16)/16)
                    in_play = True
                    draw_guide = False
                    strike_sound.play()
                cue_ball.movement_direction = cue_direction
                collision_monitor_reset()
            elif event.type == pygame.MOUSEMOTION and mouse_held is False:
                draw_guide = True
                mouseX, mouseY = pygame.mouse.get_pos(
                )[0], pygame.mouse.get_pos()[1]
                mouse_hold_coords = mouseX, mouseY
                cue_direction = coordinates_to_angle(
                    cue_ball.x, cue_ball.y, mouseX, mouseY)
                pool_cue_rotated = rot_center(pool_cue_original, cue_direction)
                pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)
    pygame.display.update()
    clock.tick(90)
