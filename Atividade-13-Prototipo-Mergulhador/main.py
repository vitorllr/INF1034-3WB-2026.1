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
# PROTOTIPO PARA G3 - estilo FLAPPY BIRD
# o mergulhador anda da esquerda para a direita sozinho
# o jogador aperta SPACE pra nadar pra cima, gravidade puxa pra baixo
# tubaroes aparecem pela direita e nadam pra esquerda perseguindo
# a cada nivel concluido aumenta a quantidade de tubaroes
# bateu em tubarao, parede ou chao = morre, recomeca do nivel 1
#
# Assets: Underwater Diving Pack (CC0) - opengameart.org
# ver assets/CREDITS.txt

import os
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 13 - Mergulhador (G3 prototipo)")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)

TILE = 64
MAPA_PATH = "mapa.txt"
ASSETS = "assets"


def carrega_imagem(nome):
    return pygame.image.load(os.path.join(ASSETS, nome)).convert_alpha()


background = carrega_imagem("background.png")
BG_LARGURA = background.get_width()
BG_ALTURA = background.get_height()


def recorte_escalado(folha, area, tamanho):
    """Pega um pedaco da folha e redimensiona pra (tamanho, tamanho)."""
    pedaco = folha.subsurface(pygame.Rect(area)).copy()
    return pygame.transform.scale(pedaco, (tamanho, tamanho))


folha_tiles = carrega_imagem("tiles.png")
folha_props = carrega_imagem("props.png")
sprite_mina = carrega_imagem("mine.png")

# dict de tiles 64x64 indexado pelo char do mapa (extra: sem ifs)
# as areas vem das folhas do pacote underwater
TILES = {
    "w": None,  # agua = transparente, o background aparece atras
    "s": recorte_escalado(folha_tiles, (320, 80, 80, 80), TILE),
    "r": recorte_escalado(folha_tiles, (0, 0, 80, 80), TILE),
    "c": recorte_escalado(folha_props, (480, 320, 80, 80), TILE),
    "m": pygame.transform.scale(sprite_mina, (TILE, TILE)),
}

SOLIDOS = {"r", "c", "m", "s"}


def carrega_mapa():
    with open(MAPA_PATH) as arquivo:
        return [linha.rstrip("\n") for linha in arquivo if linha.strip()]


mapa = carrega_mapa()
MAPA_COLUNAS = len(mapa[0])
MAPA_LINHAS = len(mapa)
MAPA_LARGURA = MAPA_COLUNAS * TILE
MAPA_ALTURA = MAPA_LINHAS * TILE


# sprites do mergulhador (7 frames de 80x80, escalados pra 64x64)
folha_jogador = carrega_imagem("player-swiming.png")
NUM_FRAMES_JOGADOR = 7
TAMANHO_JOGADOR = 64
frames_jogador = []
for indice in range(NUM_FRAMES_JOGADOR):
    rect_frame = pygame.Rect(indice * 80, 0, 80, 80)
    sprite = folha_jogador.subsurface(rect_frame).copy()
    sprite = pygame.transform.scale(sprite, (TAMANHO_JOGADOR, TAMANHO_JOGADOR))
    frames_jogador.append(sprite)


# sprites do tubarao (4 frames de 54x49, escalados)
folha_tubarao = carrega_imagem("fish-big.png")
NUM_FRAMES_TUBARAO = 4
LARGURA_TUBARAO = 96
ALTURA_TUBARAO = 56
TUBARAO_FRAME_FONTE = 54
frames_tubarao = []
for indice in range(NUM_FRAMES_TUBARAO):
    rect_frame = pygame.Rect(indice * TUBARAO_FRAME_FONTE, 0, TUBARAO_FRAME_FONTE, 49)
    sprite = folha_tubarao.subsurface(rect_frame).copy()
    sprite = pygame.transform.scale(sprite, (LARGURA_TUBARAO, ALTURA_TUBARAO))
    frames_tubarao.append(sprite)


VELOCIDADE_HORIZONTAL = 220
GRAVIDADE = 750
FORCA_FLAP = -300
VELOCIDADE_FRAME = 10
VELOCIDADE_TUBARAO_BASE = 170

