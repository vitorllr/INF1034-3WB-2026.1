import pygame
from pygame import key
from pygame import *
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True
clock = pygame.time.Clock()

fonte = pygame.font.Font("batmfa__.ttf", 50)
image = pygame.image.load("batman.png")
image = pygame.transform.scale(image, (200, 200))
pygame.mixer.music.load("batman_1966.mp3")
# pygame.mixer.music.play(-1)

timer = 0


#Definir Variaveis 
# Nuvem
pos_x_nuvem = 300
background_color = "#97D1FA"
velocidade_nuvem = 400

# Sol
pos_sol = (300,300)
comprimento_raio = 100
angulos_raios = [0, 45, 90, 135, 180, 225, 270, 315]
# velocidade_sol = pygame.mouse.get_rel()

def movimento_nuvem(pos,vel):
    if pos + 260 > screen.get_width() :
        vel = -vel
    if pos < 50:
        vel = -vel
    return pos, vel

def muda_cor_do_background(pos_sol, background_color):
    if pos_sol[0] + 50 < screen.get_width()/3:
        background_color = "#97D1FA"
    elif pos_sol[0] + 50 > 2*(screen.get_width()/3) :
        background_color = (40,86,133)
    else:
        background_color = (203,90,11)
    return background_color

    
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #diferente do key, esse KEYDOWN é uma ação instantanea
            key_pressed = event.key
            if key_pressed == K_SPACE and background_color == "#97D1FA":
                background_color = (255,174,64)
            elif key_pressed == K_SPACE and background_color == (255,174,64):
                background_color = "#97D1FA"
          

    ## Update - diferenca de tempo entre um frame e o outro
    dt = clock.get_time()/1000
    keys = key.get_pressed()
    #Se eu pressionar a tecla D entao
    if keys[K_d]:
        pos_x_nuvem = pos_x_nuvem + 100 * dt
    elif keys[K_a]:
        pos_x_nuvem = pos_x_nuvem - 100 * dt

    #dt garante que a mov sera proporcional ao fps que esta rodando
    timer = timer + dt

    pos_x_nuvem += velocidade_nuvem * dt
    
    

    ##Draw
    screen.fill(background_color)
    pygame.draw.rect(screen, "#0D1664", (100, 200, 200, 50))
    pygame.draw.circle(screen, "#FFF251", (pos_sol), 50)
    pygame.draw.polygon(screen, "#F2883B", [(400, 300), (450, 300), (425, 250)])
    
    for grau in angulos_raios:
        rad = math.radians(grau)
        dx = math.cos(rad) * comprimento_raio
        dy = math.sin(rad) * comprimento_raio
        pygame.draw.line(screen, "#FFF251", pos_sol, (pos_sol[0] + dx, pos_sol[1] + dy), 4)
   
    

    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+70, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+140, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+210, 80), 50)

    pos_x_nuvem, velocidade_nuvem = movimento_nuvem(pos_x_nuvem, velocidade_nuvem)  
    pos_sol = (pygame.mouse.get_pos())   
    background_color = muda_cor_do_background(pos_sol, background_color)   

    screen.blit(image, (500, 300))

    steve_text = fonte.render("I am BATMAN!", True, "#000000")
    screen.blit(steve_text, (500, 250))

    pygame.display.update()



