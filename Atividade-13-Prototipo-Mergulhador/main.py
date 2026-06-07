# ANOTACOES DE AULA
# desenhando mapas em tiles, dividindo a tela em varios pedacinhos
# o tamanho do tile e mudado para altura e largura
#
# trabalhando com o for aninhado para fazer uma matriz
# usando tilesets para colocar ao inves de cores simples,
# usando um dict para fazer os recortes de cada fundo
# O tamanho do tileset sera 64x64
# A ordem dos tiles a serem desenhados e controlada por uma lista
# de varias strings que representam as linhas e colunas
#
# Colisao:
# Criar colliders para envolver personagens e obstaculos
# Esses colliders sao formas geometricas, geralmente um retangulo
# collider_jogador = pygame.Rect(pos_x, pos_y, 64, 64)
# declarar o collider dentro do while loop
# o pygame fornece o recurso de colliderect(collider_a_comparar)
#
# antes de checar o pressionar das teclas vou pegar as posicoes antigas
# em old_pos_x e old_pos_y. Se houver colisao, reverter pra elas.
#
# IDEIA PARA O PROJETO DA G3:
# Jogo com mapa na agua, jogador (mergulhador) usa as setas pra atravessar
# de uma ponta a outra. Tubaroes seguem o mergulhador, ao passar de nivel
# aumenta a quantidade. Ao tocar no mergulhador, o tubarao explode e o
# jogo acaba. Obstaculos: minas submarinas, submarinos e pedras.
#
# Este arquivo: PROTOTIPO da atividade 12 com a tematica do mergulhador.
# Implementa so o que a atividade pede (mapa em tileset, personagem
# animado, colisao, dict de recortes, mapa via txt e camera).
# Tubaroes/niveis/game over ficam pra G3.

import math
import os
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 13 - Prototipo Mergulhador")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 22)

TILE = 64
MAPA_PATH = "mapa.txt"
TILESET_PATH = "tileset.png"
SPRITESHEET_PATH = "mergulhador.png"


TIPOS_TILES = ["w", "s", "r", "c", "m"]


def gera_tileset():
    folha = pygame.Surface((TILE * len(TIPOS_TILES), TILE), pygame.SRCALPHA)

    # agua (col 0)
    folha.fill((30, 90, 160), (0, 0, TILE, TILE))
    for indice in range(7):
        y = indice * 9 + 4
        pygame.draw.line(folha, (80, 140, 200), (0, y), (TILE, y), 1)

    # areia (col 1)
    sx = TILE
    folha.fill((230, 210, 140), (sx, 0, TILE, TILE))
    random.seed(42)
    for _ in range(50):
        px = sx + random.randint(0, TILE - 1)
        py = random.randint(0, TILE - 1)
        folha.set_at((px, py), (200, 180, 110))

    # rocha (col 2)
    rx = TILE * 2
    folha.fill((30, 90, 160), (rx, 0, TILE, TILE))
    poligono = [
        (rx + 8, 56),
        (rx + 18, 14),
        (rx + 42, 8),
        (rx + 58, 28),
        (rx + 50, 58),
        (rx + 12, 60),
    ]
    pygame.draw.polygon(folha, (110, 110, 120), poligono)
    pygame.draw.polygon(folha, (70, 70, 80), poligono, 3)

    # coral (col 3)
    cx = TILE * 3
    folha.fill((30, 90, 160), (cx, 0, TILE, TILE))
    pygame.draw.circle(folha, (220, 70, 110), (cx + 32, 48), 14)
    pygame.draw.circle(folha, (220, 70, 110), (cx + 18, 34), 10)
    pygame.draw.circle(folha, (220, 70, 110), (cx + 48, 30), 11)
    pygame.draw.circle(folha, (250, 130, 160), (cx + 32, 48), 6)
    pygame.draw.circle(folha, (250, 130, 160), (cx + 18, 34), 4)

    # mina (col 4)
    mx = TILE * 4
    folha.fill((30, 90, 160), (mx, 0, TILE, TILE))
    pygame.draw.circle(folha, (50, 50, 60), (mx + 32, 32), 22)
    for angulo_graus in range(0, 360, 45):
        rad = math.radians(angulo_graus)
        x1 = mx + 32 + math.cos(rad) * 22
        y1 = 32 + math.sin(rad) * 22
        x2 = mx + 32 + math.cos(rad) * 30
        y2 = 32 + math.sin(rad) * 30
        pygame.draw.line(folha, (50, 50, 60), (x1, y1), (x2, y2), 4)
    pygame.draw.circle(folha, (220, 60, 50), (mx + 32, 32), 5)

    pygame.image.save(folha, TILESET_PATH)


