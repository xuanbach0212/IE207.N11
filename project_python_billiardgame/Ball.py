import pygame
class Ball (object):
    def __init__(self, colour, x, y, img_name):
        self.colour = colour
        self.x = x
        self.y = y
        ball_Img = pygame.image.load(img_name).convert_alpha()
        self.sprite = pygame.transform.scale(ball_Img,(36,36))
        self.movement_direction = 0
        self.speed = 0
        self.frames = 0
        self.potted = False
        self.collision_monitor = []
        for i in range(16):
            self.collision_monitor.append(False)