
import pygame
import sys
from config import *
from pool_table import *
from Player import *
pygame.init()


def draw_text_menu(text,color,surface,x,y):
    textobj = menuFont.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surface.blit(textobj,textrect)
click = False
def menu():
    while True:
        gameDisplay.fill((0,130,0))
        draw_text_menu("Billiard Game Project",(255,255,255),gameDisplay,700,100)
        play_button_8 = pygame.Rect(550,200,300,100)
        play_button_9 = pygame.Rect(550,350,300,100)
        quit_button = pygame.Rect(550,500,300,100)
        
        mx,my = pygame.mouse.get_pos()
        
        if play_button_8.collidepoint((mx,my)):
            if click:
                exec(open('8_Balls_play.py').read())
        if play_button_9.collidepoint((mx,my)):
            if click:
                exec(open('9_Balls_play.py').read())
        if quit_button.collidepoint((mx,my)):
            if click:
                pygame.quit()
                sys.exit()

        play_button_draw= pygame.draw.rect(gameDisplay,(0,100,0),play_button_8)
        play_button_draw= pygame.draw.rect(gameDisplay,(0,100,0),play_button_9)
        play_button_text = draw_text_menu("8 Balls",(255,255,255),gameDisplay,700,250)
        play_button_text = draw_text_menu("9 Balls",(255,255,255),gameDisplay,700,400)
        quit_button_draw = pygame.draw.rect(gameDisplay,(0,100,0),quit_button)
        quit_button_text = draw_text_menu("QUIT",(255,255,255),gameDisplay,700,550)
        click = False
        for event in pygame.event.get():    
            if event.type== pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
menu()

