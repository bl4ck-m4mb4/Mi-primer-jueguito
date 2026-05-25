import pygame

# 1. Inicializar todas las funciones de Pygame
pygame.init()

# 2. Configurar el tamaño de la ventana (Ancho, Alto) en píxeles
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# 3. Poner un título a la ventana del juego
pygame.display.set_caption("Mi Primer Jueguito")

# 4. Bucle principal del juego (mantiene la ventana corriendo)
ejecutando = True
while ejecutando:
    
    # Revisar si el usuario hace clic en cerrar (la X)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
    # Llenar la pantalla de color negro para borrar el cuadro anterior
    pantalla.fill((0, 0, 0))
    
    # Actualizar la pantalla con lo que dibujamos
    pygame.display.flip()

# 5. Cerrar el juego correctamente al salir del bucle
pygame.quit()