import pygame
from PIL import Image
import time
import sys
import random

pygame.init()

screen = pygame.display.set_mode((1200, 600))
icon_image = pygame.image.load('img/icn.png')
icon_image = pygame.transform.smoothscale(icon_image, (64, 64)).convert_alpha() 
pygame.display.set_icon(icon_image)
pygame.display.set_caption("THE SKY")
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/ring-matrix/RingMatrix.ttf', 50)
th_cloud = pygame.image.load('img/thundercloud.webp').convert_alpha()
th_cloud.set_colorkey((255, 255, 255))
jet = pygame.image.load("img/jet.png")


game_active = True
th_cloud_list = []
cloud_spawn_timer = 0

def get_cloud_rect(exclusion_rect, max_retries=10):
    for _ in range(max_retries):
        spawn_x = random.randint(0, 1100)
        spawn_y = random.randint(0, 500)
        th_cloud_surface = pygame.transform.smoothscale(th_cloud, (100, 100)).convert_alpha()
        th_cloud_rect = th_cloud_surface.get_rect(topleft=(spawn_x, spawn_y))
        if not exclusion_rect.colliderect(th_cloud_rect):
            th_cloud_list.append(th_cloud_rect)
            return th_cloud_rect
    return None

Sky_surface = pygame.image.load('img/bg.jpg').convert_alpha()
text_surface = test_font.render('THE SKY', True, (0, 0, 0)).convert_alpha()
jet_surface = pygame.transform.smoothscale(jet, (225, 80)).convert_alpha()
jet_rect = jet_surface.get_rect(topleft=(1200, 260))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     
            pygame.quit()
            sys.exit()
     
    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            jet_rect.y -= 5
        if keys[pygame.K_DOWN]:
            jet_rect.y += 5
             
        if jet_rect.y < -150:
            jet_rect.y = 600
        elif jet_rect.y > 600:
            jet_rect.y = -150

        if jet_rect.x < -300:
            jet_rect.x = 1200
        else:
            jet_rect.x -= 5
        
        cloud_spawn_timer += 1
        if cloud_spawn_timer >= 60:  
            get_cloud_rect(jet_rect)
            cloud_spawn_timer = 0

        if len(th_cloud_list) > 7:
            del th_cloud_list[0]

    screen.blit(Sky_surface, (-100, -250))
    screen.blit(text_surface, (400, 50))
    screen.blit(jet_surface, jet_rect)

    for i in th_cloud_list:
        screen.blit(pygame.transform.smoothscale(th_cloud, (100, 100)), i)
        if jet_rect.collidepoint(i.center):
            game_active = False
            lost_text = test_font.render('YOU LOST', True, (255, 0, 0)).convert_alpha()
            screen.blit(lost_text, (400, 250))
    pygame.display.update()
    clock.tick(60)
