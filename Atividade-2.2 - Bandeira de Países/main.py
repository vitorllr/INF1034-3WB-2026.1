from turtle import *
import math
from time import sleep
screen = Screen()
turtle = Turtle()
turtle.speed(5)


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
colors = ["orange","white","green"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Costa do Marfim')
sleep(1)
turtle.clear()

#Bandeira França - 2
colors = ["blue","white","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'França')
sleep(1)
turtle.clear()


#Bandeira Itália - 3
colors = ["green","white","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa, "Itália")
sleep(1)
turtle.clear()

#Bandeira Irlanda - 4

colors = ["green","white","orange"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Irlanda')
sleep(1)
turtle.clear()

#Bandeira Bélgica - 5

colors = ["black","yellow","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Bélgica')
sleep(1)
turtle.clear()


#Bandeira Peru - 6

colors = ["red","white","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Peru')
sleep(1)
turtle.clear()

#Bandeira Nigéria - 7

colors = ["green","white","green"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Nigéria')
sleep(1)
turtle.clear()

#Bandeira Romênia - 8

colors = ["blue","yellow","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Romênia')
sleep(1)
turtle.clear()

#Bandeira Alemanha - 9

colors = ["black","red","gold"]
desenha_bandeira_simples_horizontal(colors,largura_faixa,altura_faixa,'Alemanha')
sleep(1)
turtle.clear()

#Bandeira Russia - 10

colors = ["white","blue","red"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Russia')
sleep(1)
turtle.clear()

#Bandeira Países Baixos - 11

colors = ["red","white","blue"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Países Baixos')
sleep(1)
turtle.clear()



#Bandeira Bulgária - 12

colors = ["white","green","red"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Bulgária')
sleep(1)
turtle.clear()

#Bandeira Estônia - 12

colors = ["blue","black","white"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Estônia')
sleep(1)
turtle.clear()

#Bandeira Hungria - 13

colors = ["red","white","green"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Hungria')
sleep(1)
turtle.clear()

#Bandeira Iêmen - 14

colors = ["red","white","black"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Iêmen')
sleep(1)
turtle.clear()


#Bandeira Lituânia - 15

colors = ["yellow","green","red"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Lituânia')
sleep(1)
turtle.clear()


#Bandeira Luxemburgo - 16

colors = ["red","white","blue"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Luxemburgo')
sleep(1)
turtle.clear()

#Bandeira Serra Leoa - 17

colors = ["green","white","blue"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Serra Leoa')
sleep(1)
turtle.clear()

#Bandeira Bolivia - 18

colors = ["red","yellow","dark-green"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Bolivia')
sleep(1)
turtle.clear()


#Bandeira Mali - 19

colors = ["green","yellow","red"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Mali')
sleep(1)
turtle.clear()

#Bandeira Gabão - 20

colors = ["green","yellow","blue"]
desenha_bandeira_simples_horizontal(colors,largura_faixa_horizontal,altura_faixa_horizontal,'Gabão')
sleep(1)
turtle.clear()








mainloop()
