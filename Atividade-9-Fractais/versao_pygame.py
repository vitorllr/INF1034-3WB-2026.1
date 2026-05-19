import math
import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 9 - Fractais")
fonte_grande = pygame.font.SysFont("Arial", 36)
fonte = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()

CANVAS_Y = 70
CANVAS_H = ALTURA - 70 - 140
canvas = pygame.Surface((LARGURA, CANVAS_H))


def desenha_triangulo(surf, p1, p2, p3, cor, espessura):
    pygame.draw.lines(surf, cor, True, [p1, p2, p3], espessura)


#  FRACTAL MEDIO


def coleta_arvore(segs, x, y, comprimento, angulo, abertura, profundidade):
    if profundidade == 0 or comprimento < 2:
        return
    x2 = x + comprimento * math.cos(angulo)
    y2 = y + comprimento * math.sin(angulo)
    t = profundidade / 10
    cor = (
        int(220 * t + 255 * (1 - t)),
        int(120 * t + 200 * (1 - t)),
        int(40 * t + 80 * (1 - t)),
    )
    segs.append(((x, y), (x2, y2), cor, max(1, profundidade // 2)))
    novo = comprimento * 0.72
    coleta_arvore(segs, x2, y2, novo, angulo - abertura, abertura, profundidade - 1)
    coleta_arvore(segs, x2, y2, novo, angulo, abertura, profundidade - 1)
    coleta_arvore(segs, x2, y2, novo, angulo + abertura, abertura, profundidade - 1)


#  FRACTAL DIFICIL
def coleta_koch(segs, p1, p2, nivel, cor):
    if nivel == 0:
        segs.append((p1, p2, cor, 2))
        return
    dx = (p2[0] - p1[0]) / 3
    dy = (p2[1] - p1[1]) / 3
    a = (p1[0] + dx, p1[1] + dy)
    b = (p1[0] + 2 * dx, p1[1] + 2 * dy)
    ang = math.atan2(dy, dx) - math.radians(60)
    comp = math.hypot(dx, dy)
    pico = (a[0] + comp * math.cos(ang), a[1] + comp * math.sin(ang))
    coleta_koch(segs, p1, a, nivel - 1, cor)
    coleta_koch(segs, a, pico, nivel - 1, cor)
    coleta_koch(segs, pico, b, nivel - 1, cor)
    coleta_koch(segs, b, p2, nivel - 1, cor)


def coleta_floco(segs, cx, cy, tamanho, nivel, cor):
    h = tamanho / math.sqrt(3)
    p1 = (cx, cy - h)
    p2 = (cx + tamanho / 2, cy + h / 2)
    p3 = (cx - tamanho / 2, cy + h / 2)
    if nivel == 0:
        desenha_triangulo(canvas, p1, p2, p3, cor, 2)
        segs.append((p1, p2, cor, 2))
        segs.append((p2, p3, cor, 2))
        segs.append((p3, p1, cor, 2))
        return
    coleta_koch(segs, p1, p2, nivel, cor)
    coleta_koch(segs, p2, p3, nivel, cor)
    coleta_koch(segs, p3, p1, nivel, cor)


#  slider
def desenha_slider(surf, sl, ativo):
    pygame.draw.rect(
        surf, (180, 180, 180), (sl["x"], sl["y"], sl["w"], 8), border_radius=4
    )
    prop = (sl["valor"] - sl["vmin"]) / (sl["vmax"] - sl["vmin"])
    hx = sl["x"] + int(prop * sl["w"])
    pygame.draw.rect(
        surf, (90, 140, 220), (sl["x"], sl["y"], hx - sl["x"], 8), border_radius=4
    )
    cor = (200, 70, 50) if ativo else (40, 90, 180)
    pygame.draw.circle(surf, cor, (hx, sl["y"] + 4), 12)
    txt = fonte.render(f"{sl['rotulo']}: {int(sl['valor'])}", True, (30, 30, 30))
    surf.blit(txt, (sl["x"], sl["y"] - 28))


def mouse_no_slider(sl, mx, my):
    return (
        sl["x"] - 8 <= mx <= sl["x"] + sl["w"] + 8
        and sl["y"] - 12 <= my <= sl["y"] + 18
    )


def atualiza_slider(sl, mx):
    mx = max(sl["x"], min(sl["x"] + sl["w"], mx))
    prop = (mx - sl["x"]) / sl["w"]
    sl["valor"] = int(round(sl["vmin"] + prop * (sl["vmax"] - sl["vmin"])))


sl_sierp_n = {
    "x": 220,
    "y": ALTURA - 80,
    "w": 700,
    "vmin": 1000,
    "vmax": 40000,
    "valor": 15000,
    "rotulo": "Pontos",
}
sl_arv_prof = {
    "x": 220,
    "y": ALTURA - 100,
    "w": 400,
    "vmin": 1,
    "vmax": 9,
    "valor": 7,
    "rotulo": "Profundidade",
}
sl_arv_abert = {
    "x": 700,
    "y": ALTURA - 100,
    "w": 400,
    "vmin": 5,
    "vmax": 60,
    "valor": 28,
    "rotulo": "Abertura (graus)",
}
sl_koch = {
    "x": 220,
    "y": ALTURA - 80,
    "w": 700,
    "vmin": 0,
    "vmax": 5,
    "valor": 3,
    "rotulo": "Nivel",
}

FUNDOS = {
    "sierpinski": (250, 248, 240),
    "arvore": (20, 25, 35),
    "koch": (245, 250, 255),
}

# estado da animacao
tela = "sierpinski"
segmentos = []
pontos_sierp = []
indice = 0
desenhando = False
slider_ativo = None


def preparar():
    """Limpa o canvas e gera a lista de operacoes do fractal atual."""
    global segmentos, pontos_sierp, indice, desenhando
    canvas.fill(FUNDOS[tela])
    indice = 0
    desenhando = True
    segmentos = []
    pontos_sierp = []
    w, h = canvas.get_size()

    if tela == "sierpinski":
        #  FRACTAL FACIL

        alvos = [(w // 2, 40), (60, h - 60), (w - 60, h - 60)]
        x, y = w // 2, h // 2
        for i in range(sl_sierp_n["valor"]):
            px, py = alvos[random.randint(0, 2)]
            x, y = (x + px) / 2, (y + py) / 2
            pontos_sierp.append((int(x), int(y), i / sl_sierp_n["valor"]))

    elif tela == "arvore":
        coleta_arvore(
            segmentos,
            w // 2,
            h - 20,
            110,
            -math.pi / 2,
            math.radians(sl_arv_abert["valor"]),
            sl_arv_prof["valor"],
        )

    elif tela == "koch":
        coleta_floco(
            segmentos, w // 2, h // 2 + 30, 460, sl_koch["valor"], (30, 90, 180)
        )


def avancar_animacao():
    """Desenha as proximas operacoes no canvas (anima o fractal)."""
    global indice, desenhando
    if not desenhando:
        return
    if tela == "sierpinski":
        total = len(pontos_sierp)

        quantos = max(1, total // 360)
        fim = min(indice + quantos, total)
        for i in range(indice, fim):
            px, py, t = pontos_sierp[i]
            cor = (int(220 - 100 * t), int(60 + 120 * t), int(80 + 100 * t))
            canvas.set_at((px, py), cor)
        indice = fim
        if indice >= total:
            desenhando = False
    else:
        total = len(segmentos)
        quantos = max(1, total // 360)
        fim = min(indice + quantos, total)
        for i in range(indice, fim):
            p1, p2, cor, esp = segmentos[i]
            pygame.draw.line(canvas, cor, p1, p2, esp)
        indice = fim
        if indice >= total:
            desenhando = False


abas = [
    ("1 - Sierpinski", "sierpinski", (200, 90, 90)),
    ("2 - Arvore", "arvore", (90, 160, 90)),
    ("3 - Koch", "koch", (90, 120, 200)),
]


preparar()

running = True
while running:
    screen.fill((240, 240, 245))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                tela = "sierpinski"
                preparar()
            elif ev.key == pygame.K_2:
                tela = "arvore"
                preparar()
            elif ev.key == pygame.K_3:
                tela = "koch"
                preparar()

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos
            trocou = False
            for i, (rotulo, nome, cor) in enumerate(abas):
                rx = 20 + i * 200
                if rx <= mx <= rx + 180 and 15 <= my <= 60:
                    tela = nome
                    preparar()
                    trocou = True
            if not trocou and not desenhando:
                cand = None
                if tela == "sierpinski" and mouse_no_slider(sl_sierp_n, mx, my):
                    cand = sl_sierp_n
                elif tela == "arvore" and mouse_no_slider(sl_arv_prof, mx, my):
                    cand = sl_arv_prof
                elif tela == "arvore" and mouse_no_slider(sl_arv_abert, mx, my):
                    cand = sl_arv_abert
                elif tela == "koch" and mouse_no_slider(sl_koch, mx, my):
                    cand = sl_koch
                if cand is not None:
                    slider_ativo = cand
                    atualiza_slider(cand, mx)
                    preparar()

        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            slider_ativo = None

        elif ev.type == pygame.MOUSEMOTION and slider_ativo is not None:
            atualiza_slider(slider_ativo, ev.pos[0])
            preparar()

    avancar_animacao()

    screen.blit(canvas, (0, CANVAS_Y))

    # abas no topo
    for i, (rotulo, nome, cor) in enumerate(abas):
        rx = 20 + i * 200
        c = cor if nome == tela else (200, 200, 200)
        pygame.draw.rect(screen, c, (rx, 15, 180, 45), border_radius=6)
        pygame.draw.rect(screen, (40, 40, 40), (rx, 15, 180, 45), 2, border_radius=6)
        t = fonte.render(rotulo, True, (255, 255, 255))
        screen.blit(t, (rx + 90 - t.get_width() // 2, 25))

    # painel de sliders
    pygame.draw.rect(screen, (225, 225, 230), (0, ALTURA - 140, LARGURA, 140))
    pygame.draw.line(
        screen, (180, 180, 180), (0, ALTURA - 140), (LARGURA, ALTURA - 140), 2
    )
    if desenhando:
        status = "Desenhando..."
        cor_status = (200, 90, 60)
    else:
        status = "Pronto. Arraste os sliders pra alterar o fractal."
        cor_status = (80, 130, 80)
    dica = fonte.render(f"{status}   |   Teclas 1/2/3 trocam fractal", True, cor_status)
    screen.blit(dica, (20, ALTURA - 132))

    if tela == "sierpinski":
        desenha_slider(screen, sl_sierp_n, slider_ativo is sl_sierp_n)
    elif tela == "arvore":
        desenha_slider(screen, sl_arv_prof, slider_ativo is sl_arv_prof)
        desenha_slider(screen, sl_arv_abert, slider_ativo is sl_arv_abert)
    elif tela == "koch":
        desenha_slider(screen, sl_koch, slider_ativo is sl_koch)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
