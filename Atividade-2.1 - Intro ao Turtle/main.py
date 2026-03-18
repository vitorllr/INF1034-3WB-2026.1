from turtle import *
import math

turtle = Turtle()
turtle.speed(5)

# Desenhando um plano cartesiano 

turtle.fd(400)
turtle.stamp()
turtle.lt(180)
turtle.fd(800)
turtle.stamp()
turtle.lt(180)
turtle.fd(400)
turtle.lt(90)
turtle.fd(400)
turtle.stamp()
turtle.lt(180)
turtle.fd(800)
turtle.stamp()


turtle.penup() # ou pu()
turtle.goto(200,250)
turtle.pendown() # ou pd()


color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")
# Desenhando um trapezio
turtle.color("black") #Cor da borda
turtle.begin_fill() # Usa a cor que a Turtle estiver na hora se nao definido o preenchimento
turtle.fillcolor(color)

for _ in range(2): 
    turtle.fd(100)
    turtle.lt(50)
    turtle.fd(100)


turtle.end_fill()


turtle.penup() # ou pu()
turtle.goto(300,300)
turtle.pendown() # ou pd()

# Desenhando um triangulo

turtle.penup() # ou pu()
turtle.goto(-200,-200)
turtle.pendown() # ou pd()


color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")

turtle.color("black") #Cor da borda
turtle.begin_fill() # Usa a cor que a Turtle estiver na hora se nao definido o preenchimento
turtle.fillcolor(color)

for _ in range(3): 
    turtle.fd(100)
    turtle.lt(120)

turtle.end_fill()

# Desenhando uma estrela

turtle.penup() # ou pu()
turtle.goto(-200,200)
turtle.pendown() # ou pd()

color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")

turtle.color("black") #Cor da borda
turtle.begin_fill() # Usa a cor que a Turtle estiver na hora se nao definido o preenchimento
turtle.fillcolor(color)

for _ in range(8): 
    turtle.fd(50)
    turtle.lt(135)

turtle.end_fill()


# Desenhando um octogono

turtle.penup() # ou pu()
turtle.goto(200,-200)
turtle.pendown() # ou pd()

color = textinput("Insira uma cor","Digite a cor desejada no preenchimento: ")

turtle.color("black") #Cor da borda
turtle.begin_fill() # Usa a cor que a Turtle estiver na hora se nao definido o preenchimento
turtle.fillcolor(color)

for _ in range(8): 
    turtle.fd(50)
    turtle.lt(45)

turtle.end_fill()


#Espiral 
turtle.penup() # ou pu()
turtle.goto(200,-300)
turtle.pendown() # ou pd()


# Parâmetros da Espiral
for i in range(50):
    turtle.forward(i * 2)
    turtle.right(91) 

mainloop()

