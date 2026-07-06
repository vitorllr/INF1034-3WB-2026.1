import math
import os
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Diver")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 26, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 20)


TILE = 64
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "assets")
RECORDE_PATH = os.path.join(BASE_DIR, "recorde.txt")
LEADERBOARD_PATH = os.path.join(BASE_DIR, "leaderboard.txt")
MAX_LEADERBOARD = 10
MAX_NOME = 12
AZUL_MARINHO = (30, 60, 100)
BRANCO = (255, 255, 255)


def carrega_fonte_titulo(tamanho):
    # fonte empacotada em assets/ -> mesmo visual em qualquer PC
    empacotada = os.path.join(ASSETS, "TitanOne-Regular.ttf")
    if os.path.exists(empacotada):
        return pygame.font.Font(empacotada, tamanho)
    # fallback por seguranca caso o arquivo suma
    alternativa = pygame.font.match_font(
        "titanone,fredokaone,arialroundedmtbold,cooperblack,arialblack,impact,arial"
    )
    if alternativa:
        return pygame.font.Font(alternativa, tamanho)
    return pygame.font.SysFont("arial", tamanho, bold=True)


fonte_titulo = carrega_fonte_titulo(130)


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
explosoes = []

DURACAO_EXPLOSAO = 0.55
CORES_EXPLOSAO = [(255, 240, 120), (255, 170, 40), (255, 90, 20), (200, 40, 20)]
proximo_obstaculo_x = 0.0
proximo_tubarao_x = 0.0
proximo_decoracao_x = 0.0
estado = "nome"
nome_jogador = ""


def carrega_recorde():
    try:
        with open(RECORDE_PATH) as arquivo:
            return int(arquivo.read().strip())
    except (OSError, ValueError):
        return 0


def salva_recorde(valor):
    with open(RECORDE_PATH, "w") as arquivo:
        arquivo.write(str(valor))


def carrega_leaderboard():
    entradas = []
    try:
        with open(LEADERBOARD_PATH, encoding="utf-8") as arquivo:
            for linha in arquivo:
                if ";" not in linha:
                    continue
                nome, pontos = linha.rsplit(";", 1)
                try:
                    entradas.append((nome.strip(), int(pontos)))
                except ValueError:
                    continue
    except OSError:
        pass
    entradas.sort(key=lambda item: item[1], reverse=True)
    return entradas


def salva_leaderboard(entradas):
    with open(LEADERBOARD_PATH, "w", encoding="utf-8") as arquivo:
        for nome, pontos in entradas[:MAX_LEADERBOARD]:
            arquivo.write(f"{nome};{pontos}\n")


def registra_pontuacao(nome, pontos):
    entradas = carrega_leaderboard()
    entradas.append((nome or "anonimo", pontos))
    entradas.sort(key=lambda item: item[1], reverse=True)
    entradas = entradas[:MAX_LEADERBOARD]
    salva_leaderboard(entradas)
    return entradas


recorde = carrega_recorde()
leaderboard = carrega_leaderboard()


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
    explosoes.clear()
    proximo_obstaculo_x = LARGURA + 400
    proximo_tubarao_x = LARGURA + 900
    proximo_decoracao_x = LARGURA + 200
    estado = "jogando"


def flap():
    jogador["vy"] = FORCA_FLAP


def velocidade_atual():
    return VELOCIDADE_BASE + min(distancia / 22, 260)


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


def descarta_fora_da_tela(lista, margem):
    sobreviventes = []
    for objeto in lista:
        if objeto["x"] - distancia > -margem:
            sobreviventes.append(objeto)
    lista[:] = sobreviventes


def recicla():
    descarta_fora_da_tela(obstaculos, TILE * 2)
    descarta_fora_da_tela(tubaroes, LARGURA_TUBARAO * 2)
    descarta_fora_da_tela(decoracoes, 300)


def collider_jogador():
    return pygame.Rect(
        JOGADOR_X + 20,
        int(jogador["y"]) + 26,
        TAMANHO_JOGADOR - 40,
        TAMANHO_JOGADOR - 44,
    )


