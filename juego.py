import pygame
import random
import sys

# Inicializar PyGame
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Juego")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 120, 255)

fuente = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()

def limpiar_pantalla():
    pantalla.fill(NEGRO)

def mover_jugador(teclas, jugador, velocidad):
    if teclas[pygame.K_LEFT]: jugador.x -= velocidad
    if teclas[pygame.K_RIGHT]: jugador.x += velocidad
    if teclas[pygame.K_UP]: jugador.y -= velocidad
    if teclas[pygame.K_DOWN]: jugador.y += velocidad

def mover_enemigos(enemigos, velocidades):
    for i, enemigo in enumerate(enemigos):
        enemigo.x += velocidades[i][0]
        enemigo.y += velocidades[i][1]
        if enemigo.left <= 0 or enemigo.right >= ANCHO:
            velocidades[i][0] *= -1
        if enemigo.top <= 0 or enemigo.bottom >= ALTO:
            velocidades[i][1] *= -1

def crear_enemigo(enemigos, velocidades):
    nuevo = pygame.Rect(random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50), 50, 50)
    enemigos.append(nuevo)
    velocidades.append([random.choice([-6, 6]), random.choice([-6, 6])])

def mostrar_vidas(vidas):
    texto = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

def mostrar_instrucciones():
    esperando = True
    while esperando:
        limpiar_pantalla()
        instrucciones = [
            "INSTRUCCIONES:",
            "Usa las flechas del teclado para mover al jugador.",
            "Evita chocar con los enemigos.",
            "Tienes 3 vidas.",
            "",
            "Haz clic para volver al menú."
        ]
        for i, linea in enumerate(instrucciones):
            texto = fuente.render(linea, True, BLANCO)
            pantalla.blit(texto, (250, 100 + i * 40))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                esperando = False

def mostrar_game_over():
    esperando = True
    while esperando:
        limpiar_pantalla()
        texto = fuente.render("¡Has perdido!", True, BLANCO)
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 60))

        boton_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2, 200, 50)
        pygame.draw.rect(pantalla, AZUL, boton_rect)
        texto_boton = fuente.render("Volver al menú", True, BLANCO)
        pantalla.blit(texto_boton, (boton_rect.x + 30, boton_rect.y + 15))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    esperando = False

def iniciar_juego():
    jugador = pygame.Rect(400, 300, 50, 50)
    enemigos = [pygame.Rect(random.randint(0, ANCHO - 50), random.randint(0, ALTO - 50), 50, 50)]
    velocidades = [[random.choice([-6, 6]), random.choice([-6, 6])]]
    tiempo_ultimo = pygame.time.get_ticks()
    vidas = 3

    en_juego = True
    while en_juego:
        clock.tick(60)
        limpiar_pantalla()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

        teclas = pygame.key.get_pressed()
        mover_jugador(teclas, jugador, 5)
        mover_enemigos(enemigos, velocidades)

        for enemigo in enemigos:
            if jugador.colliderect(enemigo):
                vidas -= 1
                jugador.x, jugador.y = 400, 300
                pygame.time.delay(500)
                break

        if pygame.time.get_ticks() - tiempo_ultimo > 6000:
            crear_enemigo(enemigos, velocidades)
            tiempo_ultimo = pygame.time.get_ticks()

        pygame.draw.rect(pantalla, VERDE, jugador)
        for enemigo in enemigos:
            pygame.draw.rect(pantalla, ROJO, enemigo)

        mostrar_vidas(vidas)
        pygame.display.flip()

        if vidas <= 0:
            pygame.time.delay(1000)
            mostrar_game_over()
            en_juego = False

    mostrar_menu()

def mostrar_menu():
    en_menu = True
    while en_menu:
        limpiar_pantalla()
        titulo = fuente.render("Mini Juego", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        botones = [
            ("Iniciar", iniciar_juego),
            ("Instrucciones", mostrar_instrucciones),
            ("Salir", salir)
        ]

        botones_rects = []
        for i, (texto, accion) in enumerate(botones):
            rect = pygame.Rect(ANCHO // 2 - 100, 200 + i * 80, 200, 50)
            pygame.draw.rect(pantalla, AZUL, rect)

            texto_render = fuente.render(texto, True, BLANCO)
            pantalla.blit(texto_render, (rect.x + 50, rect.y + 10))
            botones_rects.append((rect, accion))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for rect, accion in botones_rects:
                    if rect.collidepoint(evento.pos):
                        en_menu = False
                        accion()

def salir():
    pygame.quit()
    sys.exit()

# Ejecutar el menú principal
if __name__ == "__main__":
    mostrar_menu()
