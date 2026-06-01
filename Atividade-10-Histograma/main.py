import random

import pygame

pygame.init()
LARGURA, ALTURA = 1280, 720
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Atividade 10 - Histogramas")
fonte_grande = pygame.font.SysFont("Arial", 30)
fonte = pygame.font.SysFont("Arial", 20)
fonte_pequena = pygame.font.SysFont("Arial", 15)
clock = pygame.time.Clock()

# area onde o histograma eh desenhado fica entre o topo (abas) e o painel inferior
CANVAS_Y = 75
PAINEL_H = 200
CANVAS_H = ALTURA - CANVAS_Y - PAINEL_H
canvas = pygame.Surface((LARGURA, CANVAS_H))


def cor_aleatoria():
    """Gera uma cor RGB aleatoria evitando tons muito claros ou muito escuros."""
    return (random.randint(60, 220), random.randint(60, 220), random.randint(60, 220))


#  HISTOGRAMA 1 - lista aleatoria (10 faixas)


def gerar_lista_aleatoria():
    """Cria uma lista com pelo menos 50 numeros aleatorios entre 0 e 99."""
    n = random.randint(60, 120)
    return [random.randint(0, 99) for _ in range(n)]


def faixas_h1():
    """10 faixas de tamanho 10, cobrindo 0..99."""
    return [(i * 10, i * 10 + 9, f"{i * 10}-{i * 10 + 9}") for i in range(10)]


#  HISTOGRAMA 2 - lista estatica (6 faixas)
# lista fixa "como mostrada em sala", com 60 elementos
LISTA_ESTATICA = [
    23,
    45,
    12,
    67,
    89,
    34,
    56,
    78,
    90,
    21,
    43,
    65,
    87,
    19,
    31,
    53,
    75,
    97,
    28,
    50,
    72,
    94,
    16,
    38,
    60,
    82,
    4,
    26,
    48,
    70,
    92,
    14,
    36,
    58,
    80,
    2,
    24,
    46,
    68,
    88,
    10,
    32,
    54,
    76,
    98,
    7,
    29,
    51,
    73,
    95,
    18,
    40,
    62,
    84,
    6,
    27,
    49,
    71,
    93,
    15,
]


def faixas_h2():
    """6 faixas para o histograma estatico (numero diferente das outras telas)."""
    return [
        (0, 16, "0-16"),
        (17, 33, "17-33"),
        (34, 50, "34-50"),
        (51, 67, "51-67"),
        (68, 84, "68-84"),
        (85, 100, "85-100"),
    ]


def gerar_contagens_h2():
    """Contagens aleatorias por faixa garantindo que a soma nao
    ultrapasse o tamanho de LISTA_ESTATICA."""
    total = len(LISTA_ESTATICA)
    n = len(faixas_h2())
    contagens = [random.randint(2, 18) for _ in range(n)]
    # remove unidades aleatoriamente ate a soma caber em "total"
    while sum(contagens) > total:
        idx = random.randint(0, n - 1)
        if contagens[idx] > 0:
            contagens[idx] -= 1
    return contagens


#  HISTOGRAMA 3 - lista do usuario via pygame (8 faixas)


def faixas_h3():
    """8 faixas de tamanho 25 cobrindo 0..199."""
    return [(i * 25, i * 25 + 24, f"{i * 25}-{i * 25 + 24}") for i in range(8)]


#  funcao generica de contagem


def contar_em_faixas(lista, faixas):
    """Conta quantos valores da lista caem em cada faixa (inclusiva)."""
    contagens = [0] * len(faixas)
    for v in lista:
        for i, (lo, hi, _) in enumerate(faixas):
            if lo <= v <= hi:
                contagens[i] += 1
                break
    return contagens


#  desenho do histograma


