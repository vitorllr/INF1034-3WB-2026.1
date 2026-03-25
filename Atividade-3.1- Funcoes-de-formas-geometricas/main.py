from turtle import *
import random
import math


t = Turtle()
t.speed(7)

def desenhar_plano_cartesiano():
    # Desenhando um plano cartesiano 
    t.goto(0,0)
    t.fd(400)
    t.stamp()
    t.lt(180)
    t.fd(800)
    t.stamp()
    t.lt(180)
    t.fd(400)
    t.lt(90)
    t.fd(400)
    t.stamp()
    t.lt(180)
    t.fd(800)
    t.stamp()

    t.hideturtle()
    #t.penup() # ou pu()
    #t.goto(200,250)
    #t.pendown() # ou pd()


def desenhar_quadrado(x, y, fill_color: str, lado:int):

    x = rand_x - lado
    y = rand_y -lado

    t.penup()
    t.goto(x,y)
    t.setheading(0)
    t.pendown()

    t.fillcolor(fill_color)
    t.begin_fill()

    for _ in range(4):
        t.fd(lado)
        t.rt(90)

    t.end_fill()

    t.hideturtle()


def desenhar_triangulo_equilatero(fill_color: str, lado:int):
    altura = lado * math.sqrt(3)/2
    rand_x = random.randint(0, int(300 - lado))
    rand_y = random.randint(-300, int(0 - altura))

    t.penup()
    t.goto(rand_x,rand_y)
    t.pendown()


    t.color(fill_color) #Cor da borda
    t.begin_fill() # Usa a cor que a T estiver na hora se nao definido o preenchimento
    t.fillcolor(color)

    for _ in range(3): 
        t.fd(lado)
        t.lt(120)

    t.end_fill()

def desenhar_octogono(fill_color: str, lado:int):
    altura = int(lado*(1 + math.sqrt(2)))

    rand_x = random.randint(-300,altura)
    rand_y = random.randint(-300,int(300-altura))

    t.penup() # ou pu()
    t.goto(rand_x, rand_y)
    t.pendown() # ou pd()


    t.begin_fill() # Usa a cor que a t estiver na hora se nao definido o preenchimento
    t.fillcolor(fill_color)

    for _ in range(8): 
        t.fd(lado)
        t.lt(45)

    t.end_fill()

def desenhar_trapezio(fill_color: str, lado_menor:int, lado_maior:int, lado_nao_paralelo:int):


    rand_x = random.randint(-300,lado_maior)
    rand_y = random.randint(1,(300-altura))

    t.penup() # ou pu()
    t.goto(rand_x, rand_y)
    t.pendown() # ou pd()


    t.begin_fill() # Usa a cor que a t estiver na hora se nao definido o preenchimento
    t.fillcolor(fill_color)

    for _ in range(2): 
        t.fd(lado_menor)
        t.lt(130) # Ângulo suplementar para fechar um trapézio comum
        t.fd(lado_maior)
        t.lt(50)


    t.end_fill()



desenhar_plano_cartesiano()
color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")
rand_x = random.randint(0,int(300))
rand_y = random.randint(0,int(300))
desenhar_quadrado(rand_x,rand_y,color,100)
color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")
desenhar_triangulo_equilatero(color,100)
color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")
desenhar_octogono(color,70)
color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")
desenhar_trapezio(color, 50,100,10)



mainloop()