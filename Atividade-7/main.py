import random 

def pedir_letra():
    letra = input("Digite a letra da palavra ou a palavra inteira: ").lower()
    if isinstance(letra, str) == False:
        print("Não podem ser escolhidos valores que nao strings")
        letra = input("Digite a letra da palavra ou a palavra inteira: ").lower()
    return letra

esportes =[
  "Futebol", "Basquete", "Vôlei", "Natação", "Tênis",
  "Atletismo", "Boxe", "Ciclismo", "Skate", "Surf",
  "Ginástica", "Rugby", "Handebol", "Medalha", "Treinador",
  "Estádio", "Árbitro", "Campeonato", "Corrida", "Olimpíadas"
]

vidas = 6
tentativas = 0
palavra_aleatoria = esportes[random.randint(0,len(esportes))]
aparicao = 0
forca = len(palavra_aleatoria)*["_"]
print(f"{forca}")
print(f"{palavra_aleatoria}")

while vidas > 0:
   palpite = pedir_letra()
   tentativas += 1
   for i, letra in enumerate(palpite):
    if palpite == palavra_aleatoria:
        print(f"Você acertou a palavra em {tentativas} !")
        break
    elif letra in palavra_aleatoria:
        aparicao += 1
        forca[i] = letra
        print(f"A letra escrita aparece {aparicao} vezes")
        print(f"{forca}")
    else:
       vidas -= 1