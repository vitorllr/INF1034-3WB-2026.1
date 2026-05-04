
import random 
import pygame
from pygame import key
from pygame import *
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jogo da Forca")
fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()




esportes =[
  "Futebol", "Basquete", "Volei", "Nataçao", "Tenis",
  "Atletismo", "Boxe", "Ciclismo", "Skate", "Surf",
  "Ginastica", "Rugby", "Handebol", "Medalha", "Treinador",
  "Estadio", "Arbitro", "Campeonato", "Corrida", "Olimpiadas"
]

vidas = 6
tentativas = 0
palavra_aleatoria = esportes[random.randint(0,len(esportes))].lower()
forca = len(palavra_aleatoria)*["_"]
letras_tentadas = []
modo = "letra"
mensagem = f"Adivinhe a palavra!"
chute = []

running = True
game_over = False

print(f"{forca}")
print(f"Palavra: {' '.join(forca)}")

while running:
    screen.fill('white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if modo == 'letra':
                modo = 'palavra'
            elif modo == 'palavra':
                modo = 'letra'
        
        if event.type == pygame.KEYDOWN and not game_over and modo == 'letra':
            letra = event.unicode.lower()

            if letra.isalpha() and len(letra) == 1 and letra not in letras_tentadas:
                letras_tentadas.append(letra)
                tentativas += 1

                if letra in palavra_aleatoria:
                    mensagem = f"Boa! A letra '{letra}' existe!"
                    for i, char in enumerate(palavra_aleatoria):
                        if char == letra:
                            forca[i] = letra
                else:
                    vidas -= 1
                    mensagem = f"Errou! '{letra}' não está na palavra"

                if "_" not in forca:
                    mensagem = f"Parabéns! Venceu em {tentativas} tentativas!"
                    game_over = True
                elif vidas <= 0:
                    mensagem = f"Que pena! A palavra era: {palavra_aleatoria}"
                    game_over = True
                    
        elif event.type == pygame.KEYDOWN and not game_over and modo == 'palavra':
        
            palpite = event.unicode.lower()
            if palpite.isalpha() and len(palpite) == 1:
                chute.append(palpite)
                
            if event.key == pygame.K_RETURN :
                if "".join(chute) == palavra_aleatoria:
                    for letra in chute: 
                        letras_tentadas.append(letra)
                    tentativas += 1
                    mensagem = f"Parabéns! Venceu em {tentativas} tentativas! A palavra e '{palavra_aleatoria}'"
                    game_over = True
                else:
                    vidas -= 1
                    tentativas += 1
                    mensagem = f"Errou! '{"".join(chute)}' não e a palavra"
                    chute = []
                

            

    palavra_display = " ".join(forca)
    texto_palavra = fonte.render(palavra_display, True, 'black')
    texto_mensagem = fonte_pequena.render(mensagem, True, 'blue')
    texto_modo = fonte_pequena.render(f"modo: {modo}",True, 'green')
    texto_vidas = fonte_pequena.render(f"Vidas: {vidas}", True, (255, 0, 0))
    
    screen.blit(texto_palavra, (screen.get_width()//2 - texto_palavra.get_width()//2, 200))
    screen.blit(texto_mensagem, (screen.get_width()//2 - texto_mensagem.get_width()//2, 300))
    screen.blit(texto_modo, (screen.get_width()//2 - texto_mensagem.get_width()//2, 350))
    screen.blit(texto_vidas, (50, 50))
    

    pygame.display.update()