def desenha_histograma(
    surf, contagens, rotulos, cores, titulo, eixo_x="Faixas", eixo_y="Frequencia"
):
    """Desenha o histograma na surface com eixos, marcacoes,
    barras coloridas e rotulos."""
    surf.fill((252, 252, 248))
    w, h = surf.get_size()

    # margens dentro da surface
    marg_esq, marg_dir = 95, 50
    marg_topo, marg_baixo = 55, 75
    area_w = w - marg_esq - marg_dir
    area_h = h - marg_topo - marg_baixo
    x0 = marg_esq
    y0 = marg_topo + area_h  # baseline (eixo x)

    # titulo
    t = fonte_grande.render(titulo, True, (25, 25, 25))
    surf.blit(t, (w // 2 - t.get_width() // 2, 10))

    # se nao houver dado, evita divisao por zero
    maximo = max(contagens) if contagens and max(contagens) > 0 else 1

    # grid + marcacoes do eixo y (5 divisoes)
    divisoes = 5
    for i in range(divisoes + 1):
        valor = maximo * i / divisoes
        py = y0 - i * area_h / divisoes
        pygame.draw.line(surf, (225, 225, 230), (x0 + 1, py), (x0 + area_w, py), 1)
        pygame.draw.line(surf, (30, 30, 30), (x0 - 6, py), (x0, py), 2)
        vt = fonte_pequena.render(f"{int(round(valor))}", True, (40, 40, 40))
        surf.blit(vt, (x0 - 10 - vt.get_width(), py - 8))

    # eixos x e y com setinhas nas pontas
    pygame.draw.line(surf, (25, 25, 25), (x0, marg_topo - 8), (x0, y0), 3)
    pygame.draw.line(surf, (25, 25, 25), (x0, y0), (x0 + area_w + 8, y0), 3)
    pygame.draw.polygon(
        surf,
        (25, 25, 25),
        [
            (x0, marg_topo - 14),
            (x0 - 6, marg_topo - 6),
            (x0 + 6, marg_topo - 6),
        ],
    )
    pygame.draw.polygon(
        surf,
        (25, 25, 25),
        [
            (x0 + area_w + 14, y0),
            (x0 + area_w + 6, y0 - 6),
            (x0 + area_w + 6, y0 + 6),
        ],
    )

    # barras
    n = len(contagens)
    if n > 0:
        espaco = area_w / n
        larg_barra = espaco * 0.78
        for i, c in enumerate(contagens):
            bx = x0 + espaco * i + (espaco - larg_barra) / 2
            bh = (c / maximo) * area_h if maximo > 0 else 0
            by = y0 - bh
            pygame.draw.rect(surf, cores[i], (bx, by, larg_barra, bh))
            pygame.draw.rect(surf, (25, 25, 25), (bx, by, larg_barra, bh), 2)
            # tick no eixo x sob cada barra
            tick_x = bx + larg_barra / 2
            pygame.draw.line(surf, (30, 30, 30), (tick_x, y0), (tick_x, y0 + 6), 2)
            # rotulo da faixa abaixo
            rx = fonte_pequena.render(rotulos[i], True, (40, 40, 40))
            surf.blit(rx, (bx + larg_barra / 2 - rx.get_width() / 2, y0 + 10))
            # valor da contagem em cima da barra
            if c > 0:
                vt = fonte_pequena.render(str(c), True, (25, 25, 25))
                surf.blit(vt, (bx + larg_barra / 2 - vt.get_width() / 2, by - 18))

    # rotulo do eixo x
    tx = fonte.render(eixo_x, True, (30, 30, 30))
    surf.blit(tx, (x0 + area_w / 2 - tx.get_width() / 2, h - 28))
    # rotulo do eixo y (rotacionado 90 graus)
    ty = fonte.render(eixo_y, True, (30, 30, 30))
    ty = pygame.transform.rotate(ty, 90)
    surf.blit(ty, (18, marg_topo + area_h / 2 - ty.get_height() / 2))


#  estado da aplicacao

# histograma 1
lista_h1 = gerar_lista_aleatoria()
cores_h1 = [cor_aleatoria() for _ in faixas_h1()]
contagens_h1 = contar_em_faixas(lista_h1, faixas_h1())

# histograma 2
contagens_h2 = gerar_contagens_h2()
cores_h2 = [cor_aleatoria() for _ in faixas_h2()]

# histograma 3
lista_h3 = []
cores_h3 = [cor_aleatoria() for _ in faixas_h3()]
texto_input = ""
mensagem_h3 = "Digite um numero (0-199) e pressione Enter"

tela = 0  # 0=h1, 1=h2, 2=h3

abas = [
    ("1 - Aleatoria", (200, 90, 90)),
    ("2 - Estatica", (90, 160, 90)),
    ("3 - Sua lista", (90, 120, 200)),
]

# botoes de navegacao no topo (setas)
botao_esq = pygame.Rect(LARGURA - 130, 20, 50, 45)
botao_dir = pygame.Rect(LARGURA - 70, 20, 50, 45)

# botoes no painel inferior
input_rect = pygame.Rect(40, ALTURA - PAINEL_H + 90, 220, 42)
botao_add = pygame.Rect(280, ALTURA - PAINEL_H + 90, 130, 42)
botao_limpar = pygame.Rect(430, ALTURA - PAINEL_H + 90, 150, 42)
botao_rerolar_h1 = pygame.Rect(40, ALTURA - PAINEL_H + 90, 260, 42)
botao_rerolar_h2 = pygame.Rect(40, ALTURA - PAINEL_H + 90, 290, 42)


def desenha_topo():
    """Desenha as 3 abas e os botoes de seta na parte de cima."""
    for i, (rotulo, cor) in enumerate(abas):
        rx = 20 + i * 230
        c = cor if i == tela else (190, 190, 195)
        pygame.draw.rect(screen, c, (rx, 20, 210, 45), border_radius=6)
        pygame.draw.rect(screen, (40, 40, 40), (rx, 20, 210, 45), 2, border_radius=6)
        cor_txt = (255, 255, 255) if i == tela else (50, 50, 50)
        t = fonte.render(rotulo, True, cor_txt)
        screen.blit(t, (rx + 105 - t.get_width() // 2, 32))

    # botao seta esquerda
    pygame.draw.rect(screen, (220, 220, 225), botao_esq, border_radius=6)
    pygame.draw.rect(screen, (40, 40, 40), botao_esq, 2, border_radius=6)
    pygame.draw.polygon(
        screen,
        (40, 40, 40),
        [
            (botao_esq.right - 15, botao_esq.top + 10),
            (botao_esq.right - 15, botao_esq.bottom - 10),
            (botao_esq.left + 14, botao_esq.centery),
        ],
    )
    # botao seta direita
    pygame.draw.rect(screen, (220, 220, 225), botao_dir, border_radius=6)
    pygame.draw.rect(screen, (40, 40, 40), botao_dir, 2, border_radius=6)
    pygame.draw.polygon(
        screen,
        (40, 40, 40),
        [
            (botao_dir.left + 15, botao_dir.top + 10),
            (botao_dir.left + 15, botao_dir.bottom - 10),
            (botao_dir.right - 14, botao_dir.centery),
        ],
    )


def desenha_botao(rect, texto, cor_fundo=(220, 220, 225), cor_texto=(30, 30, 30)):
    """Desenha um botao retangular com texto centralizado."""
    pygame.draw.rect(screen, cor_fundo, rect, border_radius=6)
    pygame.draw.rect(screen, (40, 40, 40), rect, 2, border_radius=6)
    t = fonte.render(texto, True, cor_texto)
    screen.blit(
        t, (rect.centerx - t.get_width() // 2, rect.centery - t.get_height() // 2)
    )


def desenha_painel_h1():
    info = (
        f"Lista aleatoria com {len(lista_h1)} numeros entre 0 e 99   |   "
        "10 faixas de tamanho 10"
    )
    t = fonte.render(info, True, (40, 40, 40))
    screen.blit(t, (40, ALTURA - PAINEL_H + 25))
    dica = fonte_pequena.render(
        "Clique para sortear uma nova lista. Cada faixa tem cor aleatoria.",
        True,
        (90, 90, 90),
    )
    screen.blit(dica, (40, ALTURA - PAINEL_H + 55))
    desenha_botao(botao_rerolar_h1, "Sortear nova lista", (240, 200, 200))


def desenha_painel_h2():
    total = len(LISTA_ESTATICA)
    info = (
        f"Lista estatica com {total} elementos   |   6 faixas   |   "
        f"soma das contagens <= {total}"
    )
    t = fonte.render(info, True, (40, 40, 40))
    screen.blit(t, (40, ALTURA - PAINEL_H + 25))
    soma = sum(contagens_h2)
    dica = fonte_pequena.render(
        f"Soma atual das faixas: {soma} / {total}   (contagens sorteadas aleatoriamente)",
        True,
        (90, 90, 90),
    )
    screen.blit(dica, (40, ALTURA - PAINEL_H + 55))
    desenha_botao(botao_rerolar_h2, "Sortear novas contagens", (200, 230, 200))


def desenha_painel_h3():
    info = f"Sua lista: {len(lista_h3)} numeros   |   8 faixas de tamanho 25 (0-199)"
    t = fonte.render(info, True, (40, 40, 40))
    screen.blit(t, (40, ALTURA - PAINEL_H + 25))
    msg = fonte_pequena.render(mensagem_h3, True, (90, 90, 90))
    screen.blit(msg, (40, ALTURA - PAINEL_H + 55))

    # caixa de input
    pygame.draw.rect(screen, (255, 255, 255), input_rect, border_radius=4)
    pygame.draw.rect(screen, (60, 90, 180), input_rect, 2, border_radius=4)
    # cursor pisca a cada meio segundo
    cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
    txt = fonte.render(texto_input + cursor, True, (20, 20, 20))
    screen.blit(txt, (input_rect.x + 10, input_rect.y + 9))

    desenha_botao(botao_add, "Adicionar", (200, 220, 240))
    desenha_botao(botao_limpar, "Limpar lista", (240, 210, 210))

    # preview dos ultimos valores adicionados
    if lista_h3:
        ultimos = lista_h3[-20:]
        prefixo = "..., " if len(lista_h3) > 20 else ""
        valores = prefixo + ", ".join(str(v) for v in ultimos)
        tl = fonte_pequena.render("Ultimos valores: " + valores, True, (40, 40, 40))
        screen.blit(tl, (600, ALTURA - PAINEL_H + 100))


def adicionar_numero():
    """Tenta converter o texto da caixa em numero e adiciona na lista_h3."""
    global texto_input, mensagem_h3
    if not texto_input:
        mensagem_h3 = "Digite algum numero primeiro"
        return
    try:
        v = int(texto_input)
        if 0 <= v <= 199:
            lista_h3.append(v)
            mensagem_h3 = f"Adicionado: {v}   (total na lista: {len(lista_h3)})"
        else:
            mensagem_h3 = "Numero fora da faixa permitida (0-199)"
    except ValueError:
        mensagem_h3 = "Entrada invalida"
    texto_input = ""


#  loop principal

running = True
while running:
    screen.fill((240, 240, 245))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.KEYDOWN:
            # navegacao por teclas
            if ev.key == pygame.K_LEFT:
                tela = (tela - 1) % 3
            elif ev.key == pygame.K_RIGHT:
                tela = (tela + 1) % 3
            elif ev.key == pygame.K_1:
                tela = 0
            elif ev.key == pygame.K_2:
                tela = 1
            elif ev.key == pygame.K_3:
                tela = 2
            elif tela == 2:
                # entrada de texto so faz sentido na tela 3
                if ev.key == pygame.K_RETURN:
                    adicionar_numero()
                elif ev.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                elif ev.unicode.isdigit() and len(texto_input) < 4:
                    texto_input += ev.unicode

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = ev.pos

            # cliques nas abas
            for i in range(3):
                rx = 20 + i * 230
                if rx <= mx <= rx + 210 and 20 <= my <= 65:
                    tela = i

            # setas
            if botao_esq.collidepoint(mx, my):
                tela = (tela - 1) % 3
            if botao_dir.collidepoint(mx, my):
                tela = (tela + 1) % 3

            # botoes do painel dependem da tela atual
            if tela == 0 and botao_rerolar_h1.collidepoint(mx, my):
                lista_h1 = gerar_lista_aleatoria()
                cores_h1 = [cor_aleatoria() for _ in faixas_h1()]
                contagens_h1 = contar_em_faixas(lista_h1, faixas_h1())

            elif tela == 1 and botao_rerolar_h2.collidepoint(mx, my):
                contagens_h2 = gerar_contagens_h2()
                cores_h2 = [cor_aleatoria() for _ in faixas_h2()]

            elif tela == 2:
                if botao_add.collidepoint(mx, my):
                    adicionar_numero()
                elif botao_limpar.collidepoint(mx, my):
                    lista_h3.clear()
                    mensagem_h3 = "Lista limpa"

    # desenha o histograma da tela atual no canvas
    if tela == 0:
        rotulos = [r for _, _, r in faixas_h1()]
        desenha_histograma(
            canvas,
            contagens_h1,
            rotulos,
            cores_h1,
            "Histograma 1 - Lista Aleatoria (10 faixas)",
        )
    elif tela == 1:
        rotulos = [r for _, _, r in faixas_h2()]
        desenha_histograma(
            canvas,
            contagens_h2,
            rotulos,
            cores_h2,
            "Histograma 2 - Lista Estatica (6 faixas)",
        )
    else:
        contagens = contar_em_faixas(lista_h3, faixas_h3())
        rotulos = [r for _, _, r in faixas_h3()]
        desenha_histograma(
            canvas, contagens, rotulos, cores_h3, "Histograma 3 - Sua Lista (8 faixas)"
        )

    screen.blit(canvas, (0, CANVAS_Y))
    desenha_topo()

    # painel inferior
    pygame.draw.rect(screen, (230, 230, 235), (0, ALTURA - PAINEL_H, LARGURA, PAINEL_H))
    pygame.draw.line(
        screen, (180, 180, 180), (0, ALTURA - PAINEL_H), (LARGURA, ALTURA - PAINEL_H), 2
    )

    if tela == 0:
        desenha_painel_h1()
    elif tela == 1:
        desenha_painel_h2()
    else:
        desenha_painel_h3()

    # dica de navegacao no canto
    dica = fonte_pequena.render(
        "Setas <- ->  ou  teclas 1/2/3  para trocar de histograma",
        True,
        (90, 90, 90),
    )
    screen.blit(dica, (LARGURA - dica.get_width() - 20, ALTURA - 25))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