def detecta_colisao():
    collider = collider_jogador()
    if collider.top < TETO or collider.bottom > CHAO:
        return ("parede", collider.center)
    for obstaculo in obstaculos:
        rect = pygame.Rect(
            int(obstaculo["x"] - distancia) + 7,
            int(obstaculo["y"]) + 7,
            TILE - 14,
            TILE - 14,
        )
        if collider.colliderect(rect):
            centro = (
                int(obstaculo["x"] - distancia) + TILE // 2,
                int(obstaculo["y"]) + TILE // 2,
            )
            return ("mina", centro)
    for tubarao in tubaroes:
        rect = pygame.Rect(
            int(tubarao["x"] - distancia) + 16,
            int(tubarao["y"]) + 14,
            LARGURA_TUBARAO - 32,
            ALTURA_TUBARAO - 28,
        )
        if collider.colliderect(rect):
            centro = (
                int(tubarao["x"] - distancia) + LARGURA_TUBARAO // 2,
                int(tubarao["y"]) + ALTURA_TUBARAO // 2,
            )
            return ("tubarao", centro)
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
            return ("decoracao", collider.center)
    return None


def spawna_explosao(x, y):
    particulas = []
    for _ in range(16):
        particulas.append(
            {
                "ang": random.uniform(0, math.tau),
                "vel": random.uniform(120, 340),
                "cor": random.choice(CORES_EXPLOSAO),
                "raio": random.randint(4, 9),
            }
        )
    explosoes.append(
        {"x": float(x), "y": float(y), "tempo": 0.0, "particulas": particulas}
    )


def atualiza_explosoes(delta_tempo):
    for explosao in explosoes:
        explosao["tempo"] += delta_tempo
    explosoes[:] = [e for e in explosoes if e["tempo"] < DURACAO_EXPLOSAO]


def desenha_explosoes():
    for explosao in explosoes:
        t = min(explosao["tempo"] / DURACAO_EXPLOSAO, 1.0)
        alpha = int(255 * (1 - t))
        lado = 360
        centro = lado // 2
        surf = pygame.Surface((lado, lado), pygame.SRCALPHA)
        raio_nucleo = int(10 + 55 * (1 - t))
        pygame.draw.circle(surf, (255, 245, 200, alpha), (centro, centro), raio_nucleo)
        raio_anel = int(30 + 130 * t)
        pygame.draw.circle(
            surf,
            (255, 140, 30, alpha),
            (centro, centro),
            raio_anel,
            max(2, int(12 * (1 - t))),
        )
        for p in explosao["particulas"]:
            dist = p["vel"] * explosao["tempo"]
            px = centro + math.cos(p["ang"]) * dist
            py = centro + math.sin(p["ang"]) * dist
            raio = max(1, int(p["raio"] * (1 - t)))
            pygame.draw.circle(surf, (*p["cor"], alpha), (int(px), int(py)), raio)
        screen.blit(surf, (int(explosao["x"]) - centro, int(explosao["y"]) - centro))


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


def sprite_tubarao_orientado(tubarao):
    base = frames_tubarao[int(tubarao["frame"])]
    dx = JOGADOR_X - (tubarao["x"] - distancia)
    dy = jogador["y"] - tubarao["y"]
    if dx <= 0:
        # mergulhador a esquerda: sprite olha pra direita, espelha e inclina
        base = pygame.transform.flip(base, True, False)
        return pygame.transform.rotate(base, math.degrees(math.atan2(dy, -dx)))
    # mergulhador a direita (peixe ja passou): sprite ja olha pra direita
    return pygame.transform.rotate(base, math.degrees(math.atan2(-dy, dx)))


def desenha_tubaroes():
    for tubarao in tubaroes:
        sprite = sprite_tubarao_orientado(tubarao)
        centro = (
            int(tubarao["x"] - distancia) + LARGURA_TUBARAO // 2,
            int(tubarao["y"]) + ALTURA_TUBARAO // 2,
        )
        screen.blit(sprite, sprite.get_rect(center=centro))


def desenha_jogador():
    screen.blit(frames_jogador[int(jogador["frame"])], (JOGADOR_X, int(jogador["y"])))


def display_pontuacao():
    metros = int(distancia / TILE)
    screen.blit(fonte.render(f"{metros} m", True, BRANCO), (16, 12))
    screen.blit(fonte_pequena.render(f"recorde: {recorde} m", True, BRANCO), (16, 44))


def desenha_caixa(linhas):
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


