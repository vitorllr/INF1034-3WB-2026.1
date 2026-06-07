import math
import os
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 11 - Animacoes")
clock = pygame.time.Clock()
fonte_grande = pygame.font.SysFont("Arial", 32, bold=True)
fonte = pygame.font.SysFont("Arial", 22)

CHAO_Y = 560


LARGURA_FRAME = 72
ALTURA_FRAME = 96
NUM_FRAMES_ANDAR = 8
NUM_FRAMES_PULO = 4
SPRITESHEET_PATH = "personagem_spritesheet.png"


def desenha_frame_personagem(folha, offset_x, fase, pulando):
    centro_x = offset_x + LARGURA_FRAME // 2
    # cabeca
    pygame.draw.circle(folha, (250, 220, 180), (centro_x, 22), 16)
    pygame.draw.circle(folha, (40, 30, 25), (centro_x + 4, 20), 3)
    # tronco
    pygame.draw.rect(
        folha, (60, 100, 180), (centro_x - 12, 38, 24, 34), border_radius=4
    )

    if pulando:
        # bracos pra cima, pernas dobradas
        pygame.draw.line(
            folha, (250, 220, 180), (centro_x - 12, 44), (centro_x - 22, 28), 6
        )
        pygame.draw.line(
            folha, (250, 220, 180), (centro_x + 12, 44), (centro_x + 22, 28), 6
        )
        pygame.draw.line(
            folha, (30, 30, 30), (centro_x - 8, 72), (centro_x - 14, 88), 7
        )
        pygame.draw.line(
            folha, (30, 30, 30), (centro_x + 8, 72), (centro_x + 14, 88), 7
        )
    else:
        # bracos e pernas balancando em fases opostas
        deslocamento_braco = int(fase * 10)
        deslocamento_perna = int(fase * 14)
        pygame.draw.line(
            folha,
            (250, 220, 180),
            (centro_x - 12, 44),
            (centro_x - 12 + deslocamento_braco, 64),
            6,
        )
        pygame.draw.line(
            folha,
            (250, 220, 180),
            (centro_x + 12, 44),
            (centro_x + 12 - deslocamento_braco, 64),
            6,
        )
        pygame.draw.line(
            folha,
            (30, 30, 30),
            (centro_x - 6, 72),
            (centro_x - 6 + deslocamento_perna, 92),
            7,
        )
        pygame.draw.line(
            folha,
            (30, 30, 30),
            (centro_x + 6, 72),
            (centro_x + 6 - deslocamento_perna, 92),
            7,
        )


def gera_e_salva_spritesheet():
    total_frames = NUM_FRAMES_ANDAR + NUM_FRAMES_PULO
    folha = pygame.Surface(
        (LARGURA_FRAME * total_frames, ALTURA_FRAME), pygame.SRCALPHA
    )

    for indice in range(NUM_FRAMES_ANDAR):
        offset_x = indice * LARGURA_FRAME
        fase = math.sin(indice / NUM_FRAMES_ANDAR * 2 * math.pi)
        desenha_frame_personagem(folha, offset_x, fase, pulando=False)

    for indice in range(NUM_FRAMES_PULO):
        offset_x = (NUM_FRAMES_ANDAR + indice) * LARGURA_FRAME
        desenha_frame_personagem(folha, offset_x, 0, pulando=True)

    pygame.image.save(folha, SPRITESHEET_PATH)


def fatia_spritesheet(folha):
    frames_andar = []
    frames_pulo = []
    for indice in range(NUM_FRAMES_ANDAR):
        rect = pygame.Rect(indice * LARGURA_FRAME, 0, LARGURA_FRAME, ALTURA_FRAME)
        frames_andar.append(folha.subsurface(rect).copy())
    for indice in range(NUM_FRAMES_PULO):
        rect = pygame.Rect(
            (NUM_FRAMES_ANDAR + indice) * LARGURA_FRAME, 0, LARGURA_FRAME, ALTURA_FRAME
        )
        frames_pulo.append(folha.subsurface(rect).copy())
    return frames_andar, frames_pulo


if not os.path.exists(SPRITESHEET_PATH):
    gera_e_salva_spritesheet()
folha_personagem = pygame.image.load(SPRITESHEET_PATH).convert_alpha()
frames_andar, frames_pulo = fatia_spritesheet(folha_personagem)


nuvens = [
    {"x": 100, "y": 90, "velocidade": 30},
    {"x": 500, "y": 150, "velocidade": 22},
    {"x": 900, "y": 70, "velocidade": 38},
    {"x": 1150, "y": 180, "velocidade": 26},
]


def desenha_nuvem(x, y):
    x = int(x)
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 28)
    pygame.draw.circle(screen, (255, 255, 255), (x + 30, y), 32)
    pygame.draw.circle(screen, (255, 255, 255), (x + 60, y), 26)
    pygame.draw.circle(screen, (255, 255, 255), (x + 30, y - 18), 24)


def atualiza_nuvens(delta_tempo):
    for nuvem in nuvens:
        nuvem["x"] += nuvem["velocidade"] * delta_tempo
        if nuvem["x"] > LARGURA + 80:
            nuvem["x"] = -120


NUM_PARTICULAS = 40
fogos = []


def cria_fogo(x, y):
    cor_base = (
        random.randint(180, 255),
        random.randint(100, 255),
        random.randint(80, 255),
    )
    for _ in range(NUM_PARTICULAS):
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(140, 320)
        fogos.append(
            {
                "x": x,
                "y": y,
                "velocidade_x": math.cos(angulo) * velocidade,
                "velocidade_y": math.sin(angulo) * velocidade,
                "vida": 1.0,
                "cor": cor_base,
            }
        )


