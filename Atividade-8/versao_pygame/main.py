import os
import subprocess
import sys

import pygame


def valida_dominio_email(email):
    return email[-8:] == "@puc.com"


def possui_maiuscula(palavra):
    for c in palavra:
        if c.isupper():
            return True
    return False


def possui_minuscula(palavra):
    for c in palavra:
        if c.islower():
            return True
    return False


def possui_numero(palavra):
    for c in palavra:
        if c.isdigit():
            return True
    return False


def avalia_senha(senha):
    check_tamanho = len(senha) >= 8
    check_maiuscula = possui_maiuscula(senha)
    check_minuscula = possui_minuscula(senha)
    check_numero = possui_numero(senha)

    return check_tamanho and check_maiuscula and check_minuscula and check_numero


def criptografa_a_senha(senha):
    senha_criptografada = ""
    for char in senha:
        if char.isdigit():
            ref = ord("0")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto + 3
            pos_cesar = pos_cesar % 10
            letra_cifrada = chr(ref + pos_cesar)
            senha_criptografada += letra_cifrada
        elif "A" <= char <= "Z":
            ref = ord("A")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto + 3
            pos_cesar = pos_cesar % 26
            letra_cifrada = chr(ref + pos_cesar)
            senha_criptografada += letra_cifrada
        elif "a" <= char <= "z":
            ref = ord("a")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto + 3
            pos_cesar = pos_cesar % 26
            letra_cifrada = chr(ref + pos_cesar)
            senha_criptografada += letra_cifrada
        else:
            senha_criptografada += char
    return senha_criptografada


def decriptografa_a_senha(senha):
    senha_decriptografada = ""
    for char in senha:
        if char.isdigit():
            ref = ord("0")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto - 3
            pos_cesar = pos_cesar % 10
            letra = chr(ref + pos_cesar)
            senha_decriptografada += letra
        elif "A" <= char <= "Z":
            ref = ord("A")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto - 3
            pos_cesar = pos_cesar % 26
            letra = chr(ref + pos_cesar)
            senha_decriptografada += letra
        elif "a" <= char <= "z":
            ref = ord("a")
            ascii_char = ord(char)
            pos_alfabeto = ascii_char - ref
            pos_cesar = pos_alfabeto - 3
            pos_cesar = pos_cesar % 26
            letra = chr(ref + pos_cesar)
            senha_decriptografada += letra
        else:
            senha_decriptografada += char
    return senha_decriptografada


# Testes das funcoes
print(f"{valida_dominio_email('vitor@puc.com')}")
print(f"{avalia_senha('Senha1@aaaa')}")
print(f"{criptografa_a_senha('Senha123@')}")
print(f"{decriptografa_a_senha(criptografa_a_senha('Senha123@'))}")


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Login")
fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()


PASTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
projetos = {
    1: ("Casinha", os.path.join(PASTA_BASE, "Atividade - 6 - La Casita Ultimate")),
    2: ("Jogo da Forca", os.path.join(PASTA_BASE, "Atividade-7")),
    3: ("Pedra, Papel e Tesoura", os.path.join(PASTA_BASE, "Atividade-7", "ppt")),
}


email = ""
senha = ""
campo_ativo = "email"
mensagem = "Faca o login"
tela = "login"
senha_cripto = ""
senha_decripto = ""

running = True

while running:
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and tela == "login":
            if event.key == pygame.K_TAB:
                if campo_ativo == "email":
                    campo_ativo = "senha"
                else:
                    campo_ativo = "email"
            elif event.key == pygame.K_BACKSPACE:
                if campo_ativo == "email" and len(email) > 0:
                    email = email[:-1]
                elif campo_ativo == "senha" and len(senha) > 0:
                    senha = senha[:-1]
            elif event.key == pygame.K_RETURN:
                if not valida_dominio_email(email):
                    mensagem = "E-mail invalido (precisa terminar em @puc.com)"
                elif not avalia_senha(senha):
                    mensagem = (
                        "Senha fraca (min 8 chars, maiuscula, minuscula e numero)"
                    )
                else:
                    senha_cripto = criptografa_a_senha(senha)
                    senha_decripto = decriptografa_a_senha(senha_cripto)
                    mensagem = "Login OK! Escolha um projeto"
                    tela = "menu"
            else:
                char = event.unicode
                if char != "" and char.isprintable():
                    if campo_ativo == "email":
                        email += char
                    elif campo_ativo == "senha":
                        senha += char

        elif event.type == pygame.KEYDOWN and tela == "menu":
            if event.key == pygame.K_1:
                nome, pasta = projetos[1]
                subprocess.Popen([sys.executable, "main.py"], cwd=pasta)
            elif event.key == pygame.K_2:
                nome, pasta = projetos[2]
                subprocess.Popen([sys.executable, "main.py"], cwd=pasta)
            elif event.key == pygame.K_3:
                nome, pasta = projetos[3]
                subprocess.Popen([sys.executable, "main.py"], cwd=pasta)

    if tela == "login":
        titulo = fonte.render("Login", True, "black")
        screen.blit(titulo, (screen.get_width() // 2 - titulo.get_width() // 2, 80))

        cor_email = "blue" if campo_ativo == "email" else "gray"
        label_email = fonte_pequena.render("Email:", True, "black")
        screen.blit(label_email, (300, 200))
        pygame.draw.rect(screen, cor_email, pygame.Rect(300, 240, 680, 50), 3)
        texto_email = fonte_pequena.render(email, True, "black")
        screen.blit(texto_email, (310, 245))

        cor_senha = "blue" if campo_ativo == "senha" else "gray"
        label_senha = fonte_pequena.render("Senha:", True, "black")
        screen.blit(label_senha, (300, 320))
        pygame.draw.rect(screen, cor_senha, pygame.Rect(300, 360, 680, 50), 3)
        texto_senha = fonte_pequena.render("*" * len(senha), True, "black")
        screen.blit(texto_senha, (310, 365))

        instrucao = fonte_pequena.render(
            "TAB troca de campo, ENTER envia", True, "gray"
        )
        screen.blit(
            instrucao,
            (screen.get_width() // 2 - instrucao.get_width() // 2, 450),
        )

        texto_mensagem = fonte_pequena.render(mensagem, True, "blue")
        screen.blit(
            texto_mensagem,
            (screen.get_width() // 2 - texto_mensagem.get_width() // 2, 520),
        )

    elif tela == "menu":
        titulo = fonte.render("Menu - Escolha um projeto", True, "black")
        screen.blit(titulo, (screen.get_width() // 2 - titulo.get_width() // 2, 80))

        for numero in projetos:
            nome, _ = projetos[numero]
            texto = fonte_pequena.render(f"{numero} - {nome}", True, "black")
            screen.blit(
                texto,
                (screen.get_width() // 2 - texto.get_width() // 2, 200 + numero * 60),
            )

        info_cripto = fonte_pequena.render(
            f"Senha criptografada: {senha_cripto}", True, "green"
        )
        info_decripto = fonte_pequena.render(
            f"Senha decriptografada: {senha_decripto}", True, "green"
        )
        screen.blit(
            info_cripto,
            (screen.get_width() // 2 - info_cripto.get_width() // 2, 500),
        )
        screen.blit(
            info_decripto,
            (screen.get_width() // 2 - info_decripto.get_width() // 2, 540),
        )

        texto_mensagem = fonte_pequena.render(mensagem, True, "blue")
        screen.blit(
            texto_mensagem,
            (screen.get_width() // 2 - texto_mensagem.get_width() // 2, 600),
        )

    pygame.display.update()
    clock.tick(60)

pygame.quit()
