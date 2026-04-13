from pygame import *
import sys


init()

window = display.set_mode((1200, 600))
clock = time.Clock()
running = True

# posicao da nuvem, vai ser atualizada no loop
nuvem_x = 350


def desenha_ceu():
    window.fill((151, 209, 250))

def desenha_sol():
    draw.circle(window, (255, 220, 0), (110, 95), 55)

def desenha_nuvem(x):
    draw.circle(window, (255, 255, 255), (x,      115), 38)
    draw.circle(window, (255, 255, 255), (x + 48, 100), 48)
    draw.circle(window, (255, 255, 255), (x + 95, 112), 40)
    draw.circle(window, (255, 255, 255), (x + 55, 125), 32)

def desenha_chao():
    draw.rect(window, (72, 157, 37), Rect(0, 500, window.get_width(), 100))

def desenha_casa():
    # paredes
    draw.rect(window, (85, 85, 95), Rect(330, 355, 240, 150))
    # telhado
    draw.polygon(window, (185, 95, 35), [(310, 358), (450, 230), (590, 358)])
    # porta
    draw.rect(window, (45, 32, 28), Rect(418, 435, 55, 72))
    # janela esquerda
    draw.rect(window, (75, 115, 195), Rect(345, 385, 52, 48))

def desenha_arvore():
    draw.rect(window, (105, 62, 22), Rect(760, 400, 28, 105))
    draw.circle(window, (58, 138, 32), (774, 375), 75)

def desenha_grama_detalhe():
    # faixinha mais escura na borda do chao
    draw.rect(window, (55, 130, 28), Rect(0, 500, window.get_width(), 12))


batman_img = image.load("./casinha_batman/batman.png")
batman_img = transform.scale(batman_img, (110, 110))

batman_font = font.Font("./casinha_batman/batmfa__.ttf", 38)
batman_text = batman_font.render("I am Batman", True, (0, 0, 0))

mixer.music.load("./casinha_batman/batman_1966.mp3")
mixer.music.play(-1)


while running:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

    desenha_ceu()
    desenha_sol()
    desenha_nuvem(nuvem_x)
    desenha_chao()
    desenha_grama_detalhe()
    desenha_casa()
    desenha_arvore()

    window.blit(batman_img, (960, 380))
    window.blit(batman_text, (880, 540))

    # nuvem anda pra direita, quando sai teletransporta pro inicio
    nuvem_x += 2
    if nuvem_x > window.get_width() + 120:
        nuvem_x = -130

    display.update()
    clock.tick(60)
