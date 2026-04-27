import random 
import unicodedata

def pedir_letra():
    letra = input("Digite a letra da palavra ou a palavra inteira: ")
    if isinstance(letra, str) == False:
        print("Não podem ser escolhidos valores que nao strings")
        letra = input("Digite a letra da palavra ou a palavra inteira: ")
    return letra

def normaliza_palavra_aleatoria(palavra):
    for i, letra in enumerate(palavra):
        normal = unicodedata.normalize('NFKD', letra)
        palavra[i] = normal[0]

esportes =[
  "Futebol", "Basquete", "Vôlei", "Natação", "Tênis",
  "Atletismo", "Boxe", "Ciclismo", "Skate", "Surf",
  "Ginástica", "Rugby", "Handebol", "Medalha", "Treinador",
  "Estádio", "Árbitro", "Campeonato", "Corrida", "Olimpíadas"
]

vidas = 6
tentativas = 0
palavra_aleatoria = esportes[random.randint(0,len(esportes))].lower()
forca = len(palavra_aleatoria)*["_"]

print(f"{forca}")
print(f"Palavra: {' '.join(forca)}")

while vidas > 0 and "_" in forca:
    palpite = pedir_letra().lower()
    tentativas += 1

    if palpite == palavra_aleatoria:
        forca = list(palavra_aleatoria)
        break


    if palpite in palavra_aleatoria:
        print(f"Boa! A letra '{palpite}' existe na palavra.")
        for i, letra in enumerate(palavra_aleatoria):
            if letra == palpite:
                forca[i] = palpite
        print(f"{forca}")
    else:
        vidas -= 1
        print(f"Errou! Vidas restantes: {vidas}")


if "_" not in forca:
    print(f"Parabéns! Você acertou a palavra '{palavra_aleatoria}' em {tentativas} tentativas!")
else:
    print(f"Que pena! Você perdeu. A palavra era: {palavra_aleatoria}")
    print(f"Progresso: {' '.join(forca)}")
  