LARGURA_FRAME = 48
ALTURA_FRAME = 48
NUM_FRAMES = 4


def desenha_frame_mergulhador(folha, offset_x, fase):
    centro_x = offset_x + LARGURA_FRAME // 2
    centro_y = ALTURA_FRAME // 2
    # tanque atras
    pygame.draw.rect(folha, (200, 200, 210), (centro_x - 5, centro_y - 18, 10, 10))
    # corpo
    pygame.draw.ellipse(folha, (40, 60, 110), (centro_x - 10, centro_y - 12, 20, 22))
    # capacete
    pygame.draw.circle(folha, (180, 220, 240), (centro_x, centro_y - 14), 8)
    pygame.draw.circle(folha, (40, 30, 25), (centro_x, centro_y - 12), 3)
    # nadadeiras animam de acordo com a fase
    deslocamento = int(math.sin(fase) * 5)
    pygame.draw.ellipse(
        folha, (250, 180, 60), (centro_x - 14, centro_y + 10 + deslocamento, 10, 8)
    )
    pygame.draw.ellipse(
        folha, (250, 180, 60), (centro_x + 4, centro_y + 10 - deslocamento, 10, 8)
    )


def gera_spritesheet():
    folha = pygame.Surface((LARGURA_FRAME * NUM_FRAMES, ALTURA_FRAME), pygame.SRCALPHA)
    for indice in range(NUM_FRAMES):
        fase = indice / NUM_FRAMES * 2 * math.pi
        desenha_frame_mergulhador(folha, indice * LARGURA_FRAME, fase)
    pygame.image.save(folha, SPRITESHEET_PATH)


def carrega_mapa():
    with open(MAPA_PATH) as arquivo:
        return [linha.rstrip("\n") for linha in arquivo if linha.strip()]


if not os.path.exists(TILESET_PATH):
    gera_tileset()
if not os.path.exists(SPRITESHEET_PATH):
    gera_spritesheet()

tileset = pygame.image.load(TILESET_PATH).convert_alpha()
spritesheet = pygame.image.load(SPRITESHEET_PATH).convert_alpha()

# dict pra acessar o corte direto pelo char do mapa (extra: sem varios ifs)
RECORTES = {
    "w": pygame.Rect(0 * TILE, 0, TILE, TILE),
    "s": pygame.Rect(1 * TILE, 0, TILE, TILE),
    "r": pygame.Rect(2 * TILE, 0, TILE, TILE),
    "c": pygame.Rect(3 * TILE, 0, TILE, TILE),
    "m": pygame.Rect(4 * TILE, 0, TILE, TILE),
}

# chars que bloqueiam movimento
SOLIDOS = {"r", "c", "m"}

mapa = carrega_mapa()
MAPA_COLUNAS = len(mapa[0])
MAPA_LINHAS = len(mapa)
MAPA_LARGURA = MAPA_COLUNAS * TILE
MAPA_ALTURA = MAPA_LINHAS * TILE

frames_mergulhador = []
for indice in range(NUM_FRAMES):
    rect_frame = pygame.Rect(indice * LARGURA_FRAME, 0, LARGURA_FRAME, ALTURA_FRAME)
    frames_mergulhador.append(spritesheet.subsurface(rect_frame).copy())


jogador = {
    "x": 3 * TILE,
    "y": 3 * TILE,
    "direcao": "baixo",
    "frame": 0.0,
    "andando": False,
}
VELOCIDADE = 220
VELOCIDADE_FRAME = 8
ANGULOS_DIRECAO = {"baixo": 0, "esquerda": 90, "cima": 180, "direita": -90}