jogador = {
    "x": float(TILE * 2),
    "y": float(MAPA_ALTURA // 2),
    "vy": 0.0,
    "frame": 0.0,
}
tubaroes = []
nivel = 1
estado = "jogando"  # jogando, morreu, vitoria


def novo_tubarao():
    return {
        "x": float(jogador["x"] + LARGURA + random.randint(100, 700)),
        "y": float(random.randint(TILE, MAPA_ALTURA - TILE * 2)),
        "frame": random.random() * NUM_FRAMES_TUBARAO,
    }


def inicia_nivel():
    global tubaroes, estado
    jogador["x"] = float(TILE * 2)
    jogador["y"] = float(MAPA_ALTURA // 2)
    jogador["vy"] = 0.0
    jogador["frame"] = 0.0
    tubaroes = [novo_tubarao() for _ in range(nivel)]
    estado = "jogando"


def reinicia_jogo():
    global nivel
    nivel = 1
    inicia_nivel()


def proximo_nivel():
    global nivel
    nivel += 1
    inicia_nivel()


def flap():
    jogador["vy"] = FORCA_FLAP


def collider_jogador():
    return pygame.Rect(
        int(jogador["x"]) + 8,
        int(jogador["y"]) + 16,
        TAMANHO_JOGADOR - 16,
        TAMANHO_JOGADOR - 28,
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


def colide_com_tubaroes():
    collider = collider_jogador()
    for tubarao in tubaroes:
        tubarao_rect = pygame.Rect(
            int(tubarao["x"]) + 10,
            int(tubarao["y"]) + 10,
            LARGURA_TUBARAO - 20,
            ALTURA_TUBARAO - 20,
        )
        if collider.colliderect(tubarao_rect):
            return True
    return False


def atualiza_jogador(delta_tempo):
    jogador["x"] += VELOCIDADE_HORIZONTAL * delta_tempo
    jogador["vy"] += GRAVIDADE * delta_tempo
    jogador["y"] += jogador["vy"] * delta_tempo
    if jogador["y"] < 0:
        jogador["y"] = 0
        jogador["vy"] = 0
    jogador["frame"] = (
        jogador["frame"] + VELOCIDADE_FRAME * delta_tempo
    ) % NUM_FRAMES_JOGADOR


def atualiza_tubaroes(delta_tempo):
    velocidade_atual = VELOCIDADE_TUBARAO_BASE + (nivel - 1) * 15
    for tubarao in tubaroes:
        tubarao["x"] -= velocidade_atual * delta_tempo
        if tubarao["y"] < jogador["y"]:
            tubarao["y"] += 50 * delta_tempo
        elif tubarao["y"] > jogador["y"]:
            tubarao["y"] -= 50 * delta_tempo
        tubarao["frame"] = (tubarao["frame"] + 6 * delta_tempo) % NUM_FRAMES_TUBARAO
        if tubarao["x"] < jogador["x"] - 400:
            tubarao["x"] = jogador["x"] + LARGURA + random.randint(200, 800)
            tubarao["y"] = random.randint(TILE, MAPA_ALTURA - TILE * 2)


def desenha_background(camera_x, camera_y):
    # parallax: bg desloca mais devagar que a camera (sensacao de profundidade)
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
    screen.blit(
        sprite,
        (int(jogador["x"] - camera_x), int(jogador["y"] - camera_y)),
    )


def desenha_tubaroes(camera_x, camera_y):
    for tubarao in tubaroes:
        sprite = frames_tubarao[int(tubarao["frame"])]
        screen.blit(
            sprite,
            (int(tubarao["x"] - camera_x), int(tubarao["y"] - camera_y)),
        )


def desenha_hud():
    txt_nivel = fonte.render(f"Nivel {nivel}", True, (255, 255, 255))
    screen.blit(txt_nivel, (16, 12))
    txt_tubaroes = fonte_pequena.render(
        f"tubaroes neste nivel: {len(tubaroes)}", True, (255, 255, 255)
    )
    screen.blit(txt_tubaroes, (16, 44))
    txt_dica = fonte_pequena.render("SPACE pra nadar pra cima", True, (255, 255, 255))
    screen.blit(txt_dica, (16, 68))


def desenha_mensagem(texto):
    superficie = fonte.render(texto, True, (255, 255, 255))
    rect = superficie.get_rect(center=(LARGURA // 2, ALTURA // 2))
    fundo = rect.inflate(60, 30)
    pygame.draw.rect(screen, (0, 0, 0), fundo, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), fundo, 2, border_radius=8)
    screen.blit(superficie, rect)


inicia_nivel()

running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                if estado == "jogando":
                    flap()
                elif estado == "morreu":
                    reinicia_jogo()
                elif estado == "vitoria":
                    proximo_nivel()

    if estado == "jogando":
        atualiza_jogador(delta_tempo)
        atualiza_tubaroes(delta_tempo)

        if colide_com_mapa() or colide_com_tubaroes() or jogador["y"] > MAPA_ALTURA:
            estado = "morreu"
        elif jogador["x"] >= MAPA_LARGURA - TAMANHO_JOGADOR * 2:
            estado = "vitoria"

    camera_x = int(jogador["x"] + TAMANHO_JOGADOR // 2 - LARGURA // 2)
    camera_x = max(0, min(MAPA_LARGURA - LARGURA, camera_x))
    camera_y = 0

    desenha_background(camera_x, camera_y)
    desenha_mapa(camera_x, camera_y)
    desenha_tubaroes(camera_x, camera_y)
    desenha_jogador(camera_x, camera_y)
    desenha_hud()

    if estado == "morreu":
        desenha_mensagem(f"voce foi pego no nivel {nivel}! SPACE pra recomecar")
    elif estado == "vitoria":
        desenha_mensagem(f"nivel {nivel} concluido! SPACE pra avancar")

    pygame.display.update()
