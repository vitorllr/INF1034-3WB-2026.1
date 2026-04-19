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

def movimento_nuvem(pos, vel):
    if pos + 260 > screen.get_width():
        vel = -vel
    if pos < 50:
        vel = -vel
    return pos, vel

def movimento_sol(pos_sol, velocidade_sol, estado_sol, dt, keys):
    sol_x, sol_y = pos_sol
    if estado_sol == "mouse":
        mouse_x, mouse_y = pygame.mouse.get_pos()
        sol_x = pygame.math.clamp(mouse_x, 50, screen.get_width()  - 50)
        sol_y = pygame.math.clamp(mouse_y, 50, screen.get_height() - 50)
    else:
        if keys[K_DOWN]:
            sol_y += velocidade_sol * dt
        if keys[K_UP]:
            sol_y -= velocidade_sol * dt
        if keys[K_RIGHT]:
            sol_x += velocidade_sol * dt
        if keys[K_LEFT]:
            sol_x -= velocidade_sol * dt
        sol_x = pygame.math.clamp(sol_x, 50, screen.get_width()  - 50)
        sol_y = pygame.math.clamp(sol_y, 50, screen.get_height() - 50)
    return (sol_x, sol_y)

def muda_RGB(pos_sol):
    pos_sol
    

def muda_cor_do_background(pos_sol):
    if pos_sol[0] < screen.get_width() // 3:
        return (151, 209, 250)   # dia
    elif pos_sol[0] < 2 * screen.get_width() // 3:
        return (255, 160, 80)    # tarde
    else:
        return (20, 24, 82)      # noite

def tocar_estagio_do_dia(pos_sol, estagio_atual):
    if pos_sol[0] < screen.get_width() // 3:
        novo_estagio = "manha"
    elif pos_sol[0] < 2 * screen.get_width() // 3:
        novo_estagio = "tarde"
    else:
        novo_estagio = "noite"
    if novo_estagio != estagio_atual:
        pygame.mixer.music.load(sons[novo_estagio])
        pygame.mixer.music.play(-1)
        return novo_estagio
    return estagio_atual



fonte = pygame.font.Font("gandalf.ttf", 50)
image = pygame.image.load("gandalf.jpeg")
image = pygame.transform.scale(image, (150, 150))

sons = {
    "manha": "som_manha.wav",
    "tarde":  "som_tarde.aiff",
    "noite":  "som_noite.wav"
}

timer = 0

#Definir Variaveis
# Nuvem
pos_x_nuvem = 300
velocidade_nuvem = 400

# Sol
pos_sol = (300, 300)
comprimento_raio = 100
angulos_raios = [0, 45, 90, 135, 180, 225, 270, 315]
estado_sol = "mouse"
velocidade_sol = 400
estagio_atual = ""

#Background Desafio
background_color_inicial = pygame.Color(151, 209, 250)
background_color_final = pygame.Color(20, 24, 82)


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_pressed = event.key
            if key_pressed == K_DOWN or key_pressed == K_UP or key_pressed == K_RIGHT or key_pressed == K_LEFT:
                estado_sol = "keyboard"
        if event.type == pygame.MOUSEBUTTONDOWN:
            estado_sol = "mouse"
            tocar_estagio_do_dia(pos_sol,estagio_atual)

    ## Update
    dt = clock.get_time() / 1000
    keys = key.get_pressed()

    if keys[K_d]:
        pos_x_nuvem += 100 * dt
    elif keys[K_a]:
        pos_x_nuvem -= 100 * dt

    timer += dt
    pos_x_nuvem += velocidade_nuvem * dt
    pos_x_nuvem, velocidade_nuvem = movimento_nuvem(pos_x_nuvem, velocidade_nuvem)

    pos_sol = movimento_sol(pos_sol, velocidade_sol, estado_sol, dt, keys)
    background_color = muda_cor_do_background(pos_sol)
    
    # estagio_atual = tocar_estagio_do_dia(pos_sol, estagio_atual)
    
    fator = pos_sol[0] / screen.get_width()
    cor_atual = background_color_inicial.lerp(background_color_final, fator)

    ##Draw
    screen.fill(cor_atual)
    desenha_sol()
    desenha_nuvem(pos_x_nuvem)
    desenha_chao()
    desenha_grama_detalhe()
    desenha_casa()
    desenha_arvore()

    screen.blit(image, (1100, 300))
    steve_text = fonte.render("You shall not pass!!", True, "#000000")
    screen.blit(steve_text, (1000, 200))

    pygame.display.update()
