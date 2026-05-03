import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jogo da Forca")
fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

opcoes = {1:'pedra',2:'papel',3:'tesoura'}

running = True 
game_over = False
mensagem = f"escolha a sua opcao: p(pedra), a(papel), t(tesoura)"
pontos_computador = 0
pontos_jogador = 0

while running:
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and pontos_jogador < 3 and pontos_computador < 3:
            
            opcao_maquina = random.randint(1,3)
            opcao_jogador = event.unicode
            
            if opcao_jogador != ['p','a','t']:
                mensagem = f"Opcao invalida"
                
            
            if opcao_jogador == 'p':
                opcao_jogador = 1
            if opcao_jogador == 'a':
                opcao_jogador = 2
            if opcao_jogador == 't':
                opcao_jogador = 3
                

            if opcao_maquina > opcao_jogador:
                pontos_computador += 1
                mensagem = f"deu {opcoes[opcao_maquina]} contra {opcoes[opcao_jogador]}, computador vence"
            elif opcao_maquina < opcao_jogador:
                pontos_jogador += 1
                mensagem = f"deu {opcoes[opcao_maquina]} contra {opcoes[opcao_jogador]}, jogador vence"
            elif opcao_jogador == opcao_maquina:
                mensagem = f"deu {opcoes[opcao_maquina]} contra {opcoes[opcao_jogador]}, ninguem vence"

                
            if pontos_computador == 3 :
                mensagem = f"o computador venceu!"
            elif pontos_jogador == 3:
                mensagem = f"parabens!! Voce venceu!!"
                

        texto_mensagem = fonte_pequena.render(mensagem, True, 'blue')
        texto_pontuacao_pc = fonte_pequena.render(f"Computador: {pontos_computador}", True, (255, 0, 0))
        texto_pontuacao_jogador = fonte_pequena.render(f"Jogador: {pontos_jogador}", True, (255, 0, 0))
        
        screen.blit(texto_mensagem, (screen.get_width()//2 - texto_mensagem.get_width()//2, 300))
        screen.blit(texto_pontuacao_pc, (50, 50))
        screen.blit(texto_pontuacao_jogador, (100, 100))
        
        screen.blit  
    
        pygame.display.update()


