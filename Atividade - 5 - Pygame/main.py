from pygame import *
from pygame.locals import QUIT
import sys 


# Estrutura inicial do pygame, montagem da tela inicial + loop depois das Fs

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

def desenha_casa(lado):
    draw.rect(window,)

draw.line(window, (255,0,255), (100,100), (200,200), 6)
# def desenha_poligonos_nao_regulares():

# insercao de recursos 

    # Carregar a imagem no programa e diminuir proporcionalmente
batman_img = image.load("batman.png")
batman_img = transform.scale(batman_img, (200,200))

    # Imprimir na tela a imagem
window.blit(batman_img,(0,0))

# carregando font 
batman_font = font.Font("batmfa__.ttf",50) 

#desenhar texto 
batman_text = batman_font.render("I am Batman", True, (0,0,0))
window.blit(batman_text, (0,0))

# Inserir som (nao inserir no loop)
batman_sound = mixer.music.load("batman_1966.mp3")
mixer.music.play(-1) #loop ate o fim, sem nada roda uma vez

while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

    # Desenha-se a partir daqui

    desenha_chao()
    desenha_arvore()
    desenha_triangulo()

    display.update()

#apagar comment