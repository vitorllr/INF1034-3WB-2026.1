from turtle import *
from time import sleep

screen = Screen()
turtle = Turtle()
turtle.speed(10)

colors = ["orange","white","green"]
largura_faixa = 75
altura_faixa = 150

largura_faixa_horizontal = 210
altura_faixa_horizontal = 50

def desenha_bandeira_simples(cores:list,largura:float,altura:float,nome_pais:str):


    # Posicionamento inicial (para não começar no meio da tela)
    turtle.penup()
    turtle.goto(-75, 50) 
    turtle.pendown()
    turtle.color("black")

    for i in cores:
        turtle.fillcolor(i)
        turtle.begin_fill()
        # Desenha o retângulo 
        for _ in range(2):
            turtle.forward(largura)
            turtle.right(90)
            turtle.forward(altura)
            turtle.right(90)
        turtle.end_fill()
        # Move para a posição da próxima faixa
        turtle.penup()
        turtle.forward(largura)
        turtle.pendown()

    # 3. Coloca o nome do país acima da bandeira
    
    centro_x = largura/2
    posicao_y_texto = altura + 20
    
    turtle.penup()
    turtle.goto(centro_x, posicao_y_texto)
    turtle.color("black")
    
    turtle.write(nome_pais, align="center", font=("Arial", 16, "bold"))
    
    turtle.hideturtle()

def desenha_bandeira_simples_horizontal(cores:list, largura:float, altura:float, nome_pais:str):
    # Posicionamento inicial
    turtle.penup()
    turtle.goto(-largura/2, 100) # Centraliza melhor no eixo X
    turtle.pendown()
    turtle.setheading(0) # Garante que está olhando para a direita
    turtle.color("black")

    start_x, start_y = turtle.pos()

    for i in cores:
        turtle.fillcolor(i)
        turtle.begin_fill()
        # Desenha o retângulo 
        for _ in range(2):
            turtle.forward(largura)
            turtle.right(90)
            turtle.forward(altura)
            turtle.right(90)
        turtle.end_fill()

        # Move pra baixo para a próxima faixa
        turtle.penup()
        turtle.right(90)
        turtle.forward(altura)
        turtle.left(90)
        turtle.pendown()

    # 3. Nome do país (acima da primeira faixa)
    turtle.penup()
    turtle.goto(0, start_y + 10)
    turtle.write(nome_pais, align="center", font=("Arial", 16, "bold"))
    turtle.hideturtle()

