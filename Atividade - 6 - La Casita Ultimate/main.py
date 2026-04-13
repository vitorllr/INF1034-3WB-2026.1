import pygame
from pygame import key
from pygame import K_d,K_a

pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True
clock = pygame.time.Clock()

fonte = pygame.font.Font("batmfa__.ttf", 50)
image = pygame.image.load("batman.png")
image = pygame.transform.scale(image, (200, 200))
pygame.mixer.music.load("batman_1966.mp3")
pygame.mixer.music.play(-1)

timer = 0


#Definir Variaveis 

pos_x_nuvem = 300

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ## Update - diferenca de tempo entre um frame e o outro
    keys = key.get_pressed()
    #Se eu pressionar a tecla D entao 
    if keys[K_d]:
        pos_x_nuvem = pos_x_nuvem + 100 * dt
    elif keys[K_a]: 
        pos_x_nuvem = pos_x_nuvem - 100 * dt
    #keys = key.get_pressed()
    dt = clock.get_time()/1000
    pos_x_nuvem = pos_x_nuvem + 100 * dt
    if pos_x_nuvem == screen.get_width():
        pos_x_nuvem =  pos_x_nuvem - 100 * dt
    #dt garante que a mov sera proporcional ao fps que esta rodando
    # Quantos s tenho de diferenca d
    timer = timer + dt


    ##Draw
    screen.fill("#97D1FA")
    pygame.draw.rect(screen, "#0D1664", (100, 200, 200, 50))
    pygame.draw.circle(screen, "#FFF251", (80, 80), 50)
    pygame.draw.polygon(screen, "#F2883B", [(400, 300), (450, 300), (425, 250)])
    pygame.draw.line(screen, "#FFF251", (10, 150), (100, 20), 4)

    
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+70, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+140, 80), 50)
    pygame.draw.circle(screen, "#FFFFFF", (pos_x_nuvem+210, 80), 50)


    screen.blit(image, (500, 300))

    steve_text = fonte.render("I am BATMAN!", True, "#000000")
    screen.blit(steve_text, (500, 250))

    pygame.display.update()



#