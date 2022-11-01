import pygame
from config import *

def draw_background():
    gameDisplay.fill(WHITE)
    pygame.draw.rect(gameDisplay, FELT, (200, 150, 1000, 500))
    for wall in walls: pygame.draw.rect(gameDisplay, OAK, wall)
    for hole in holes: pygame.draw.circle(gameDisplay, BLACK, hole, 22)
    p1_colour = player_1.colour
    p2_colour = player_2.colour
    gameDisplay.blit(mainFont.render('PLAYER 1', 1, BLACK), (20, 10))
    gameDisplay.blit(mainFont.render(p1_colour.upper(), 1, BLACK), (20, 50))
    gameDisplay.blit(mainFont.render('PLAYER 2', 1, BLACK), (1260, 10))
    gameDisplay.blit(mainFont.render(p2_colour.upper(), 1, BLACK), (1260, 50))
    gameDisplay.blit(mainFont.render('PLAYER ' + str(player_turn.number) + '\'S TURN', 1, RED), (600, 10))