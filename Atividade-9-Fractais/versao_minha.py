import turtle


def desenha_fractal_estrela(t, size):
    if size < 10:
        return
    for i in range(5):
        t.fd(size)
        desenha_fractal_estrela(t, size / 3)
        t.lt(216)


t = turtle.Turtle()
turtle.colormode(255)
t.speed(0)

desenha_fractal_estrela(t, 200)
