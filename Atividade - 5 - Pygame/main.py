from pygame import *
from pygame.locals import QUIT
import sys 


# Estrutura inicial do pygame, montagem da tela inicial

init()

window = display.set_mode((1200,600))
running = True

window.fill((151, 209, 250))

# No pygame o x cresce para a direita e y para baixo, tudo é a partir do canto superior
# esquerdo

def desenha_chao():
    chao = Rect((0,500,window.get_width(),100))
    draw.rect(window,(72, 157, 37),chao)

def desenha_arvore():
    draw.circle(window,(72, 157, 37),(500,600), 200)

def desenha_triangulo():
    draw.polygon(window,(0,255,0), [(200,300), (250,150), (300,300)])


while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

    # Desenha-se a partir daqui

    # Desenha chao
   
    desenha_chao()
    desenha_arvore()
    desenha_triangulo()
    display.update()








# Desenho da casa

def desenha_casa(lado):
    draw.rect(window,)
