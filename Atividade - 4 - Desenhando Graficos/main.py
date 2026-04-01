from turtle import *
from time import sleep
import math


t = Turtle()
t.speed(0)

def soma_2(x):
    return x + 2

def raiz_2(x):
    return x ** 1/2

def inverso_x(x):
    return 1/x

def desenha_soma_2():
    for i in range(-99,101):
        # t.pu()
        t.goto(i*2,soma_2(2*i))
        t.pd()
       
    sleep(1)

def desenha_plano_cartesiano():
    t.color("black")
    # Eixo dos X
    t.pu()
    t.goto(-300, 0)
    t.pd()
    t.goto(300, 0)
    t.stamp()

    # Eixo dos Y
    t.pu()
    t.goto(0,-300)
    t.pd()
    t.goto(0,300)
    t.lt(90)
    t.stamp()
    t.rt(90)


def desenha_raiz_2():
    for i in range(0,101):
        # t.pu()
        t.goto(i*2,math.sqrt(2*i))
        t.pd()
    sleep(1)

def desenha_inverso_de_x():
    for i in range(-99,101):
        # t.pu()
        t.goto(i*2,inverso_x(2*i))
        t.pd()
    sleep(1)



# Bloco Principal

# Soma 2

desenha_plano_cartesiano()
t.color("red")
t.pu()
t.goto(-200,soma_2(-200))
t.pd()
# t.goto(100,soma_2(100))
desenha_soma_2()
t.clear()
   
# Raiz de X
desenha_plano_cartesiano()
t.pu()
t.goto(0,0)
t.pd()
# t.goto(100,soma_2(100))
t.color("blue")
desenha_raiz_2()
t.clear()

# 1/X
  
desenha_plano_cartesiano()

t.pu()
t.goto(-200,inverso_x(-200))
t.pd()
# t.goto(100,soma_2(100))
t.color("green")
desenha_inverso_de_x()
t.clear()



mainloop()