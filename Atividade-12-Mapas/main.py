# desenhando mapas em tiles, dividindo a tela em varios pedacinhos
# o tamanho do tile e mudado para altura e largura


# trabalhando com o for aninhado para fazer uma matriz
# usando tilesets para colocar ao inves de cores simples, usando um dict para fazer os recortes de cada fundo
# O tamanho do tileset sera 64x64
# A ordem dos tiles a serem desenhados e controlada por uma lista de varias strings que representam as linhas e colunas

# Colisao:
# Criar colliders para envolver personagens e obstaculos
# Esses colliders sao formas geometricas, geralmente um retangulo
# collider_jogador = pygame.Rect(pos_x,pos_y, 64,64) desenhado junto com o personagem
# declarar o collider dentro do while loop
# escrever a logica de quando os objetos se encontram:
# o pygame fornece o recurso de colliderect(collider_a_comparar)

# antes de checar o pressionar das teclas vou pegar as posicoes antogas com old_pos_x e old_pos_y
#
# if collider_mergulhador == colliderect(collider_a_comparar):
#     pos_x = old_pos_x
#     pos_y = old_pos_y


# IDEIA PARA O PROJETO DA G3:
# Jogo com mapa na agua, estilo flappy bird, jogador(mergulhador) deve usar as setas para se movimentar de uma
# ponta a outra do mapa, com um tubarao seguindo ele, ao passar de nivel a quantidade de tubaroes aumenta
# ao tocar no mergulhador o tubarao explode e o jogo acaba
# Os obsltaculos serao minas submarinas, submarinos e pedras
