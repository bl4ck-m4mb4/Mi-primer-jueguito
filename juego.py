import pygame
import random

# 1. Inicializar Pygame
pygame.init()

# 2. Configurar ventana
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Murciélago - ¡Dificultad y Colores Dinámicos!")

# Fuentes para el texto
fuente_game_over = pygame.font.SysFont("Arial", 40)
fuente_puntos = pygame.font.SysFont("Arial", 30)

# 3. Configuración del Murciélago
X = 200
Y = 300
TAMANO_ANCHO = 85
TAMANO_ALTO = 50

# Variables de física
GRAVEDAD = 0.4
IMPULSO = -7.5
velocidad_y = 0

# Animación del vuelo
ala_arriba = True
contador_tiempo = 0
VEL_ANIMACION = 8

# --- CONFIGURACIÓN DE OBSTÁCULOS Y PUNTOS ---
ancho_columna = 70
velocidad_base = 5     
velocidad_columna = velocidad_base
hueco_libre = 180      

puntos = 0

# Variable para controlar el color de fondo actual (RGB)
color_fondo = (15, 15, 25)

def generar_columna():
    alto_superior = random.randint(50, ALTO - hueco_libre - 50)
    return {
        "x": ANCHO,
        "alto_sup": alto_superior,
        "y_inf": alto_superior + hueco_libre,
        "alto_inf": ALTO - (alto_superior + hueco_libre),
        "pasado": False  
    }

columnas = [generar_columna()]
juego_activo = True
reloj = pygame.time.Clock()

# 4. Bucle principal
ejecutando = True
while ejecutando:
    reloj.tick(60)
    
    # --- CONTROL DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and juego_activo:
                velocidad_y = IMPULSO
            # Reiniciar todo al perder con la tecla R
            if evento.key == pygame.K_r and not juego_activo:
                Y = 300
                velocidad_y = 0
                velocidad_columna = velocidad_base
                puntos = 0
                color_fondo = (15, 15, 25)
                columnas = [generar_columna()]
                juego_activo = True

    if juego_activo:
        # --- FÍSICAS DEL MURCIÉLAGO ---
        velocidad_y += GRAVEDAD
        Y += velocidad_y

        if Y > ALTO - TAMANO_ALTO:
            juego_activo = False
        if Y < 0:
            Y = 0
            velocidad_y = 0

        # --- LÓGICA DE ANIMACIÓN ---
        contador_tiempo += 1
        limite_animacion = VEL_ANIMACION if velocidad_y >= 0 else 4
        if contador_tiempo >= limite_animacion:
            ala_arriba = not ala_arriba
            contador_tiempo = 0

        # --- GESTIÓN DE OBSTÁCULOS, PUNTOS Y FONDOS ---
        for col in columnas:
            col["x"] -= velocidad_columna  

            # Sumar puntos cuando el murciélago pasa la mitad de la columna
            if not col["pasado"] and col["x"] + ancho_columna < X:
                puntos += 1
                col["pasado"] = True
                
                # Aumentar la velocidad cada 5 puntos para subir la dificultad
                if puntos % 5 == 0:
                    velocidad_columna += 1

        # --- CAMBIAR COLOR DE FONDO SEGÚN EL PUNTAJE ---
        if puntos < 5:
            color_fondo = (15, 15, 25)       # Noche oscura original
        elif puntos < 10:
            color_fondo = (40, 20, 60)       # Noche morada / mística
        elif puntos < 15:
            color_fondo = (20, 45, 75)       # Azul eléctrico profundo
        else:
            color_fondo = (70, 20, 20)       # Carmesí / Nivel experto

        if columnas[-1]["x"] < ANCHO - 300:
            columnas.append(generar_columna())

        if columnas[0]["x"] < -ancho_columna:
            columnas.pop(0)

        # --- DETECCIÓN DE COLISIONES ---
        caja_murcielago = pygame.Rect(X, Y, 50, 30) 
        
        for col in columnas:
            caja_superior = pygame.Rect(col["x"], 0, ancho_columna, col["alto_sup"])
            caja_inferior = pygame.Rect(col["x"], col["y_inf"], ancho_columna, col["alto_inf"])
            
            if caja_murcielago.colliderect(caja_superior) or caja_murcielago.colliderect(caja_inferior):
                juego_activo = False

    # --- DIBUJAR EN PANTALLA ---
    pantalla.fill(color_fondo)  # Pintar el fondo con el color dinámico actual
    
    # Dibujar obstáculos (Color roca contrastante: 50, 75, 70)
    for col in columnas:
        pygame.draw.rect(pantalla, (50, 75, 70), (col["x"], 0, ancho_columna, col["alto_sup"]))
        pygame.draw.rect(pantalla, (50, 75, 70), (col["x"], col["y_inf"], ancho_columna, col["alto_inf"]))

    # Dibujar al Murciélago
    pygame.draw.ellipse(pantalla, (95, 55, 120), (X, Y, 50, 30))
    pygame.draw.circle(pantalla, (95, 55, 120), (X + 25, Y - 5), 12)
    
    if ala_arriba:
        pygame.draw.polygon(pantalla, (65, 25, 90), [(X, Y + 15), (X - 35, Y - 15), (X - 10, Y + 10)])
        pygame.draw.polygon(pantalla, (65, 25, 90), [(X + 50, Y + 15), (X + 85, Y - 15), (X + 60, Y + 10)])
    else:
        pygame.draw.polygon(pantalla, (65, 25, 90), [(X, Y + 15), (X - 35, Y + 35), (X - 15, Y + 10)])
        pygame.draw.polygon(pantalla, (65, 25, 90), [(X + 50, Y + 15), (X + 85, Y + 35), (X + 65, Y + 10)])
    
    # Dibujar el marcador de puntos
    texto_puntos = fuente_puntos.render(f"Puntos: {puntos}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (20, 20))

    # Si el jugador perdió, mostrar letrero de Game Over
    if not juego_activo:
        texto_game_over = fuente_game_over.render("¡GAME OVER! Presiona 'R' para reiniciar", True, (255, 255, 255))
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 20))

    pygame.display.flip()

pygame.quit()

