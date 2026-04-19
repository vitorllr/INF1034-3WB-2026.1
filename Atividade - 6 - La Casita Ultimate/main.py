import pygame
from pygame import key
from pygame import *
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True
clock = pygame.time.Clock()


#Funcoes
def desenha_sol():
    pygame.draw.circle(screen, "#FFF251", pos_sol, 50)
    for grau in angulos_raios:
        rad = math.radians(grau)
        dx = math.cos(rad) * comprimento_raio
        dy = math.sin(rad) * comprimento_raio
        pygame.draw.line(screen, "#FFF251", pos_sol, (pos_sol[0] + dx, pos_sol[1] + dy), 4)

def desenha_nuvem(x):
    pygame.draw.circle(screen, "#FFFFFF", (x,       80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (x + 70,  80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (x + 140, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (x + 210, 80), 50)
    
def desenha_casa():
    pygame.draw.rect(screen, (85, 85, 95), pygame.Rect(330, 355, 240, 150))   # paredes
    pygame.draw.polygon(screen, (185, 95, 35), [(310, 358), (450, 230), (590, 358)])  # telhado
    pygame.draw.rect(screen, (45, 32, 28), pygame.Rect(418, 435, 55, 72))     # porta
    pygame.draw.rect(screen, (75, 115, 195), pygame.Rect(345, 385, 52, 48))   # janela

def desenha_chao():
    pygame.draw.rect(screen, (72, 157, 37), pygame.Rect(0, 500, screen.get_width(), 220))

def desenha_arvore():
    pygame.draw.rect(screen, (105, 62, 22), pygame.Rect(760, 400, 28, 105))   # tronco
    pygame.draw.circle(screen, (58, 138, 32), (774, 375), 75)                 # folhagem

def desenha_grama_detalhe():
    pygame.draw.rect(screen, (55, 130, 28), pygame.Rect(0, 500, screen.get_width(), 12))



fonte = pygame.font.Font("batmfa__.ttf", 50)
image = pygame.image.load("batman.png")
image = pygame.transform.scale(image, (200, 200))
pygame.mixer.music.load("batman_1966.mp3")
# pygame.mixer.music.play(-1)

timer = 0


#Definir Variaveis 
# Nuvem
pos_x_nuvem = 300
background_color = (151, 209, 250)
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

    
    s
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
          

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

    pos_sol = (
        pygame.math.clamp(pygame.mouse.get_pos()[0], 50, screen.get_width()  - 50),
        pygame.math.clamp(pygame.mouse.get_pos()[1], 50, screen.get_height() - 50)
    )
    largura = screen.get_width()
    # background_color = pegar_RGB(pos_sol)
    
    if pos_sol[0] < largura // 3:
        background_color = (151, 209, 250)   # dia
    elif pos_sol[0] < 2 * largura // 3:
        background_color = (255, 160, 80)    # tarde
    else:
        background_color = (20, 24, 82)      # noite

    ##Draw
    screen.fill(background_color)
    desenha_sol()                    
    desenha_nuvem(pos_x_nuvem)       
    desenha_chao()                   
    desenha_grama_detalhe()          
    desenha_casa()                   
    desenha_arvore()                 
    # screen.blit(image, (960, 300))   
    # screen.blit(texto, (900, 500))   

    pos_x_nuvem, velocidade_nuvem = movimento_nuvem(pos_x_nuvem, velocidade_nuvem)

    screen.blit(image, (500, 300))

    steve_text = fonte.render("I am BATMAN!", True, "#000000")
    screen.blit(steve_text, (500, 250))

    pygame.display.update()



