import pygame
import math
import time
import sys
from pool_table import *
from gameState import *
from config import *
from Collision import *
from Ball import *
from Player import *

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

def game_over_9():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_background()
        for b in balls_9: 
            if not b.potted:
                gameDisplay.blit(b.sprite, (b.x - 18, b.y - 18))
        gameDisplay.blit(mainFont.render('PLAYER ' + str(winner.number) + ' WINS!', 1, RED), (615, 390))
        pygame.display.update()
        

while winner is None:
    draw_background()
    draw_potted_balls()
    for ball in balls_9:
        if not ball.potted:
            gameDisplay.blit(ball.sprite, (ball.x - 18, ball.y - 18))
            if in_play:
                if ball.speed > 0:
                    for i in range(int(ball.speed)):
                        # checks collides with a wall
                        if ball.y - 18 <= 150 or ball.y + 18 >= 650 or ball.x + 18 >= 1200 or ball.x - 18 <= 200:
                            hit_sound.play()
                            if ball.speed > 1: # ball loses speed
                                ball.speed -= 1
                            ball.movement_direction = collision_with_wall(ball.x, ball.y, ball.movement_direction)
                            collision_monitor_reset_9()
                        ball.x, ball.y = angle_to_coordinates(ball.x, ball.y, ball.movement_direction, 1)
                    if ball_potted(ball.x, ball.y):
                        sunk_sound.play()
                        recent_potted_balls.append(ball)
                        potted_balls.append(ball)
                        ball.potted = True
                    

                    ball_collided_with = check_collision_with_other_ball_9(ball.x, ball.y, ball)
                    if ball_collided_with is not None:
                        hit_sound.play()
                        if first_ball_collided_with is None:
                            first_ball_collided_with = ball_collided_with
                        ball.movement_direction, ball_collided_with.movement_direction, ball.speed, ball_collided_with.speed = ball_collision_physics(ball.x, ball.y, ball_collided_with.x, ball_collided_with.y, ball.movement_direction, ball.speed)
                        collision_monitor_reset_9() 

                        ball.collision_monitor[balls_9.index(ball_collided_with)] = True
                        ball_collided_with.collision_monitor[balls_9.index(ball)] = True

                    # FRICTION
            
                    # decreases speed 
                    if ball.frames >= (-30) * math.log10(0.05 * (ball.speed + 1)):
                        ball.speed -= 1
                        ball.frames = 0
                    ball.frames += 1
                    # updates the coordinates 
                    if ball is cue_ball:
                        pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)
                # if ball stop
                if balls_stopped_9():
                    draw_background()
                    draw_potted_balls()
                    for ball in balls_9:
                        if not ball.potted:
                            gameDisplay.blit(ball.sprite, (ball.x - 18, ball.y - 18))
                    pygame.display.update()
                    time.sleep(0.25)
                    


                    if player_turn.only_nine_ball_left:
                        turn_change = True # doi turn khi bi 9 vao``
                        cue_ball_in_hand = False
                        if first_ball_collided_with is not None: 
                            if not first_ball_collided_with.colour == 'nine':
                                cue_ball_in_hand = True
                        else:
                            cue_ball_in_hand = True
                    else :  
                        if first_ball_collided_with is not None:
                            if not first_ball_collided_with.colour == recent_balls_9[0] :
                                cue_ball_in_hand = True
                                turn_change = True
                            elif first_ball_collided_with.colour == recent_balls_9[0]:
                                    if check_collision_recent_ball_9 == 1:
                                        turn_change = True
                        else:
                            turn_change = True
                            cue_ball_in_hand = True
                   
                    
                    # CHECKS POTTED BALLS AFTER EACH TURN
                    
                    for ball in recent_potted_balls:
                        if ball.colour == recent_balls_9[0] and ball.colour != "" and ball.colour != "nine":
                            turn_change = False
                            cue_ball_in_hand = False
                            recent_balls_9.remove(ball.colour)

                        elif ball.colour != recent_balls_9[0] and ball.colour != "" and ball.colour != "nine":
                            if first_ball_collided_with.colour == recent_balls_9[0] and check_collision_recent_ball_9 == False:
                                turn_change = False
                                cue_ball_in_hand = False
                                recent_balls_9.remove(ball.colour)
                                check_collision_recent_ball_9 = True
                            else:
                                turn_change = True
                                recent_balls_9.remove(ball.colour)
                                cue_ball_in_hand = True
                    
                        elif ball.colour == "nine" :
                            if len(recent_balls_9) == 9:
                                if first_ball_collided_with.colour == recent_balls_9[0]:
                                    winner = player_turn
                                    
                                elif first_ball_collided_with.colour == "nine":
                                    if player_turn == 1:
                                        winner = player_2
                                        
                                    else:
                                        winner = player_1
                               
                            if len(recent_balls_9) > 1:
                                if player_turn.only_nine_ball_left:
                                    if cue_ball.potted or not first_ball_collided_with.colour == "nine":
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
                                
                            game_over_9()       

                    recent_potted_balls[:] = []
                    
                    first_ball_collided_with = None
                    # if cue ball is potted
                    if cue_ball.potted:
                        potted_balls.remove(cue_ball)
                        turn_change = True
                        cue_ball.potted = False
                        cue_ball_in_hand = True

                    # change turn
                    if turn_change:
                        player_turn = player_turn_switch(player_turn)

                    if cue_ball_in_hand:
                        ball_in_hand_9()
                        pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)
                        cue_ball_in_hand = False

                    
                    in_play = False

    # AIMING AND STRIKING THE CUE BALL
    if not in_play:
        if draw_guide:
            pygame.draw.line(gameDisplay, WHITE, (cue_ball.x, cue_ball.y), mouse_hold_coords, 2)
            gameDisplay.blit(pool_cue_rotated, pool_cue_coords)
            pygame.draw.circle(gameDisplay, WHITE, mouse_hold_coords, 16, 1)

        # DRAWING CUE
        if mouse_held:
            mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            # adjusts angle value if it is greater than 360
            temporary_angle = cue_direction + 180
            if temporary_angle > 360:
                temporary_angle -= 360
            strike_distance = distance_between_points(mouse_hold_coords[0], mouse_hold_coords[1], mouseX, mouseY)
            if strike_distance > 210:
                strike_distance = 210
            pool_cue_coords = angle_to_coordinates(cue_ball.x - 462, cue_ball.y - 450, temporary_angle, strike_distance)


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
                if strike_distance > 10:
                    cue_ball.speed = round((strike_distance - 10)/10)
                    in_play = True
                    draw_guide = False
                    strike_sound.play()
                cue_ball.movement_direction = cue_direction
                collision_monitor_reset_9()

            elif event.type == pygame.MOUSEMOTION and mouse_held is False:
                draw_guide = True
                mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                mouse_hold_coords = mouseX, mouseY
                cue_direction = coordinates_to_angle(cue_ball.x, cue_ball.y, mouseX, mouseY)
                pool_cue_rotated = rot_center(pool_cue_original, cue_direction)
                pool_cue_coords = (cue_ball.x - 462, cue_ball.y - 450)

    pygame.display.update()
    clock.tick(90)