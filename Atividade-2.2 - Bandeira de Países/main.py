from turtle import *
import math
from time import sleep
screen = Screen()
turtle = Turtle()
turtle.speed(5)


colors = ["orange","white","green"]
largura_faixa = 75
altura_faixa = 150



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


#Bandeira Costa do Marfim - 1

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

#Bandeira Romênia - 9

colors = ["blue","yellow","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Romênia')
sleep(1)
turtle.clear()

#Bandeira Romênia - 10

colors = ["blue","yellow","red"]
desenha_bandeira_simples(colors,largura_faixa,altura_faixa,'Romênia')
sleep(1)
turtle.clear()






mainloop()
