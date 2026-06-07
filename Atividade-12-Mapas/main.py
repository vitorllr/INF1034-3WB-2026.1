import os

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 12 - Mapas")
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

SOLIDOS = {"r", "c", "m"}


def carrega_mapa():
    with open(MAPA_PATH) as arquivo:
        return [linha.rstrip("\n") for linha in arquivo if linha.strip()]


mapa = carrega_mapa()
MAPA_COLUNAS = len(mapa[0])
MAPA_LINHAS = len(mapa)
MAPA_LARGURA = MAPA_COLUNAS * TILE
MAPA_ALTURA = MAPA_LINHAS * TILE


folha_jogador = carrega_imagem("player-swiming.png")
NUM_FRAMES = 7
TAMANHO_JOGADOR = 64
frames_jogador = []
for indice in range(NUM_FRAMES):
    rect_frame = pygame.Rect(indice * 80, 0, 80, 80)
    sprite = folha_jogador.subsurface(rect_frame).copy()
    sprite = pygame.transform.scale(sprite, (TAMANHO_JOGADOR, TAMANHO_JOGADOR))
    frames_jogador.append(sprite)


jogador = {
    "x": 3 * TILE,
    "y": 3 * TILE,
    "direcao": "direita",
    "frame": 0.0,
    "andando": False,
}
VELOCIDADE = 220
VELOCIDADE_FRAME = 10
ANGULOS_DIRECAO = {"direita": 0, "cima": 90, "esquerda": 180, "baixo": -90}


def collider_jogador():
    return pygame.Rect(
        int(jogador["x"]) + 8,
        int(jogador["y"]) + 8,
        TAMANHO_JOGADOR - 16,
        TAMANHO_JOGADOR - 16,
    )


def colide_com_mapa():
    collider = collider_jogador()
    col_min = max(0, collider.left // TILE - 1)
    col_max = min(MAPA_COLUNAS - 1, collider.right // TILE + 1)
    lin_min = max(0, collider.top // TILE - 1)
    lin_max = min(MAPA_LINHAS - 1, collider.bottom // TILE + 1)
    for linha in range(lin_min, lin_max + 1):
        for coluna in range(col_min, col_max + 1):
            if mapa[linha][coluna] in SOLIDOS:
                tile_rect = pygame.Rect(coluna * TILE, linha * TILE, TILE, TILE)
                if collider.colliderect(tile_rect):
                    return True
    return False


def atualiza_jogador(delta_tempo, keys):
    old_pos_x = jogador["x"]
    old_pos_y = jogador["y"]

    direcao_x = 0
    direcao_y = 0
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direcao_x += 1
        jogador["direcao"] = "direita"
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direcao_x -= 1
        jogador["direcao"] = "esquerda"
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        direcao_y -= 1
        jogador["direcao"] = "cima"
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direcao_y += 1
        jogador["direcao"] = "baixo"

    jogador["andando"] = direcao_x != 0 or direcao_y != 0

    jogador["x"] += direcao_x * VELOCIDADE * delta_tempo
    if colide_com_mapa():
        jogador["x"] = old_pos_x

    jogador["y"] += direcao_y * VELOCIDADE * delta_tempo
    if colide_com_mapa():
        jogador["y"] = old_pos_y

    jogador["x"] = max(0, min(MAPA_LARGURA - TAMANHO_JOGADOR, jogador["x"]))
    jogador["y"] = max(0, min(MAPA_ALTURA - TAMANHO_JOGADOR, jogador["y"]))

    if jogador["andando"]:
        jogador["frame"] = (
            jogador["frame"] + VELOCIDADE_FRAME * delta_tempo
        ) % NUM_FRAMES
    else:
        jogador["frame"] = 0


def desenha_background(camera_x, camera_y):
    deslocamento_x = int(camera_x * 0.3) % BG_LARGURA
    deslocamento_y = int(camera_y * 0.3) % BG_ALTURA
    x = -deslocamento_x
    while x < LARGURA:
        y = -deslocamento_y
        while y < ALTURA:
            screen.blit(background, (x, y))
            y += BG_ALTURA
        x += BG_LARGURA


def desenha_mapa(camera_x, camera_y):
    col_min = max(0, camera_x // TILE)
    col_max = min(MAPA_COLUNAS, (camera_x + LARGURA) // TILE + 1)
    lin_min = max(0, camera_y // TILE)
    lin_max = min(MAPA_LINHAS, (camera_y + ALTURA) // TILE + 1)
    for linha in range(lin_min, lin_max):
        for coluna in range(col_min, col_max):
            sprite_tile = TILES[mapa[linha][coluna]]
            if sprite_tile is not None:
                screen.blit(
                    sprite_tile,
                    (coluna * TILE - camera_x, linha * TILE - camera_y),
                )


def desenha_jogador(camera_x, camera_y):
    sprite = frames_jogador[int(jogador["frame"])]
    sprite = pygame.transform.rotate(sprite, ANGULOS_DIRECAO[jogador["direcao"]])
    screen.blit(
        sprite,
        (int(jogador["x"] - camera_x), int(jogador["y"] - camera_y)),
    )


running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    atualiza_jogador(delta_tempo, keys)

    camera_x = int(jogador["x"] + TAMANHO_JOGADOR // 2 - LARGURA // 2)
    camera_y = int(jogador["y"] + TAMANHO_JOGADOR // 2 - ALTURA // 2)
    camera_x = max(0, min(MAPA_LARGURA - LARGURA, camera_x))
    camera_y = max(0, min(MAPA_ALTURA - ALTURA, camera_y))

    desenha_background(camera_x, camera_y)
    desenha_mapa(camera_x, camera_y)
    desenha_jogador(camera_x, camera_y)

    dica = fonte.render("nada com setas ou WASD", True, (255, 255, 255))
    screen.blit(dica, (12, 12))

    pygame.display.update()
