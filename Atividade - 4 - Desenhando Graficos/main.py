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

def elevado_x(x):
    return 2**x

def calcula_5_menos_x2(x):
    return (5 - x ** 2)

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
        t.goto(i*3,math.sqrt(3*i))
        t.pd()
    sleep(1)

def desenha_inverso_de_x():
    t.color("green")

    for i in range(-199, -1):
        t.goto(i, inverso_x(i/50) * 10) 
    
    # Parte positiva
    for i in range(1, 201):
        t.goto(i, inverso_x(i/50) * 10)
    sleep(1)

def desenha_2_elevado_x():
    t.color("orange")
    for i in range(-199, 201):
        t.goto(i, elevado_x(i/50) * 10)
        t.pd()
 
    sleep(1)

def desenha_5_menos_x2():
    t.color("purple")
    for i in range(-199, 201):
        t.goto(i, calcula_5_menos_x2(i/50) * 10)
        t.pd()
 
sleep(1)

# Bloco Principal

# Soma 2

# desenha_plano_cartesiano()
# t.color("red")
# t.pu()
# t.goto(-200,soma_2(-200))
# t.pd()
# # t.goto(100,soma_2(100))
# desenha_soma_2()
# t.clear()
   
# Raiz de X
# desenha_plano_cartesiano()
# t.pu()
# t.goto(0,0)
# t.pd()
# # t.goto(100,soma_2(100))
# t.color("blue")
# desenha_raiz_2()
# t.clear()

# 1/X
  
# desenha_plano_cartesiano()
# t.pu()
# t.goto(-200,0)
# t.pd()
# desenha_inverso_de_x()
# t.clear()

# 2^x
# desenha_plano_cartesiano()
# t.pu()
# t.goto(0,0)
# desenha_2_elevado_x()
# t.clear()

# 5 - x^2
desenha_plano_cartesiano()
t.pu()
t.goto(0,0)
desenha_5_menos_x2()
t.clear()

mainloop()

