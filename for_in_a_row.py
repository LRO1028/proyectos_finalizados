import pygame
import numpy as np
import sys 
import math

#colores de tabla
Azul=(0,0,255)
Negro=(0,0,0)
Rojo=(255,0,0)
Amarillo=(255,255,0)

cantidad_de_filas=6
cantidad_de_columnas=7

def crear_tabla():
    tabla=np.zeros((cantidad_de_filas,cantidad_de_columnas) )
    return tabla

def caer_de_ficha(tabla,fila,columna,pieza):
    tabla[fila][columna]=pieza

def validacion_de_localizacion(tabla, columna):
    return tabla[cantidad_de_filas-1][columna]==0

def obtencion_de_fila_abierta(tabla, columna):
    for r in range(cantidad_de_filas):
        if tabla[r][columna]==0:
            return r

def mostrar_tabla(tabla):
    print(np.flip(tabla, 0))

def verificacion_de_victoria(tabla, pieza):
    #verificacion horizontal de cuatro en linea
    for c in range (cantidad_de_columnas-3):
        for r in range(cantidad_de_filas):
            if tabla[r][c]== pieza and tabla[r][c+1]==pieza and tabla[r][c+2]==pieza and tabla[r][c+3]==pieza:
                return True

    #verificacion vertical de cuatro en linea
    for c in range(cantidad_de_columnas):
        for r in range (cantidad_de_filas-3):
            if tabla[r][c]==pieza and tabla [r+1][c]==pieza and tabla[r+2][c]==pieza and tabla[r+3][c]==pieza:
                return True

    #verifciacion diagonal hacia adelante de cuatro en linea 
    for c in range(cantidad_de_columnas-3):
        for r in range(cantidad_de_filas-3):
            if tabla[r][c]==pieza and tabla [r+1][c+1]==pieza and tabla[r+2][c+2]==pieza and tabla[r+3][c+3]==pieza:
                return True

    #verificacion diagonal hacia atras de cuatro en linea
    for c in range (cantidad_de_columnas-3):
        for r in range (3,cantidad_de_filas):
            if tabla[r][c]== pieza and tabla[r-1][c+1]==pieza and tabla[r-2][c+2]==pieza and tabla[r-3][c+3]==pieza:
                return True

def dibujo_de_tabla(tabla):
    for c in range(cantidad_de_columnas):
        for r in range(cantidad_de_filas):
            pygame.draw.rect(screen, Azul, (c*tamaño_de_cuadro, r*tamaño_de_cuadro+tamaño_de_cuadro, tamaño_de_cuadro, tamaño_de_cuadro))
            pygame.draw.circle(screen, Negro, (int(c*tamaño_de_cuadro+tamaño_de_cuadro/2), int(r*tamaño_de_cuadro+tamaño_de_cuadro+tamaño_de_cuadro/2)), RADIUS)

    for c in range(cantidad_de_columnas):
        for r in range(cantidad_de_filas):
            if tabla[r][c]==1:
                pygame.draw.circle(screen, Rojo, (int(c*tamaño_de_cuadro+tamaño_de_cuadro/2), altura-int(r*tamaño_de_cuadro+tamaño_de_cuadro/2)), RADIUS)
            elif tabla[r][c]==2:
                pygame.draw.circle(screen, Amarillo, (int(c*tamaño_de_cuadro+tamaño_de_cuadro/2), altura-int(r*tamaño_de_cuadro+tamaño_de_cuadro/2)), RADIUS)
    pygame.display.update()

tabla=crear_tabla()
mostrar_tabla(tabla)
game_over=False
turno=0

pygame.init()

tamaño_de_cuadro=100

ancho=cantidad_de_columnas*tamaño_de_cuadro
altura=(cantidad_de_filas+1)*tamaño_de_cuadro

size=(ancho, altura)

RADIUS=int(tamaño_de_cuadro/2-5)

screen=pygame.display.set_mode(size)
dibujo_de_tabla(tabla)
pygame.display.update()

mi_frente=pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Negro, (0,0,ancho,tamaño_de_cuadro))
            posx=event.pos[0]
            if turno==0:
                pygame.draw.circle(screen, Rojo, (posx, int(tamaño_de_cuadro/2)), RADIUS)
            else:
                pygame.draw.circle(screen, Amarillo, (posx, int(tamaño_de_cuadro/2)), RADIUS)

        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Negro, (0,0,ancho,tamaño_de_cuadro))
            #pedir la entrada al jugador 1
            if turno==0:
                posx=event.pos[0]
                columna=int(math.floor(posx/tamaño_de_cuadro))

                if validacion_de_localizacion(tabla, columna):
                    fila = obtencion_de_fila_abierta(tabla, columna)
                    caer_de_ficha(tabla, fila, columna, 1)

                    if verificacion_de_victoria(tabla, 1):
                        etiqueta=mi_frente.render("Gana Jugador 1!", 1, Rojo)
                        screen.blit(etiqueta, (40,10)) #tamaño de cartel
                        game_over=True

            #pedir la entrada al jugador 2
            else:
                posx=event.pos[0]
                columna=int(math.floor(posx/tamaño_de_cuadro))

                if validacion_de_localizacion(tabla, columna):
                    fila=obtencion_de_fila_abierta(tabla,columna)
                    caer_de_ficha(tabla, fila, columna, 2)

                    if verificacion_de_victoria(tabla, 2):
                        etiqueta=mi_frente.render("Gana jugaodr 2!", 1, Amarillo)
                        screen.blit(etiqueta, (40,10))
                        game_over=True
            
            mostrar_tabla(tabla)
            dibujo_de_tabla(tabla)

            turno+=1
            turno=turno%2

            if game_over:
                pygame.time.wait(4000)
