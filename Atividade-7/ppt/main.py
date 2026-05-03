import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jogo da Forca")
fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

ASSETS = "../assets/"
opcoes = {1:'pedra', 2:'papel', 3:'tesoura'}

def carregar_imagem(nome, largura=200):
    img = pygame.image.load(ASSETS + nome + ".png")
    proporcao = largura / img.get_width()
    nova_altura = int(img.get_height() * proporcao)
    return pygame.transform.scale(img, (largura, nova_altura))

imagens = {1: carregar_imagem("pedra"), 2: carregar_imagem("papel"), 3: carregar_imagem("tesoura")}


running = True 
game_over = False
mensagem = f"escolha a sua opcao: p(pedra), a(papel), t(tesoura)"
pontos_computador = 0
pontos_jogador = 0
opcao_maquina = None
opcao_jogador = None

def vence(a, b):
    return (a - b) % 3 == 1
    

def compara_opcoes(opcao_maquina, opcao_jogador):
    global pontos_computador, pontos_jogador, mensagem
    desc = f"{opcoes[opcao_maquina]} vs {opcoes[opcao_jogador]}"

    if opcao_maquina == opcao_jogador:
        mensagem = f"{desc} — Empate!"
    elif vence(opcao_maquina, opcao_jogador):
        pontos_computador += 1
        mensagem = f"{desc} — Computador vence!"
    else:
        pontos_jogador += 1
        mensagem = f"{desc} — Jogador vence!"

while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and pontos_jogador < 3 and pontos_computador < 3:

            tecla = event.unicode

            if tecla not in ['p','a','t']:
                mensagem = f"Opcao invalida"
            else:
                opcao_jogador = {'p': 1, 'a': 2, 't': 3}[tecla]
                opcao_maquina = random.randint(1,3)
                    
                compara_opcoes(opcao_maquina,opcao_jogador)
                
                if pontos_computador == 3:
                    mensagem = "O computador venceu! Pressione R para reiniciar."
                elif pontos_jogador == 3:
                    mensagem = "Parabéns!! Você venceu! Pressione R para reiniciar."
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pontos_computador = 0
            pontos_jogador = 0
            opcao_maquina = None
            opcao_jogador = None
            mensagem = "Escolha: p(pedra), a(papel), t(tesoura)"
            
    texto_mensagem = fonte_pequena.render(mensagem, True, 'blue')
    texto_pontuacao_pc = fonte_pequena.render(f"Computador: {pontos_computador}", True, (255, 0, 0))
    texto_pontuacao_jogador = fonte_pequena.render(f"Jogador: {pontos_jogador}", True, (255, 0, 0))

    if opcao_jogador is not None:
        screen.blit(imagens[opcao_jogador], (300, 400))
    if opcao_maquina is not None:
        screen.blit(imagens[opcao_maquina], (800, 400))
    
    screen.blit(texto_mensagem, (screen.get_width()//2 - texto_mensagem.get_width()//2, 300))
    screen.blit(texto_pontuacao_pc, (50, 50))
    screen.blit(texto_pontuacao_jogador, (100, 100))
    

    pygame.display.update()
    clock.tick(60)