def collider_jogador():
    return pygame.Rect(
        int(jogador["x"]) + 6,
        int(jogador["y"]) + 8,
        LARGURA_FRAME - 12,
        ALTURA_FRAME - 12,
    )


def colide_com_mapa():
    collider = collider_jogador()
    # so olha tiles proximos pra economizar
    col_min = max(0, collider.left // TILE - 1)
    col_max = min(MAPA_COLUNAS - 1, collider.right // TILE + 1)
    lin_min = max(0, collider.top // TILE - 1)
    lin_max = min(MAPA_LINHAS - 1, collider.bottom // TILE + 1)
    for linha in range(lin_min, lin_max + 1):
        for coluna in range(col_min, col_max + 1):
            if mapa[linha][coluna] in SOLIDOS:
                collider_tile = pygame.Rect(coluna * TILE, linha * TILE, TILE, TILE)
                if collider.colliderect(collider_tile):
                    return True
    return False


def atualiza_jogador(delta_tempo, keys):
    # padrao da aula: guarda posicao antiga pra reverter em caso de colisao
    old_pos_x = jogador["x"]
    old_pos_y = jogador["y"]

    direcao_x = 0
    direcao_y = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direcao_x -= 1
        jogador["direcao"] = "esquerda"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direcao_x += 1
        jogador["direcao"] = "direita"
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        direcao_y -= 1
        jogador["direcao"] = "cima"
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direcao_y += 1
        jogador["direcao"] = "baixo"

    jogador["andando"] = direcao_x != 0 or direcao_y != 0

    # move um eixo de cada vez pra poder deslizar nas paredes
    jogador["x"] += direcao_x * VELOCIDADE * delta_tempo
    if colide_com_mapa():
        jogador["x"] = old_pos_x

    jogador["y"] += direcao_y * VELOCIDADE * delta_tempo
    if colide_com_mapa():
        jogador["y"] = old_pos_y

    # nao deixa sair do mapa
    jogador["x"] = max(0, min(MAPA_LARGURA - LARGURA_FRAME, jogador["x"]))
    jogador["y"] = max(0, min(MAPA_ALTURA - ALTURA_FRAME, jogador["y"]))

    # animacao
    if jogador["andando"]:
        jogador["frame"] = (
            jogador["frame"] + VELOCIDADE_FRAME * delta_tempo
        ) % NUM_FRAMES
    else:
        jogador["frame"] = 0


def desenha_jogador(camera_x, camera_y):
    sprite = frames_mergulhador[int(jogador["frame"])]
    sprite = pygame.transform.rotate(sprite, ANGULOS_DIRECAO[jogador["direcao"]])
    screen.blit(sprite, (int(jogador["x"] - camera_x), int(jogador["y"] - camera_y)))


def desenha_mapa(camera_x, camera_y):
    # so desenha as tiles que aparecem na tela
    col_min = max(0, camera_x // TILE)
    col_max = min(MAPA_COLUNAS, (camera_x + LARGURA) // TILE + 1)
    lin_min = max(0, camera_y // TILE)
    lin_max = min(MAPA_LINHAS, (camera_y + ALTURA) // TILE + 1)
    for linha in range(lin_min, lin_max):
        for coluna in range(col_min, col_max):
            char = mapa[linha][coluna]
            screen.blit(
                tileset,
                (coluna * TILE - camera_x, linha * TILE - camera_y),
                RECORTES[char],
            )


running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    atualiza_jogador(delta_tempo, keys)

    # camera segue o jogador, presa nas bordas do mapa
    camera_x = int(jogador["x"] + LARGURA_FRAME // 2 - LARGURA // 2)
    camera_y = int(jogador["y"] + ALTURA_FRAME // 2 - ALTURA // 2)
    camera_x = max(0, min(MAPA_LARGURA - LARGURA, camera_x))
    camera_y = max(0, min(MAPA_ALTURA - ALTURA, camera_y))

    screen.fill((10, 30, 60))
    desenha_mapa(camera_x, camera_y)
    desenha_jogador(camera_x, camera_y)

    dica = fonte.render("nada com setas ou WASD", True, (255, 255, 255))
    screen.blit(dica, (12, 12))

    pygame.display.update()

pygame.quit()