def atualiza_fogos(delta_tempo):
    for particula in fogos:
        particula["x"] += particula["velocidade_x"] * delta_tempo
        particula["y"] += particula["velocidade_y"] * delta_tempo
        particula["velocidade_y"] += 240 * delta_tempo  # gravidade leve
        particula["vida"] -= delta_tempo * 0.9
    fogos[:] = [particula for particula in fogos if particula["vida"] > 0]


def desenha_fogos():
    for particula in fogos:
        raio = max(1, int(particula["vida"] * 5))
        cor = (
            int(particula["cor"][0] * particula["vida"]),
            int(particula["cor"][1] * particula["vida"]),
            int(particula["cor"][2] * particula["vida"]),
        )
        pygame.draw.circle(
            screen, cor, (int(particula["x"]), int(particula["y"])), raio
        )


def desenha_montanhas():
    pygame.draw.polygon(
        screen, (110, 130, 150), [(0, CHAO_Y), (250, 300), (480, CHAO_Y)]
    )
    pygame.draw.polygon(
        screen, (90, 110, 130), [(300, CHAO_Y), (600, 260), (900, CHAO_Y)]
    )
    pygame.draw.polygon(
        screen, (110, 130, 150), [(750, CHAO_Y), (1050, 320), (1280, CHAO_Y)]
    )


def desenha_chao():
    pygame.draw.rect(screen, (90, 160, 70), (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
    pygame.draw.rect(screen, (60, 130, 50), (0, CHAO_Y, LARGURA, 8))


VELOCIDADE_ANDAR = 260
VELOCIDADE_FRAME = 12
FORCA_PULO = -650
GRAVIDADE = 1700

personagem = {
    "x": 200.0,
    "y": float(CHAO_Y - ALTURA_FRAME),
    "velocidade_y": 0.0,
    "direcao": 1,  # 1 = direita, -1 = esquerda
    "frame": 0.0,
    "andando": False,
    "pulando": False,
}


def atualiza_personagem(delta_tempo, keys):
    personagem["andando"] = False

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        personagem["x"] += VELOCIDADE_ANDAR * delta_tempo
        personagem["direcao"] = 1
        personagem["andando"] = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        personagem["x"] -= VELOCIDADE_ANDAR * delta_tempo
        personagem["direcao"] = -1
        personagem["andando"] = True

    # gravidade
    personagem["velocidade_y"] += GRAVIDADE * delta_tempo
    personagem["y"] += personagem["velocidade_y"] * delta_tempo
    chao_topo = CHAO_Y - ALTURA_FRAME
    if personagem["y"] >= chao_topo:
        personagem["y"] = chao_topo
        personagem["velocidade_y"] = 0
        personagem["pulando"] = False

    # limites laterais
    personagem["x"] = max(0, min(LARGURA - LARGURA_FRAME, personagem["x"]))

    # avanca frame da animacao de andar
    if personagem["andando"] and not personagem["pulando"]:
        personagem["frame"] = (
            personagem["frame"] + VELOCIDADE_FRAME * delta_tempo
        ) % NUM_FRAMES_ANDAR
    elif not personagem["andando"] and not personagem["pulando"]:
        personagem["frame"] = 0


def pular():
    if not personagem["pulando"]:
        personagem["velocidade_y"] = FORCA_PULO
        personagem["pulando"] = True


def desenha_personagem():
    if personagem["pulando"]:
        # escolhe frame de pulo pela velocidade vertical
        proporcao = (FORCA_PULO - personagem["velocidade_y"]) / (2 * FORCA_PULO)
        indice = max(0, min(NUM_FRAMES_PULO - 1, int(proporcao * NUM_FRAMES_PULO)))
        sprite = frames_pulo[indice]
    else:
        sprite = frames_andar[int(personagem["frame"])]

    if personagem["direcao"] == -1:
        sprite = pygame.transform.flip(sprite, True, False)

    screen.blit(sprite, (int(personagem["x"]), int(personagem["y"])))


def desenha_dicas():
    titulo = fonte_grande.render("Atividade 11 - Animacoes", True, (30, 30, 30))
    screen.blit(titulo, (20, 18))

    dicas = [
        "as nuvens vao passando sozinhas no ceu...",
        "segure as setas (ou A/D) e o boneco sai andando",
        "pula com seta pra cima ou W",
        "aperta espaco ou clica em qualquer lugar pra soltar fogos",
    ]
    for indice, linha in enumerate(dicas):
        texto = fonte.render(linha, True, (40, 40, 40))
        screen.blit(texto, (20, 60 + indice * 26))


running = True
while running:
    delta_tempo = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cria_fogo(
                    int(personagem["x"] + LARGURA_FRAME // 2),
                    int(personagem["y"] + ALTURA_FRAME // 2),
                )
            elif event.key in (pygame.K_UP, pygame.K_w):
                pular()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cria_fogo(event.pos[0], event.pos[1])

    keys = pygame.key.get_pressed()

    atualiza_nuvens(delta_tempo)
    atualiza_personagem(delta_tempo, keys)
    atualiza_fogos(delta_tempo)

    screen.fill((140, 200, 245))
    for nuvem in nuvens:
        desenha_nuvem(nuvem["x"], nuvem["y"])
    desenha_montanhas()
    desenha_chao()
    desenha_personagem()
    desenha_fogos()
    desenha_dicas()

    pygame.display.update()