#Bandeira Costa do Marfim - 1
def desenha_bandeira_costa_marfim():
    colors = ["orange","white","green"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Costa do Marfim')
    sleep(1)
    turtle.clear()

#Bandeira França - 2
def desenha_bandeira_franca():
    colors = ["blue","white","red"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'França')
    sleep(1)
    turtle.clear()

#Bandeira Itália - 3
def desenha_bandeira_italia():
    colors = ["green","white","red"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa, "Itália")
    sleep(1)
    turtle.clear()

#Bandeira Irlanda - 4
def desenha_bandeira_irlanda():
    colors = ["green","white","orange"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Irlanda')
    sleep(1)
    turtle.clear()

#Bandeira Bélgica - 5
def desenha_bandeira_belgica():
    colors = ["black","yellow","red"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Bélgica')
    sleep(1)
    turtle.clear()

#Bandeira Peru - 6
def desenha_bandeira_peru():
    colors = ["red","white","red"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Peru')
    sleep(1)
    turtle.clear()

#Bandeira Nigéria - 7
def desenha_bandeira_nigeria():
    colors = ["green","white","green"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Nigéria')
    sleep(1)
    turtle.clear()

#Bandeira Romênia - 8
def desenha_bandeira_romenia():
    colors = ["blue","yellow","red"]
    desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Romênia')
    sleep(1)
    turtle.clear()

#Bandeira Alemanha - 9
def desenha_bandeira_alemanha():
    colors = ["black","red","gold"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Alemanha')
    sleep(1)
    turtle.clear()

#Bandeira Russia - 10
def desenha_bandeira_russia():
    colors = ["white","blue","red"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Russia')
    sleep(1)
    turtle.clear()

#Bandeira Países Baixos - 11
def desenha_bandeira_paises_baixos():
    colors = ["red","white","blue"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Países Baixos')
    sleep(1)
    turtle.clear()

#Bandeira Bulgária - 12
def desenha_bandeira_bulgaria():
    colors = ["white","green","red"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Bulgária')
    sleep(1)
    turtle.clear()

#Bandeira Estônia - 12
def desenha_bandeira_estonia():
    colors = ["blue","black","white"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Estônia')
    sleep(1)
    turtle.clear()

#Bandeira Hungria - 13
def desenha_bandeira_hungria():
    colors = ["red","white","green"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Hungria')
    sleep(1)
    turtle.clear()

#Bandeira Iêmen - 14
def desenha_bandeira_iemen():
    colors = ["red","white","black"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Iêmen')
    sleep(1)
    turtle.clear()

#Bandeira Lituânia - 15
def desenha_bandeira_lituania():
    colors = ["yellow","green","red"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Lituânia')
    sleep(1)
    turtle.clear()

#Bandeira Luxemburgo - 16
def desenha_bandeira_luxemburgo():
    colors = ["red","white","blue"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Luxemburgo')
    sleep(1)
    turtle.clear()

#Bandeira Serra Leoa - 17
def desenha_bandeira_serra_leoa():
    colors = ["green","white","blue"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Serra Leoa')
    sleep(1)
    turtle.clear()

#Bandeira Bolivia - 18
def desenha_bandeira_bolivia():
    colors = ["red","yellow","green"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Bolivia')
    sleep(1)
    turtle.clear()

#Bandeira Mali - 19
def desenha_bandeira_mali():
    colors = ["green","yellow","red"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Mali')
    sleep(1)
    turtle.clear()

#Bandeira Gabão - 20
def desenha_bandeira_gabao():
    colors = ["green","yellow","blue"]
    desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Gabão')
    sleep(1)
    turtle.clear()

desenha_bandeira_costa_marfim()
desenha_bandeira_franca()
desenha_bandeira_italia()
desenha_bandeira_irlanda()
desenha_bandeira_belgica()
desenha_bandeira_peru()
desenha_bandeira_nigeria()
desenha_bandeira_romenia()
desenha_bandeira_alemanha()
desenha_bandeira_russia()
desenha_bandeira_paises_baixos()
desenha_bandeira_bulgaria()
desenha_bandeira_estonia()
desenha_bandeira_hungria()
desenha_bandeira_iemen()
desenha_bandeira_lituania()
desenha_bandeira_luxemburgo()
desenha_bandeira_serra_leoa()
desenha_bandeira_bolivia()
desenha_bandeira_mali()
desenha_bandeira_gabao()

#DESAFIO BANDEIRA POR TEXTINPUT
bandeiras = {
    "Costa do Marfim": desenha_bandeira_costa_marfim,
    "França": desenha_bandeira_franca,
    "Itália": desenha_bandeira_italia,
    "Irlanda": desenha_bandeira_irlanda,
    "Bélgica": desenha_bandeira_belgica,
    "Peru": desenha_bandeira_peru,
    "Nigéria": desenha_bandeira_nigeria,
    "Romênia": desenha_bandeira_romenia,
    "Alemanha": desenha_bandeira_alemanha,
    "Rússia": desenha_bandeira_russia,
    "Países Baixos": desenha_bandeira_paises_baixos,
    "Bulgária": desenha_bandeira_bulgaria,
    "Estônia": desenha_bandeira_estonia,
    "Hungria": desenha_bandeira_hungria,
    "Iêmen": desenha_bandeira_iemen,
    "Lituânia": desenha_bandeira_lituania,
    "Luxemburgo": desenha_bandeira_luxemburgo,
    "Serra Leoa": desenha_bandeira_serra_leoa,
    "Bolívia": desenha_bandeira_bolivia,
    "Mali": desenha_bandeira_mali,
    "Gabão": desenha_bandeira_gabao
}

def desenha_bandeira_por_textinput():
    input_value = textinput("Bandeira Por Input","Digite o nome de uma bandeira com")

    if input_value in bandeiras:
        bandeiras[input_value]()
    else:
        turtle.hideturtle()
        turtle.write("A bandeira inserida não está na lista!", align="center", font=("Arial", 16, "bold"))
        sleep(2)
        turtle.clear()

numero_de_bandeira = int(textinput("Ola","Quantas Bandeiras quer desenhar?"))

while numero_de_bandeira > 0:
    desenha_bandeira_por_textinput()
    numero_de_bandeira -= 1

mainloop()
