import pygame
import sys
import random

# 1. Inicializar Pygame
pygame.init()
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Murciélago Aventurero - ¡Esquiva y Junta Monedas!")
reloj = pygame.time.Clock()

# Fuentes para los textos
fuente_puntos = pygame.font.SysFont("Arial", 30, bold=True)
fuente_game_over = pygame.font.SysFont("Arial", 40, bold=True)

# 2. Cargar las Imágenes del Murciélago
try:
    imagen_ala_arriba = pygame.image.load("bat1.png").convert_alpha()
    imagen_ala_abajo = pygame.image.load("bat2.png").convert_alpha()
    imagen_ala_arriba = pygame.transform.scale(imagen_ala_arriba, (90, 60))
    imagen_ala_abajo = pygame.transform.scale(imagen_ala_abajo, (90, 60))
except:
    print("⚠️ ¡Faltan las imágenes 'bat1.png' o 'bat2.png' en la carpeta!")
    pygame.quit()
    sys.exit()

# 3. Variables del Personaje (Físicas e Imágenes)
X = 200
Y = 300
ANCHO_BAT = 90
ALTO_BAT = 60

GRAVEDAD = 0.4         
IMPULSO = -7.5         
velocidad_y = 0        

# Animación
ala_arriba = True
contador_anim = 0
VEL_ANIMACION = 8

# --- CONFIGURACIÓN DE OBSTÁCULOS Y MONEDAS ---
ancho_columna = 70
velocidad_juego = 5     
hueco_libre = 190      

puntos = 0
juego_activo = True

def generar_columna():
    alto_superior = random.randint(50, ALTO - hueco_libre - 50)
    return {
        "x": ANCHO,
        "alto_sup": alto_superior,
        "y_inf": alto_superior + hueco_libre,
        "alto_inf": ALTO - (alto_superior + hueco_libre),
        "pasado": False  
    }

def generar_moneda():
    # Genera una moneda en una posición vertical aleatoria y hacia la derecha
    return {
        "x": ANCHO + random.randint(100, 250),
        "y": random.randint(100, ALTO - 100),
        "activa": True
    }

# Inicializar listas de elementos
columnas = [generar_columna()]
monedas = [generar_moneda(), generar_moneda()]

# 4. Bucle principal
while True:
    reloj.tick(60)
    
    # --- CONTROL DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and juego_activo:
                velocidad_y = IMPULSO  
            
            # Reiniciar con la tecla R
            if evento.key == pygame.K_r and not juego_activo:
                Y = 300
                velocidad_y = 0
                puntos = 0
                columnas = [generar_columna()]
                monedas = [generar_moneda(), generar_moneda()]
                juego_activo = True

    if juego_activo:
        # --- FÍSICAS DEL MURCIÉLAGO ---
        velocidad_y += GRAVEDAD
        Y += velocidad_y

        # Límites del suelo y techo
        if Y > ALTO - ALTO_BAT:
            juego_activo = False # Game over si toca el suelo
        if Y < 0:
            Y = 0
            velocidad_y = 0

        # --- ANIMACIÓN ---
        contador_anim += 1
        limite_cambio = VEL_ANIMACION if velocidad_y >= 0 else 4
        if contador_anim >= limite_cambio:
            ala_arriba = not ala_arriba
            contador_anim = 0

        # --- GESTIÓN DE OBSTÁCULOS ---
        for col in columnas:
            col["x"] -= velocidad_juego  

            # Puntos por esquivar columnas
            if not col["pasado"] and col["x"] + ancho_columna < X:
                puntos += 5
                col["pasado"] = True

        if columnas[-1]["x"] < ANCHO - 320:
            columnas.append(generar_columna())

        if columnas[0]["x"] < -ancho_columna:
            columnas.pop(0)

        # --- GESTIÓN DE MONEDAS ---
        for moneda in monedas:
            moneda["x"] -= velocidad_juego

        # Si quedan pocas monedas en pantalla, generar más
        if len(monedas) < 3:
            monedas.append(generar_moneda())

        # Eliminar las monedas que salieron del mapa
        if monedas[0]["x"] < -30:
            monedas.pop(0)

        # --- DETECCIÓN DE COLISIONES ---
        # Caja de colisión del murciélago (un poco más pequeña que la imagen para ser justos)
        caja_bat = pygame.Rect(X + 15, Y + 10, ANCHO_BAT - 30, ALTO_BAT - 20) 
        
        # Colisión con Columnas
        for col in columnas:
            caja_superior = pygame.Rect(col["x"], 0, ancho_columna, col["alto_sup"])
            caja_inferior = pygame.Rect(col["x"], col["y_inf"], ancho_columna, col["alto_inf"])
            
            if caja_bat.colliderect(caja_superior) or caja_bat.colliderect(caja_inferior):
                juego_activo = False

        # Colisión con Monedas
        for moneda in monedas:
            if moneda["activa"]:
                caja_moneda = pygame.Rect(moneda["x"], moneda["y"], 24, 24)
                if caja_bat.colliderect(caja_moneda):
                    puntos += 10         # ¡Añade 10 puntos!
                    moneda["activa"] = False

    # --- DIBUJAR EN PANTALLA ---
    pantalla.fill((15, 15, 25))  # Fondo azul noche oscuro
    
    # 1. Dibujar Obstáculos (Color Gris Piedra/Túnel: 70, 80, 85)
    for col in columnas:
        pygame.draw.rect(pantalla, (70, 80, 85), (col["x"], 0, ancho_columna, col["alto_sup"]))
        pygame.draw.rect(pantalla, (70, 80, 85), (col["x"], col["y_inf"], ancho_columna, col["alto_inf"]))

    # 2. Dibujar Monedas (Color Dorado Brillante: 255, 215, 0)
    for moneda in monedas:
        if moneda["activa"]:
            pygame.draw.circle(pantalla, (255, 215, 0), (moneda["x"] + 12, moneda["y"] + 12), 12)
            pygame.draw.circle(pantalla, (240, 170, 0), (moneda["x"] + 12, moneda["y"] + 12), 12, 2) # Borde interno

    # 3. Dibujar al Murciélago Animado
    if ala_arriba:
        pantalla.blit(imagen_ala_arriba, (X, Y))
    else:
        pantalla.blit(imagen_ala_abajo, (X, Y))
    
    # 4. Dibujar Interfaz de Puntos
    texto_puntos = fuente_puntos.render(f"Puntos: {puntos}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (20, 20))

    # 5. Letrero de Game Over si pierdes
    if not juego_activo:
        texto_game_over = fuente_game_over.render("¡GAME OVER! Presiona 'R' para reiniciar", True, (255, 100, 100))
        pantalla.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 20))

    pygame.display.flip()
