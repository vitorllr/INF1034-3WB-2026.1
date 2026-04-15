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
estado_sol = "mouse"
velocidade_sol = 400
keys = pygame.key.get_pressed()


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

def movimento_sol(pos_sol, velocidade_sol, estado_sol, dt, keys):
    sol_x, sol_y = pos_sol
    if estado_sol == "mouse":  
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        
        # Trava no eixo X 
        if mouse_x < 50:
            sol_x = 50
        elif mouse_x > screen.get_width() - 50:
            sol_x = screen.get_width() - 50
        else:
            sol_x = mouse_x # Se não estourar o limite, usa a pos do mouse
            
         # Trava no eixo Y 
        if mouse_y < 50:
            sol_y = 50
        elif mouse_y > screen.get_height() - 50:
            sol_y = screen.get_height() - 50
        else:
            sol_y = mouse_y # Se não estourar o limite, usa a pos do mouse
            
        return (sol_x, sol_y)
    else:
        if keys[K_DOWN]:
            sol_y += velocidade_sol * dt
        if keys[K_UP]:
            sol_y -= velocidade_sol * dt
        if keys[K_RIGHT]:
            sol_x += velocidade_sol * dt
        if  keys[K_LEFT]:
            sol_x -= velocidade_sol * dt 
        # Trava no eixo X 
        if sol_x < 50:
            sol_x = 50
        elif sol_x > screen.get_width() - 50:
            sol_x = screen.get_width() - 50

        # Trava no eixo Y 
        if sol_y < 50:
            sol_y = 50
        elif sol_y > screen.get_height() - 50:
            sol_y = screen.get_height() - 50

        return (sol_x,sol_y)
    
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
            elif key_pressed == K_DOWN or key_pressed == K_UP or key_pressed == K_RIGHT or key_pressed == K_LEFT:
                estado_sol = "keyboard"
        if event.type == pygame.MOUSEBUTTONDOWN:
            estado_sol = "mouse"

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
    pos_sol = movimento_sol(pos_sol, velocidade_sol, estado_sol, dt, keys)

    background_color = muda_cor_do_background(pos_sol, background_color)   

    screen.blit(image, (500, 300))

    steve_text = fonte.render("I am BATMAN!", True, "#000000")
    screen.blit(steve_text, (500, 250))

    pygame.display.update()