def desenha_tela_nome():
    desenha_titulo(LARGURA // 2, 200)
    cursor = "_" if (pygame.time.get_ticks() // 400) % 2 == 0 else " "
    linhas = [
        fonte_pequena.render("digite seu nome:", True, BRANCO),
        fonte.render(nome_jogador + cursor, True, BRANCO),
        fonte_pequena.render("ENTER pra comecar", True, BRANCO),
    ]
    desenha_painel(linhas, ALTURA // 2 + 140)


def desenha_mensagem():
    metros = int(distancia / TILE)
    linhas = [
        fonte.render(
            f"{nome_jogador or 'anonimo'}, voce foi pego! {metros} m", True, BRANCO
        ),
        fonte_pequena.render(f"recorde: {recorde} m", True, BRANCO),
        fonte_pequena.render("-- leaderboard --", True, BRANCO),
    ]
    for posicao, (nome, pontos) in enumerate(leaderboard[:5], start=1):
        linhas.append(
            fonte_pequena.render(f"{posicao}. {nome} - {pontos} m", True, BRANCO)
        )
    linhas.append(
        fonte_pequena.render("SPACE recomecar / ENTER trocar nome", True, BRANCO)
    )
    desenha_caixa(linhas)


nadador = {
    "x": -float(TAMANHO_JOGADOR),
    "y": float(ALTURA // 2),
    "fase": 0.0,
    "frame": 0.0,
}
bolhas = []


def atualiza_bolhas(delta_tempo):
    for bolha in bolhas:
        bolha["y"] -= bolha["vy"] * delta_tempo
        bolha["x"] += math.sin(bolha["y"] * 0.02) * 0.5
    bolhas[:] = [bolha for bolha in bolhas if bolha["y"] > TETO - 20]
    if random.random() < delta_tempo * 3:
        bolhas.append(
            {
                "x": random.uniform(0, LARGURA),
                "y": float(CHAO + 10),
                "r": random.randint(3, 8),
                "vy": random.uniform(40, 90),
            }
        )


def desenha_bolhas():
    for bolha in bolhas:
        raio = bolha["r"]
        surf = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (200, 225, 255, 90), (raio, raio), raio)
        pygame.draw.circle(surf, (255, 255, 255, 120), (raio, raio), raio, 1)
        screen.blit(surf, (int(bolha["x"] - raio), int(bolha["y"] - raio)))


def atualiza_capa(delta_tempo):
    global distancia
    distancia += 120 * delta_tempo
    nadador["x"] += 130 * delta_tempo
    if nadador["x"] > LARGURA + TAMANHO_JOGADOR:
        nadador["x"] = -float(TAMANHO_JOGADOR)
    nadador["fase"] += delta_tempo
    nadador["y"] = (
        ALTURA / 2
        - TAMANHO_JOGADOR / 2
        + math.sin(nadador["fase"] * 1.6) * 70
        + math.sin(nadador["fase"] * 0.6) * 40
    )
    nadador["frame"] = (
        nadador["frame"] + VELOCIDADE_FRAME * delta_tempo
    ) % NUM_FRAMES_JOGADOR
    atualiza_bolhas(delta_tempo)


def desenha_capa_fundo():
    desenha_corredor()
    desenha_bolhas()
    quadro = frames_jogador[int(nadador["frame"])]
    screen.blit(quadro, (int(nadador["x"]), int(nadador["y"])))


def render_contornado(texto, fonte_usada, cor_fill, cor_contorno, espessura):
    base = fonte_usada.render(texto, True, cor_fill)
    contorno = fonte_usada.render(texto, True, cor_contorno)
    largura, altura = base.get_size()
    pad = espessura + 2
    surf = pygame.Surface((largura + pad * 2, altura + pad * 2), pygame.SRCALPHA)
    for dx in range(-espessura, espessura + 1):
        for dy in range(-espessura, espessura + 1):
            if dx * dx + dy * dy <= espessura * espessura:
                surf.blit(contorno, (pad + dx, pad + dy))
    surf.blit(base, (pad, pad))
    return surf


def compoe_titulo():
    fill = (250, 250, 250)
    contorno = (74, 63, 84)
    cima = pygame.transform.rotate(
        render_contornado("FLAPPY", fonte_titulo, fill, contorno, 6), 5
    )
    baixo = pygame.transform.rotate(
        render_contornado("DIVER", fonte_titulo, fill, contorno, 6), -4
    )
    offset_x = int(cima.get_width() * 0.30)
    sobreposicao = int(min(cima.get_height(), baixo.get_height()) * 0.18)
    largura = max(cima.get_width(), offset_x + baixo.get_width())
    altura = cima.get_height() + baixo.get_height() - sobreposicao
    canvas = pygame.Surface((largura, altura), pygame.SRCALPHA)
    canvas.blit(cima, (0, 0))
    canvas.blit(baixo, (offset_x, cima.get_height() - sobreposicao))
    return canvas


titulo_surf = compoe_titulo()
titulo_sombra = titulo_surf.copy()
titulo_sombra.fill((15, 12, 20, 130), special_flags=pygame.BLEND_RGBA_MULT)


def desenha_titulo(cx, cy):
    bob = math.sin(pygame.time.get_ticks() / 500) * 8
    rect = titulo_surf.get_rect(center=(cx, int(cy + bob)))
    screen.blit(titulo_sombra, (rect.x + 8, rect.y + 10))
    screen.blit(titulo_surf, rect)


def desenha_texto_central(superficie, cx, y):
    sombra = superficie.copy()
    sombra.fill((0, 0, 0, 180), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(sombra, (cx - superficie.get_width() // 2 + 2, y + 2))
    screen.blit(superficie, (cx - superficie.get_width() // 2, y))


def desenha_painel(linhas, centro_y):
    largura = max(linha.get_width() for linha in linhas) + 60
    altura = sum(linha.get_height() for linha in linhas) + 48
    caixa = pygame.Rect(0, 0, largura, altura)
    caixa.center = (LARGURA // 2, centro_y)
    fundo = pygame.Surface((largura, altura), pygame.SRCALPHA)
    fundo.fill((10, 25, 45, 190))
    screen.blit(fundo, caixa.topleft)
    pygame.draw.rect(screen, BRANCO, caixa, 2, border_radius=10)
    y = caixa.top + 18
    for linha in linhas:
        screen.blit(linha, (caixa.centerx - linha.get_width() // 2, y))
        y += linha.get_height() + 6


def desenha_tela_capa():
    desenha_titulo(LARGURA // 2, ALTURA // 2 - 30)
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        desenha_texto_central(
            fonte.render("aperte ESPACO para jogar", True, BRANCO),
            LARGURA // 2,
            ALTURA - 170,
        )
    desenha_texto_central(
        fonte_pequena.render(f"recorde: {recorde} m", True, BRANCO),
        LARGURA // 2,
        ALTURA - 120,
    )


estado = "capa"

running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado == "capa":
                estado = "nome"
        elif event.type == pygame.KEYDOWN:
            if estado == "capa":
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    estado = "nome"
            elif estado == "nome":
                if event.key == pygame.K_RETURN and nome_jogador.strip():
                    reinicia()
                elif event.key == pygame.K_BACKSPACE:
                    nome_jogador = nome_jogador[:-1]
                elif (
                    event.unicode
                    and event.unicode.isprintable()
                    and len(nome_jogador) < MAX_NOME
                ):
                    nome_jogador += event.unicode
            elif estado == "jogando":
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    flap()
            elif estado == "morreu":
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    reinicia()
                elif event.key == pygame.K_RETURN:
                    estado = "nome"

    if estado in ("capa", "nome"):
        atualiza_capa(delta_tempo)
    elif estado == "jogando":
        distancia += velocidade_atual() * delta_tempo
        atualiza_jogador(delta_tempo)
        atualiza_tubaroes(delta_tempo)
        spawna_obstaculos()
        spawna_tubaroes()
        spawna_decoracoes()
        recicla()
        colisao = detecta_colisao()
        if colisao:
            tipo, posicao = colisao
            if tipo in ("tubarao", "mina"):
                spawna_explosao(*posicao)
            estado = "morreu"
            metros = int(distancia / TILE)
            if metros > recorde:
                recorde = metros
                salva_recorde(recorde)
            leaderboard = registra_pontuacao(nome_jogador.strip(), metros)

    atualiza_explosoes(delta_tempo)

    screen.fill(AZUL_MARINHO)
    if estado in ("capa", "nome"):
        desenha_capa_fundo()
    else:
        desenha_corredor()
        desenha_decoracoes()
        desenha_obstaculos()
        desenha_tubaroes()
        desenha_jogador()
        desenha_explosoes()
        display_pontuacao()
    if estado == "capa":
        desenha_tela_capa()
    elif estado == "nome":
        desenha_tela_nome()
    elif estado == "morreu":
        desenha_mensagem()

    pygame.display.update()
