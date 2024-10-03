import pygame
import random
import time
import json
import os

pygame.init()

ANCHO, ALTO = 800, 600
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 120, 255)

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ahorcado")

fuente = pygame.font.Font(None, 36)

ruta_json = "palabras.json"
ruta_txt = "palabras.txt"

if not os.path.exists(ruta_json):
    palabras = [
        ("PYTHON", "Lenguaje de programación"),
        ("PROGRAMACION", "Proceso de codificación"),
        ("COMPUTADORA", "Máquina para realizar cálculos"),
        ("ALGORITMO", "Conjunto de pasos para resolver un problema"),
        ("DESARROLLO", "Creación de software"),
        ("INTERFAZ", "Conexión entre diferentes sistemas"),
        ("VARIABLE", "Espacio de almacenamiento"),
        ("FUNCION", "Bloque de código reutilizable"),
        ("BUCLE", "Estructura de repetición"),
        ("CONDICION", "Instrucción que evalúa una expresión"),
        ("INTELIGENCIA", "Capacidad para aprender y entender"),
        ("TECNOLOGIA", "Aplicación del conocimiento científico"),
        ("CIENCIA", "Estudio del mundo físico y natural"),
        ("ELECTRONICA", "Rama de la ingeniería"),
        ("MATEMATICAS", "Ciencia de los números"),
    ]
    with open(ruta_json, "w") as archivo_json:
        json.dump(palabras, archivo_json)
else:
    with open(ruta_json, "r") as archivo_json:
        palabras = json.load(archivo_json)


def guardar_palabra(palabra, pista):
    palabras.append((palabra, pista))
    with open(ruta_json, "w") as archivo_json:
        json.dump(palabras, archivo_json)
    with open(ruta_txt, "a") as archivo_txt:
        archivo_txt.write(f"{palabra}: {pista}\n")


def dibujar_texto(texto, x, y, color=BLANCO, tamaño=36):
    fuente = pygame.font.Font(None, tamaño)
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect(center=(x, y))
    pantalla.blit(superficie, rectangulo)


def dibujar_ahorcado(errores):
    pygame.draw.line(pantalla, BLANCO, (100, 500), (300, 500), 5)
    pygame.draw.line(pantalla, BLANCO, (200, 500), (200, 150), 5)
    pygame.draw.line(pantalla, BLANCO, (200, 150), (350, 150), 5)
    pygame.draw.line(pantalla, BLANCO, (350, 150), (350, 200), 5)
    if errores > 0:
        pygame.draw.circle(pantalla, BLANCO, (350, 230), 20, 5)
    if errores > 1:
        pygame.draw.line(pantalla, BLANCO, (350, 250), (350, 350), 5)
    if errores > 2:
        pygame.draw.line(pantalla, BLANCO, (350, 270), (320, 320), 5)
    if errores > 3:
        pygame.draw.line(pantalla, BLANCO, (350, 270), (380, 320), 5)
    if errores > 4:
        pygame.draw.line(pantalla, BLANCO, (350, 350), (320, 400), 5)
    if errores > 5:
        pygame.draw.line(pantalla, BLANCO, (350, 350), (380, 400), 5)


def ingreso_texto(pregunta):
    input_activo = False
    texto_ingresado = ""
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto(pregunta, ANCHO // 2, ALTO // 4, BLANCO)
        pygame.draw.rect(pantalla, BLANCO, (ANCHO // 4, ALTO // 2, ANCHO // 2, 40), 2)
        superficie_texto = fuente.render(texto_ingresado, True, BLANCO)
        pantalla.blit(superficie_texto, (ANCHO // 4 + 5, ALTO // 2 + 5))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return texto_ingresado
                elif evento.key == pygame.K_BACKSPACE:
                    texto_ingresado = texto_ingresado[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    return None
                else:
                    texto_ingresado += evento.unicode.upper()
        pygame.display.flip()


def agregar_palabra():
    while True:
        nueva_palabra = ingreso_texto("Introduce la nueva palabra:")
        if nueva_palabra is None:
            return
        nueva_pista = ingreso_texto("Introduce la pista para la palabra:")
        if nueva_pista is None:
            return
        guardar_palabra(nueva_palabra, nueva_pista)
        break


def menu_principal():
    seleccion = 0
    opciones = ["Jugar", "Agregar palabra", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto("Ahorcado", ANCHO // 2, ALTO // 4, BLANCO, tamaño=48)
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            dibujar_texto(opcion, ANCHO // 2, ALTO // 2 + i * 50, color)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return True
                    elif seleccion == 1:
                        agregar_palabra()
                    elif seleccion == 2:
                        pygame.quit()
                        return False
        pygame.display.flip()


def menu_pausa():
    seleccion = 0
    opciones = ["Reanudar", "Reiniciar", "Salir al menú principal"]
    while True:
        pantalla.fill(NEGRO)
        dibujar_texto("Pausa", ANCHO // 2, ALTO // 4, BLANCO)
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            dibujar_texto(opcion, ANCHO // 2, ALTO // 2 + i * 50, color)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return "reanudar"
                    elif seleccion == 1:
                        return "reiniciar"
                    elif seleccion == 2:
                        return "menu_principal"
        pygame.display.flip()


def main():
    if not menu_principal():
        return
    palabra, pista = random.choice(palabras)
    letras_adivinadas = set()
    errores = 0
    max_errores = 6
    reloj = pygame.time.Clock()
    tiempo_inicial = time.time()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key >= pygame.K_a and evento.key <= pygame.K_z:
                    letra = chr(evento.key).upper()
                    if letra not in letras_adivinadas:
                        letras_adivinadas.add(letra)
                        if letra not in palabra:
                            errores += 1
                elif evento.key == pygame.K_ESCAPE:
                    opcion = menu_pausa()
                    if opcion == "menu_principal":
                        return main()
                    elif opcion == "reiniciar":
                        palabra, pista = random.choice(palabras)
                        letras_adivinadas = set()
                        errores = 0
                        tiempo_inicial = time.time()
                elif evento.key == pygame.K_r:
                    main()
        pantalla.fill(NEGRO)
        dibujar_texto("Ahorcado", ANCHO // 2, 50, BLANCO, tamaño=48)
        dibujar_texto(f"Pista: {pista}", ANCHO // 2, 100, AZUL, tamaño=28)
        dibujar_ahorcado(errores)
        palabra_mostrada = " ".join(
            [letra if letra in letras_adivinadas else "_" for letra in palabra]
        )
        dibujar_texto(palabra_mostrada, ANCHO // 2, 400, BLANCO, tamaño=40)
        letras_usadas = " ".join(sorted(letras_adivinadas))
        dibujar_texto(f"Letras usadas: {letras_usadas}", ANCHO // 2, 450)
        tiempo_actual = time.time() - tiempo_inicial
        minutos = int(tiempo_actual // 60)
        segundos = int(tiempo_actual % 60)
        dibujar_texto(
            f"Tiempo: {minutos:02}:{segundos:02}", ANCHO - 100, 50, VERDE, tamaño=24
        )
        if "_" not in palabra_mostrada:
            dibujar_texto("¡Ganaste!", ANCHO // 2, 500, VERDE)
        elif errores >= max_errores:
            dibujar_texto(
                f"Perdiste. La palabra era: {palabra}.",
                ANCHO // 2,
                500,
                ROJO,
            )
        pygame.display.flip()
        reloj.tick(30)


if __name__ == "__main__":
    main()
