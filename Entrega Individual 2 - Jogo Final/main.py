import os

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Entrega 2 - Movimentacao e Colliders")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)

TILE = 64
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPA_PATH = os.path.join(BASE_DIR, "mapa.txt")
ASSETS = os.path.join(BASE_DIR, "assets")
AZUL_MARINHO = (30, 60, 100)
BRANCO = (255, 255, 255)


def carrega_imagem(nome):
    return pygame.image.load(os.path.join(ASSETS, nome)).convert_alpha()


def recorte_escalado(folha, area, tamanho):
    pedaco = folha.subsurface(pygame.Rect(area)).copy()
    return pygame.transform.scale(pedaco, (tamanho, tamanho))


folha_tiles = carrega_imagem("tiles.png")
folha_props = carrega_imagem("props.png")
sprite_mina = carrega_imagem("mine.png")

TILES = {
    "w": None,
    "s": recorte_escalado(folha_tiles, (0, 80, 80, 80), TILE),
    "r": recorte_escalado(folha_tiles, (0, 0, 80, 80), TILE),
    "c": recorte_escalado(folha_props, (480, 320, 80, 80), TILE),
    "m": pygame.transform.scale(sprite_mina, (TILE, TILE)),
}

SOLIDOS = {"r", "c", "m", "s"}


def recorte_prop(area):
    pedaco = folha_props.subsurface(pygame.Rect(area)).copy()
    largura, altura = pedaco.get_size()
    return pygame.transform.scale(pedaco, (largura * TILE // 80, altura * TILE // 80))


PROPS = {
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

CHAO = (MAPA_LINHAS - 1) * TILE + 20
DECORACOES = [
    ("estatua", 240),
    ("kelp", 520),
    ("coral", 760),
    ("arco", 980),
    ("anemona", 1240),
    ("pilar", 1500),
    ("kelp", 1780),
    ("estatua_coral", 2040),
    ("coral", 2320),
    ("anemona", 2560),
    ("arco", 2820),
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


VELOCIDADE_HORIZONTAL = 220
GRAVIDADE = 750
FORCA_FLAP = -300
VELOCIDADE_FRAME = 10

jogador = {
    "x": float(TILE * 2),
    "y": float(MAPA_ALTURA // 2),
    "vy": 0.0,
    "frame": 0.0,
}
estado = "jogando"


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


def flap():
    jogador["vy"] = FORCA_FLAP


def reinicia():
    global estado
    jogador["x"] = float(TILE * 2)
    jogador["y"] = float(MAPA_ALTURA // 2)
    jogador["vy"] = 0.0
    jogador["frame"] = 0.0
    estado = "jogando"


def atualiza_jogador(delta_tempo):
    jogador["x"] += VELOCIDADE_HORIZONTAL * delta_tempo
    jogador["vy"] += GRAVIDADE * delta_tempo
    jogador["y"] += jogador["vy"] * delta_tempo
    jogador["frame"] = (
        jogador["frame"] + VELOCIDADE_FRAME * delta_tempo
    ) % NUM_FRAMES_JOGADOR


def desenha_mapa(camera_x):
    col_min = max(0, camera_x // TILE)
    col_max = min(MAPA_COLUNAS, (camera_x + LARGURA) // TILE + 1)
    for linha in range(MAPA_LINHAS):
        for coluna in range(col_min, col_max):
            sprite_tile = TILES[mapa[linha][coluna]]
            if sprite_tile is not None:
                screen.blit(
                    sprite_tile,
                    (coluna * TILE - camera_x, linha * TILE + DESLOCAMENTO_Y),
                )


def desenha_decoracoes(camera_x):
    for nome, x in DECORACOES:
        sprite = PROPS[nome]
        screen.blit(
            sprite,
            (x - camera_x, CHAO - sprite.get_height() + DESLOCAMENTO_Y),
        )


def desenha_jogador(camera_x):
    sprite = frames_jogador[int(jogador["frame"])]
    pos = (int(jogador["x"] - camera_x), int(jogador["y"]) + DESLOCAMENTO_Y)
    screen.blit(sprite, pos)


def desenha_hud():
    titulo = fonte_pequena.render("Entrega 2 - movimentacao e colliders", True, BRANCO)
    screen.blit(titulo, (16, 12))
    dica = fonte_pequena.render("SPACE / W / seta pra cima = nadar", True, BRANCO)
    screen.blit(dica, (16, 38))


def desenha_mensagem(texto):
    superficie = fonte.render(texto, True, BRANCO)
    rect = superficie.get_rect(center=(LARGURA // 2, ALTURA // 2))
    fundo = rect.inflate(60, 30)
    pygame.draw.rect(screen, (0, 0, 0), fundo, border_radius=8)
    pygame.draw.rect(screen, BRANCO, fundo, 2, border_radius=8)
    screen.blit(superficie, rect)


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
                else:
                    reinicia()

    if estado == "jogando":
        atualiza_jogador(delta_tempo)
        if colide_com_mapa() or jogador["y"] > MAPA_ALTURA:
            estado = "morreu"
        elif jogador["x"] >= MAPA_LARGURA - TAMANHO_JOGADOR:
            reinicia()

    camera_x = int(jogador["x"] + TAMANHO_JOGADOR // 2 - LARGURA // 2)
    camera_x = max(0, min(MAPA_LARGURA - LARGURA, camera_x))

    screen.fill(AZUL_MARINHO)
    desenha_mapa(camera_x)
    desenha_decoracoes(camera_x)
    desenha_jogador(camera_x)
    desenha_hud()

    if estado == "morreu":
        desenha_mensagem("voce bateu! SPACE pra recomecar")

    pygame.display.update()
