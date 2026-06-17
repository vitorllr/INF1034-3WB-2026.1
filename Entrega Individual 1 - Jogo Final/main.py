import os

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Entrega 1 - Mapa e Sprites")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 22)

TILE = 64
MAPA_PATH = "mapa.txt"
ASSETS = "assets"


def carrega_imagem(nome):
    return pygame.image.load(os.path.join(ASSETS, nome)).convert_alpha()


background = carrega_imagem("background.png")
BG_LARGURA = background.get_width()
BG_ALTURA = background.get_height()


def recorte_escalado(folha, area, tamanho):
    pedaco = folha.subsurface(pygame.Rect(area)).copy()
    return pygame.transform.scale(pedaco, (tamanho, tamanho))


folha_tiles = carrega_imagem("tiles.png")
folha_props = carrega_imagem("props.png")
sprite_mina = carrega_imagem("mine.png")

TILES = {
    "w": None,
    "s": recorte_escalado(folha_tiles, (320, 80, 80, 80), TILE),
    "r": recorte_escalado(folha_tiles, (0, 0, 80, 80), TILE),
    "c": recorte_escalado(folha_props, (480, 320, 80, 80), TILE),
    "m": pygame.transform.scale(sprite_mina, (TILE, TILE)),
}


def recorte_prop(area):
    pedaco = folha_props.subsurface(pygame.Rect(area)).copy()
    largura, altura = pedaco.get_size()
    return pygame.transform.scale(pedaco, (largura * TILE // 80, altura * TILE // 80))


PROPS = {
    "ruina": recorte_prop((752, 70, 245, 186)),
    "arco": recorte_prop((177, 34, 198, 205)),
    "estatua": recorte_prop((432, 41, 92, 231)),
    "estatua_coral": recorte_prop((596, 41, 120, 231)),
    "pilar": recorte_prop((49, 95, 85, 98)),
    "kelp": recorte_prop((614, 317, 52, 67)),
    "coral": recorte_prop((514, 327, 48, 56)),
    "anemona": recorte_prop((434, 332, 46, 51)),
}


def carrega_mapa():
    with open(MAPA_PATH) as arquivo:
        return [linha.rstrip("\n") for linha in arquivo if linha.strip()]


mapa = carrega_mapa()
MAPA_COLUNAS = len(mapa[0])
MAPA_LINHAS = len(mapa)
MAPA_LARGURA = MAPA_COLUNAS * TILE
MAPA_ALTURA = MAPA_LINHAS * TILE
DESLOCAMENTO_Y = (ALTURA - MAPA_ALTURA) // 2

CHAO = (MAPA_LINHAS - 1) * TILE + DESLOCAMENTO_Y + 20
DECORACOES = [
    ("ruina", 1010),
    ("arco", 470),
    ("estatua", 250),
    ("estatua_coral", 712),
    ("pilar", 44),
    ("pilar", 952),
    ("kelp", 156),
    ("kelp", 856),
    ("coral", 636),
    ("coral", 1196),
    ("anemona", 372),
    ("anemona", 1108),
]


folha_jogador = carrega_imagem("player-swiming.png")
NUM_FRAMES_JOGADOR = 7
TAMANHO_JOGADOR = 64
frames_jogador = []
for indice in range(NUM_FRAMES_JOGADOR):
    rect_frame = pygame.Rect(indice * 80, 0, 80, 80)
    sprite = folha_jogador.subsurface(rect_frame).copy()
    sprite = pygame.transform.scale(sprite, (TAMANHO_JOGADOR, TAMANHO_JOGADOR))
    frames_jogador.append(sprite)


folha_peixe = carrega_imagem("fish-big.png")
NUM_FRAMES_PEIXE = 4
LARGURA_PEIXE = 96
ALTURA_PEIXE = 56
PEIXE_FRAME_FONTE = 54
frames_peixe = []
for indice in range(NUM_FRAMES_PEIXE):
    rect_frame = pygame.Rect(indice * PEIXE_FRAME_FONTE, 0, PEIXE_FRAME_FONTE, 49)
    sprite = folha_peixe.subsurface(rect_frame).copy()
    sprite = pygame.transform.scale(sprite, (LARGURA_PEIXE, ALTURA_PEIXE))
    frames_peixe.append(sprite)


VELOCIDADE_FRAME = 8
pos_jogador = (LARGURA // 2 - TAMANHO_JOGADOR // 2, ALTURA // 2 - TAMANHO_JOGADOR // 2)
pos_peixe = (840, 150)
frame_jogador = 0.0
frame_peixe = 0.0


def desenha_background():
    x = 0
    while x < LARGURA:
        y = 0
        while y < ALTURA:
            screen.blit(background, (x, y))
            y += BG_ALTURA
        x += BG_LARGURA


def desenha_mapa():
    for linha in range(MAPA_LINHAS):
        for coluna in range(MAPA_COLUNAS):
            sprite_tile = TILES[mapa[linha][coluna]]
            if sprite_tile is not None:
                screen.blit(
                    sprite_tile,
                    (coluna * TILE, linha * TILE + DESLOCAMENTO_Y),
                )


def desenha_decoracoes():
    for nome, x in DECORACOES:
        sprite = PROPS[nome]
        screen.blit(sprite, (x, CHAO - sprite.get_height()))


def desenha_jogador():
    screen.blit(frames_jogador[int(frame_jogador)], pos_jogador)


def desenha_peixe():
    screen.blit(frames_peixe[int(frame_peixe)], pos_peixe)


running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_jogador = (
        frame_jogador + VELOCIDADE_FRAME * delta_tempo
    ) % NUM_FRAMES_JOGADOR
    frame_peixe = (frame_peixe + 6 * delta_tempo) % NUM_FRAMES_PEIXE

    desenha_background()
    desenha_mapa()
    desenha_decoracoes()
    desenha_peixe()
    desenha_jogador()

    rotulo = fonte.render("Entrega 1 - mapa em tiles e sprites", True, (255, 255, 255))
    screen.blit(rotulo, (16, 12))

    pygame.display.update()
