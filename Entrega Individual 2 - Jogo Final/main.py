import os
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mergulhador - Endless")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)

TILE = 64
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
RECORDE_PATH = os.path.join(BASE_DIR, "recorde.txt")
AZUL_MARINHO = (30, 60, 100)
BRANCO = (255, 255, 255)


def carrega_imagem(nome):
    return pygame.image.load(os.path.join(ASSETS, nome)).convert_alpha()


def recorte_escalado(folha, area, tamanho):
    pedaco = folha.subsurface(pygame.Rect(area)).copy()
    return pygame.transform.scale(pedaco, (tamanho, tamanho))


folha_tiles = carrega_imagem("tiles.png")
sprite_mina = carrega_imagem("mine.png")

tile_mina = pygame.transform.scale(sprite_mina, (TILE, TILE))
tile_chao = recorte_escalado(folha_tiles, (0, 80, 80, 80), TILE)

TETO = TILE
CHAO = ALTURA - TILE


folha_props = carrega_imagem("props.png")


def recorte_prop(area):
    pedaco = folha_props.subsurface(pygame.Rect(area)).copy()
    largura, altura = pedaco.get_size()
    return pygame.transform.scale(pedaco, (largura * TILE // 80, altura * TILE // 80))


PROPS = [
    recorte_prop((432, 41, 92, 231)),
    recorte_prop((177, 34, 198, 205)),
    recorte_prop((49, 95, 85, 98)),
    recorte_prop((614, 317, 52, 67)),
    recorte_prop((514, 327, 48, 56)),
    recorte_prop((434, 332, 46, 51)),
]


folha_jogador = carrega_imagem("player-swiming.png")
NUM_FRAMES_JOGADOR = 7
TAMANHO_JOGADOR = 64
frames_jogador = []
for indice in range(NUM_FRAMES_JOGADOR):
    rect_frame = pygame.Rect(indice * 80, 0, 80, 80)
    sprite = folha_jogador.subsurface(rect_frame).copy()
    frames_jogador.append(
        pygame.transform.scale(sprite, (TAMANHO_JOGADOR, TAMANHO_JOGADOR))
    )


folha_tubarao = carrega_imagem("fish-big.png")
NUM_FRAMES_TUBARAO = 4
LARGURA_TUBARAO = 96
ALTURA_TUBARAO = 56
frames_tubarao = []
for indice in range(NUM_FRAMES_TUBARAO):
    rect_frame = pygame.Rect(indice * 54, 0, 54, 49)
    sprite = folha_tubarao.subsurface(rect_frame).copy()
    frames_tubarao.append(
        pygame.transform.scale(sprite, (LARGURA_TUBARAO, ALTURA_TUBARAO))
    )


GRAVIDADE = 750
FORCA_FLAP = -300
VELOCIDADE_FRAME = 10
VELOCIDADE_BASE = 200
JOGADOR_X = LARGURA // 4

jogador = {"y": float(ALTURA // 2), "vy": 0.0, "frame": 0.0}
distancia = 0.0
obstaculos = []
tubaroes = []
decoracoes = []
proximo_obstaculo_x = 0.0
proximo_tubarao_x = 0.0
proximo_decoracao_x = 0.0
estado = "jogando"


def carrega_recorde():
    try:
        with open(RECORDE_PATH) as arquivo:
            return int(arquivo.read().strip())
    except (OSError, ValueError):
        return 0


def salva_recorde(valor):
    with open(RECORDE_PATH, "w") as arquivo:
        arquivo.write(str(valor))


recorde = carrega_recorde()


def reinicia():
    global distancia, estado
    global proximo_obstaculo_x, proximo_tubarao_x, proximo_decoracao_x
    jogador["y"] = float(ALTURA // 2)
    jogador["vy"] = 0.0
    jogador["frame"] = 0.0
    distancia = 0.0
    obstaculos.clear()
    tubaroes.clear()
    decoracoes.clear()
    proximo_obstaculo_x = LARGURA + 400
    proximo_tubarao_x = LARGURA + 900
    proximo_decoracao_x = LARGURA + 200
    estado = "jogando"


def flap():
    jogador["vy"] = FORCA_FLAP


def velocidade_atual():
    return VELOCIDADE_BASE + min(distancia / 40, 160)


def spawna_obstaculos():
    global proximo_obstaculo_x
    while distancia + LARGURA + TILE >= proximo_obstaculo_x:
        y = random.randint(TETO + 10, CHAO - TILE - 10)
        obstaculos.append({"x": proximo_obstaculo_x, "y": float(y)})
        proximo_obstaculo_x += max(220, 460 - distancia / 25)


def spawna_tubaroes():
    global proximo_tubarao_x
    while distancia + LARGURA + 100 >= proximo_tubarao_x:
        y = random.randint(TETO + 20, CHAO - ALTURA_TUBARAO - 20)
        tubaroes.append(
            {
                "x": proximo_tubarao_x,
                "y": float(y),
                "frame": random.random() * NUM_FRAMES_TUBARAO,
            }
        )
        proximo_tubarao_x += max(550, 1500 - distancia / 10)


def spawna_decoracoes():
    global proximo_decoracao_x
    while distancia + LARGURA + 100 >= proximo_decoracao_x:
        decoracoes.append({"x": proximo_decoracao_x, "sprite": random.choice(PROPS)})
        proximo_decoracao_x += random.randint(320, 720)


def atualiza_jogador(delta_tempo):
    jogador["vy"] += GRAVIDADE * delta_tempo
    jogador["y"] += jogador["vy"] * delta_tempo
    jogador["frame"] = (
        jogador["frame"] + VELOCIDADE_FRAME * delta_tempo
    ) % NUM_FRAMES_JOGADOR


def atualiza_tubaroes(delta_tempo):
    velocidade = 90 + distancia / 60
    for tubarao in tubaroes:
        tubarao["x"] -= velocidade * delta_tempo
        if tubarao["y"] < jogador["y"]:
            tubarao["y"] += 60 * delta_tempo
        elif tubarao["y"] > jogador["y"]:
            tubarao["y"] -= 60 * delta_tempo
        tubarao["frame"] = (tubarao["frame"] + 6 * delta_tempo) % NUM_FRAMES_TUBARAO


def recicla():
    obstaculos[:] = [o for o in obstaculos if o["x"] - distancia > -TILE * 2]
    tubaroes[:] = [t for t in tubaroes if t["x"] - distancia > -LARGURA_TUBARAO * 2]
    decoracoes[:] = [d for d in decoracoes if d["x"] - distancia > -300]


def collider_jogador():
    return pygame.Rect(
        JOGADOR_X + 8,
        int(jogador["y"]) + 16,
        TAMANHO_JOGADOR - 16,
        TAMANHO_JOGADOR - 28,
    )


def colide():
    collider = collider_jogador()
    if collider.top < TETO or collider.bottom > CHAO:
        return True
    for obstaculo in obstaculos:
        rect = pygame.Rect(
            int(obstaculo["x"] - distancia) + 7,
            int(obstaculo["y"]) + 7,
            TILE - 14,
            TILE - 14,
        )
        if collider.colliderect(rect):
            return True
    for tubarao in tubaroes:
        rect = pygame.Rect(
            int(tubarao["x"] - distancia) + 10,
            int(tubarao["y"]) + 10,
            LARGURA_TUBARAO - 20,
            ALTURA_TUBARAO - 20,
        )
        if collider.colliderect(rect):
            return True
    for decoracao in decoracoes:
        sprite = decoracao["sprite"]
        altura = sprite.get_height()
        rect = pygame.Rect(
            int(decoracao["x"] - distancia) + 8,
            CHAO - altura + 14,
            sprite.get_width() - 16,
            altura - 16,
        )
        if collider.colliderect(rect):
            return True
    return False


def desenha_corredor():
    x = -int(distancia % TILE)
    while x < LARGURA:
        screen.blit(tile_mina, (x, 0))
        screen.blit(tile_chao, (x, CHAO))
        x += TILE


def desenha_decoracoes():
    for decoracao in decoracoes:
        sprite = decoracao["sprite"]
        screen.blit(
            sprite, (int(decoracao["x"] - distancia), CHAO - sprite.get_height() + 6)
        )


def desenha_obstaculos():
    for obstaculo in obstaculos:
        screen.blit(tile_mina, (int(obstaculo["x"] - distancia), int(obstaculo["y"])))


def desenha_tubaroes():
    for tubarao in tubaroes:
        sprite = frames_tubarao[int(tubarao["frame"])]
        screen.blit(sprite, (int(tubarao["x"] - distancia), int(tubarao["y"])))


def desenha_jogador():
    screen.blit(frames_jogador[int(jogador["frame"])], (JOGADOR_X, int(jogador["y"])))


def display_pontuacao():
    metros = int(distancia / TILE)
    screen.blit(fonte.render(f"{metros} m", True, BRANCO), (16, 12))
    screen.blit(fonte_pequena.render(f"recorde: {recorde} m", True, BRANCO), (16, 44))


def desenha_mensagem():
    metros = int(distancia / TILE)
    linhas = [
        fonte.render(f"voce foi pego! {metros} m", True, BRANCO),
        fonte_pequena.render(f"recorde: {recorde} m", True, BRANCO),
        fonte_pequena.render("SPACE pra recomecar", True, BRANCO),
    ]
    largura = max(linha.get_width() for linha in linhas) + 60
    altura = sum(linha.get_height() for linha in linhas) + 48
    caixa = pygame.Rect(0, 0, largura, altura)
    caixa.center = (LARGURA // 2, ALTURA // 2)
    pygame.draw.rect(screen, (0, 0, 0), caixa, border_radius=8)
    pygame.draw.rect(screen, BRANCO, caixa, 2, border_radius=8)
    y = caixa.top + 18
    for linha in linhas:
        screen.blit(linha, (caixa.centerx - linha.get_width() // 2, y))
        y += linha.get_height() + 6


reinicia()

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
        distancia += velocidade_atual() * delta_tempo
        atualiza_jogador(delta_tempo)
        atualiza_tubaroes(delta_tempo)
        spawna_obstaculos()
        spawna_tubaroes()
        spawna_decoracoes()
        recicla()
        if colide():
            estado = "morreu"
            metros = int(distancia / TILE)
            if metros > recorde:
                recorde = metros
                salva_recorde(recorde)

    screen.fill(AZUL_MARINHO)
    desenha_corredor()
    desenha_decoracoes()
    desenha_obstaculos()
    desenha_tubaroes()
    desenha_jogador()
    display_pontuacao()
    if estado == "morreu":
        desenha_mensagem()

    pygame.display.update()
