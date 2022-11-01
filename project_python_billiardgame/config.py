import pygame
from Ball import *
from Player import *

pygame.mixer.init(44100, -16, 2, 64)
pygame.init()
# fonts
mainFont = pygame.font.SysFont("freesansbold.ttf", 30)
menuFont = pygame.font.SysFont("freesansbold.ttf", 80)
# sound
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
sunk_sound = pygame.mixer.Sound('sounds/sunk.ogg')
strike_sound = pygame.mixer.Sound('sounds/strike.wav')
# display
gameDisplay = pygame.display.set_mode((1400, 800))
pygame.display.set_caption('Billiard Game Project')
clock = pygame.time.Clock()

walls = (pygame.Rect(150, 100, 1100, 50), pygame.Rect(150, 650, 1100, 50), pygame.Rect(1200, 100, 50, 600), pygame.Rect(150, 100, 50, 600))
holes = ((210, 160), (700, 150), (1190, 160), (210, 640), (700, 650), (1190, 640))

# pool cue
pool_cue_original = pygame.image.load('images/cue.png').convert_alpha()
pool_cue_rotated = pygame.transform.rotate(pool_cue_original, 0)
pool_cue_coords = (0, 0)

# mouse
mouse_hold_coords = (0, 0)
mouse_held = False

# cue ball
cue_ball = Ball('', 450, 400, 'images/ball0.png')
cue_direction = 0


strike_distance = 0
draw_guide = True
in_play = False
# check stripes and solids was assigned
initial_break = True

# player
player_1, player_2 = Player(1, ''), Player(2, '')
player_turn = player_1

# some setting
cue_ball_in_hand = False
turn_change = True
first_ball_collided_with = None
winner = None


# list balls
balls = [cue_ball, Ball('solids', 915+6, 400, 'images/ball1.png'), Ball('solids', 915+36*2, 400+36, 'images/ball2.png'),# 950 - 36, 400
         Ball('solids', 915+36*4-6, 400+36, 'images/ball3.png'), Ball('solids', 915+36*4-6, 400-36*2, 'images/ball4.png'),
         Ball('solids', 915+36+3, 400-18, 'images/ball5.png'), Ball('solids', 915+36*3-3, 400+18*3, 'images/ball6.png'),
         Ball('solids', 915+36*3-3, 400-18*3, 'images/ball7.png'),
         Ball('eight', 915+36*2, 400, 'images/ball8.png'), Ball('stripes', 915+36*2, 400-36, 'images/ball9.png'),
         Ball('stripes', 915+36*3-3, 400+18, 'images/ball10.png'), Ball('stripes', 915+36*3-3, 400-18, 'images/ball11.png'),
         Ball('stripes', 915+36*4-6, 400+36*2, 'images/ball12.png'), Ball('stripes', 915+36*4-6, 400-36, 'images/ball13.png'),
         Ball('stripes', 915+36+3, 400+18, 'images/ball14.png'), Ball('stripes', 915+36*4-6, 400, 'images/ball15.png')
         ]
balls_9 = [cue_ball, Ball("one", 915+6, 400, 'images/ball1.png'), Ball("two", 915+36+3, 400-18, 'images/ball2.png'),# 950 - 36, 400
         Ball("three", 915+36+3, 400+18, 'images/ball3.png'), Ball("four", 915+36*2, 400+36, 'images/ball4.png'),
         Ball("five", 915+36*2, 400-36, 'images/ball5.png'), Ball("six", 915+36*3-3, 400-18, 'images/ball6.png'),
         Ball("seven", 915+36*3-3, 400+18, 'images/ball7.png'),
         Ball("eight", 915+36*4-6, 400, 'images/ball8.png'), Ball("nine", 915+36*2, 400, 'images/ball9.png')
]

recent_potted_balls = []
potted_balls = []
recent_balls_9 = ["one","two","three","four","five","six","seven","eight","nine"]

check_collision_recent_ball_9 = False

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FELT = (49, 185, 77)
OAK = (79, 36, 18)
RED = (255, 0, 0)

