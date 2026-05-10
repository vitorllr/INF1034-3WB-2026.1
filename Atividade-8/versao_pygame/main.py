import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Login")
fonte = pygame.font.SysFont("Arial", 40)
fonte_pequena = pygame.font.SysFont("Arial", 30)
clock = pygame.time.Clock()

running = True

while running:
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_COMMA:
            mensagem = "Faça o login"
            chute = []

    palavra_display = " ".join(forca)
    texto_palavra = fonte.render(palavra_display, True, "black")
    texto_mensagem = fonte_pequena.render(mensagem, True, "blue")
    texto_modo = fonte_pequena.render(f"modo: {modo}", True, "green")
    chute_display = " ".join(chute)
    texto_chute = fonte.render(chute_display, True, "black")

    texto_vidas = fonte_pequena.render(f"Vidas: {vidas}", True, (255, 0, 0))

    # comentario do commit
    screen.blit(
        texto_palavra, (screen.get_width() // 2 - texto_palavra.get_width() // 2, 200)
    )
    screen.blit(
        texto_mensagem, (screen.get_width() // 2 - texto_mensagem.get_width() // 2, 300)
    )
    screen.blit(
        texto_modo, (screen.get_width() // 2 - texto_modo.get_width() // 2, 350)
    )
    screen.blit(
        texto_chute,
        (screen.get_width() // 2 - texto_chute.get_width() + 100 // 2, 390),
    )
    screen.blit(texto_vidas, (50, 50))

    pygame.display.update()
