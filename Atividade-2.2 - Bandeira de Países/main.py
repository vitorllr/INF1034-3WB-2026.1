from turtle import *
import math
from time import sleep
screen = Screen()
turtle = Turtle()
turtle.speed(5)


#Bandeira Costa do Marfim
colors = ["orange","white","green"]
largura_faixa = 75
altura_faixa = 150

def desenha_bandeira_simples(cores:list,largura:float,altura:float):

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



desenha_bandeira_simples(colors,largura_faixa,altura_faixa)
sleep(3)

turtle.clear()

#Bandeira França
colors = ["blue","white","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa)
sleep(3)


#Bandeira Itália 
colors = ["green","white","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa)
sleep(3)

#Bandeira Irlanda

colors = ["green","white","orange"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa)
sleep(3)


done()