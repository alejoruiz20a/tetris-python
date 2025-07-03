import pygame
import random
import time
from formas import formas
from colores import colores

pygame.font.init()

#Variables globales
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 800
ANCHO_JUEGO = 350
ALTO_JUEGO = 700
TAMANO_BLOQUE = 35

INICIAL_X=(ANCHO_PANTALLA-ANCHO_JUEGO)//2
INICIAL_Y=ALTO_PANTALLA-ALTO_JUEGO

class Ficha(object):
    filas = 20
    columnas = 10
    def __init__(self,x,y,forma):
        self.x=x
        self.y=y
        self.forma=forma
        self.color=colores[formas.index(forma)]
        self.rotacion = 0
        
#esto guarda la posicion de las fichas que ya cayeron
def crearMatriz (posicionBloqueada = {}):
    # Crea una matriz de 10x20 con un codigo de color (#,#,#) en cada posi
    matriz = [[(0,0,0) for x in range (10)] for x in range(20)] 
    for i in range (len(matriz)): # Recorre el tamano de la matriz (20) cada fila
        for j in range(len(matriz[i])): # Recorre cada fila del primer bucle (10) 
            if (j,i) in posicionBloqueada: # Si la posicion (j,i) se encuentra en el diccionario de listas bloqueadas como una key,
                temp = posicionBloqueada[(j,i)] # guarda el valor de esa key en una variable temporal
                matriz[i][j] = temp # luego guarda la variable en la matriz principal, dejando el codigo de color (#,#,#) en la celda
    return matriz

def getFicha():
    return Ficha(5,3,random.choice(formas))

def mostrarFichaSiguiente(ficha,pantalla):
    pygame.font.init()
    fuente = pygame.font.SysFont('timesnewroman',30)
    label = fuente.render("Siguiente:",1,(255,255,255))
    
    pantalla.blit(label,(INICIAL_X+ANCHO_JUEGO+50,INICIAL_Y+ALTO_JUEGO//2-50))
    
    posicionFicha = ficha.forma[ficha.rotacion % len(ficha.forma)]
    
    for i, linea in enumerate(posicionFicha):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                pygame.draw.rect(pantalla,ficha.color,(INICIAL_X+ANCHO_JUEGO+j*TAMANO_BLOQUE+20,INICIAL_Y+ALTO_JUEGO//2+i * TAMANO_BLOQUE,TAMANO_BLOQUE,TAMANO_BLOQUE))

def dibujarMatriz (pantalla,matriz,grid):
    # dibujamos las lineas de la matriz
    if grid:
        for i in range(len(matriz)): # horizontales
            pygame.draw.line(pantalla,"grey",(INICIAL_X,INICIAL_Y + i * TAMANO_BLOQUE), (INICIAL_X + ANCHO_JUEGO, INICIAL_Y + i *TAMANO_BLOQUE))
            for j in range (len(matriz[i])): #Verticales
                pygame.draw.line(pantalla,"grey",(INICIAL_X +j*TAMANO_BLOQUE,INICIAL_Y), (INICIAL_X +j*TAMANO_BLOQUE, INICIAL_Y + ALTO_JUEGO))
    else:
        pass
    pygame.draw.line(pantalla,"red",(INICIAL_X,INICIAL_Y+3*TAMANO_BLOQUE),(INICIAL_X+ANCHO_JUEGO,INICIAL_Y+3*TAMANO_BLOQUE),5)

def pausado(pantalla,pause,running):
    fuente = pygame.font.SysFont("timesnewroman",60)
    label1 = fuente.render("PAUSA",1,"red","white")
    label2 = fuente.render("Presione P para continuar",1,"black","white")
    label3 = fuente.render("Presione R para reiniciar",1,"black","white")
    label4 = fuente.render("Presione ESC para salir",1,"black","white")
    pantalla.blit(label1,(ANCHO_PANTALLA//2-label1.get_width()//2,ALTO_PANTALLA//2-120))
    pantalla.blit(label2,(ANCHO_PANTALLA//2-label2.get_width()//2,ALTO_PANTALLA//2-60))
    pantalla.blit(label3,(ANCHO_PANTALLA//2-label3.get_width()//2,ALTO_PANTALLA//2))
    pantalla.blit(label4,(ANCHO_PANTALLA//2-label4.get_width()//2,ALTO_PANTALLA//2+60))

    pygame.display.update()
    while pause: #Bucle mientra esté en pausa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause=False
                if event.key == pygame.K_r:
                    pause = False
                    running=False
                    main()    
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    pygame.quit()
    pygame.display.update()

def dibujarVentana(pantalla,matriz,grid):
    pantalla.fill((0,0,0))
    
    pygame.font.init()
    
    fuente = pygame.font.SysFont('timesnewroman',60)
    fuente2 = pygame.font.SysFont('timesnewroman',20)
    label = fuente.render("TETRIS",1,"red")
    labelDev = fuente2.render("Dev: Alejandro Amador",1,"white")
    
    pantalla.blit(label,(INICIAL_X + ANCHO_JUEGO/2 - (label.get_width()/2),15))
    pantalla.blit(labelDev,(5,ALTO_PANTALLA-25))
    
    for i in range(len(matriz)):
        for j in range (len(matriz[i])):
            pygame.draw.rect(pantalla,matriz[i][j],(INICIAL_X+j*TAMANO_BLOQUE,INICIAL_Y+i*TAMANO_BLOQUE,TAMANO_BLOQUE,TAMANO_BLOQUE))
            
    pygame.draw.rect(pantalla, "white",(INICIAL_X-3,INICIAL_Y-3,ANCHO_JUEGO+7,ALTO_JUEGO+3),4)        
    dibujarMatriz(pantalla,matriz,grid)
    
def eliminarFilas(matriz, bloqueado, puntuacion, pantalla):
    indice = 0
    incremento = 0
    for i,fila in enumerate(matriz):
        if not (0,0,0) in fila:
            incremento += 1
            indice = i
            for k in range(10):
                del bloqueado[(k,i)]
                
    if incremento>0:
        for key in sorted(list(bloqueado))[::-1]: # recorre una lista con solo las keys de bloqueado
            x,y = key #extrae el valor x y y de la key
            if y < indice: # si la coordenada y es mayor al indice en el que se eliminó una fila, entonces
                newKey = (x,y + incremento) #crea una nueva key, en la que guarda el valor de x, y y con el incremento (cantidad de filas borradas)
                bloqueado[newKey] = bloqueado.pop(key)  #ahora bien, una vez hace esto, añade la key a bloqueado y le da el value de la key inicial    
        puntuacion = puntuacion + incremento*1000 #finalmente debido a que hubo un incremento, se añaden mil puntos por fila eliminada
    return puntuacion
    
              
    
def validarMovimiento(ficha,matriz): #esta funcion define si el movimiento a realizar es valido
    posicionAceptada = [[(j,i) for j in range(10) if matriz[i][j] == (0,0,0)] for i in range (20)]
    # Hace una matriz de posiciones posibles recorriendo la matriz para ver si tien el codigo de color 0,0,0
    posicionAceptada = [elemento for fila in posicionAceptada for elemento in fila]
    # esta linea lo que hace es aplanar la matriz, para que quede como una lista
    
    posicionFicha = convertirForma(ficha) # linea 156
    
    #recorremos la matriz posiciones buscando si todas sus coordenadas están en la lista de posiciones aceptadas
    for pos in posicionFicha:
        if pos not in posicionAceptada: 
            return False
    return True        

def getGameOver(posiciones):
    for pos in posiciones:
        x,y = pos
        if y < 3:
            return True
    return False

def convertirForma(ficha):
    posiciones = [] # esta lista guardará las posiciones de donde hay cuadros en la matriz
    
    lado = ficha.forma[ficha.rotacion % len(ficha.forma)] # define en que rotaicon está la ficha
    
    #esto es de lo más rarito de entender
    for i, linea in enumerate(lado): #recorremos indice, linea (# ...00.)
        fila = list(linea) #se pasa a lista, pues linea es un string
        for j, columna in enumerate(fila): #hace lo mismo pero ahora recorriendo el string (ahora lista)
            if columna == '0':
                posiciones.append((ficha.x + j, ficha.y + i)) #si la posicion tiene un cero, agrega a posiciones la coordenada donde se ubica el cuadro
                
    for i, posicion in enumerate (posiciones) :  #esto es para que spawneen bien jasjasajsja
        posiciones[i] = (posicion[0]-2,posicion[1]-4)

    return posiciones # retorna las coordenadas en donde hay cuadrados ocupados

def mostrarPuntuacion(puntuacion,pantalla):
    pygame.font.init()
    fuente = pygame.font.SysFont('timesnewroman',30)
    label1 = fuente.render((f"Puntuacion:"),1,(255,255,255))
    label2 = fuente.render(str(puntuacion),1,(255,255,255))
    pantalla.blit(label1,(50,ALTO_JUEGO//2+100))
    pantalla.blit(label2,(100,ALTO_JUEGO//2+150))
    
def mostrarGameOver(pantalla,puntuacion,matriz,posicionesBloqueadas):
    pygame.font.init()
    fuente = pygame.font.SysFont('timesnewroman',50)
    label1 = fuente.render((f"FIN DEL JUEGO"),1,"red")
    label2 = fuente.render(str(puntuacion)+" puntos",1,"white")
    label3 = fuente.render("Presione ESC para salir",1,"white")
    label4 = fuente.render("Presione R para reiniciar",1,"white")
    pygame.draw.rect(pantalla,"black",(0,0,ANCHO_PANTALLA,ALTO_PANTALLA))

    pantalla.blit(label1,(ANCHO_PANTALLA//2-label1.get_width()//2,ALTO_PANTALLA//2-100))
    pantalla.blit(label2,(ANCHO_PANTALLA//2-label2.get_width()//2,ALTO_PANTALLA//2-50))
    pantalla.blit(label3,(ANCHO_PANTALLA//2-label3.get_width()//2,ALTO_PANTALLA//2))
    pantalla.blit(label4,(ANCHO_PANTALLA//2-label4.get_width()//2,ALTO_PANTALLA//2+50))

    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run=False
                if event.key == pygame.K_r:
                    main()  
    pygame.display.update()

    
#MAIN
def main():
    posicionesBloqueadas = {} # diccionario que guarda que posiciones están ocupadas, las keys serían un tuple con la posicion, y los
                              # values serían un tuple con los tres valores RGB del color que esta ocupando la celda
    
    pygame.mixer.init()
    pygame.mixer_music.load("theme.mp3")
    pygame.mixer_music.play(-1)
    music = True
    
    cambiarFicha = False 
    pause = False 
    running = True 
    fichaActual = getFicha() 
    nextFicha = getFicha() 
    clock = pygame.time.Clock() 
    tiempoCaida = 0 #Define cuanto tiempo ha pasado desde que la ficha cayó
    velocidadCaida=0.8 # Define que tanto tiempo debe pasar entre cada descenso
    puntuacion=0 
    grid = True
    
    # Inicia el bucle principal del juego
    while running:
        matriz = crearMatriz(posicionesBloqueadas) # linea 30 - aquí ocurre toda la magia
        tiempoCaida += clock.get_rawtime() #cada iteracion, rawtime suma el tiempo que pasa en cada iteracion a la variable
        clock.tick() # requisitos raros del clock
            #se divide entre mil para convertir en segundos
        if tiempoCaida / 1000 > velocidadCaida: #cuando sea mayor a la velocidad
            tiempoCaida=0 #se reinicia
            fichaActual.y += 1 #y se aumenta la posicion en y de la ficha, haciendola caer
                        # linea 135
            if not (validarMovimiento(fichaActual,matriz)) and fichaActual.y > 0: # revisa si el movimiento es valido y si está por debajo de y=0
                fichaActual.y -= 1 # si lo anterior no se cumple, la ficha se regresa una posicion 
                cambiarFicha = True # y se define que cambie la ficha
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Pa salir
            if event.type== pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # si se presiona una direccion
                    fichaActual.x -=1           # se aumenta o disminuye en esa direccion
                    if not(validarMovimiento(fichaActual,matriz)): # pero is el movimiento no es valido
                        fichaActual.x += 1      # se revierte la accion
                if event.key == pygame.K_RIGHT:
                    fichaActual.x += 1
                    if not(validarMovimiento(fichaActual,matriz)):
                        fichaActual.x -=1
                if event.key == pygame.K_DOWN:
                    fichaActual.y += 1
                    if not(validarMovimiento(fichaActual,matriz)):
                        fichaActual.y -=1
                if event.key == pygame.K_UP:
                    fichaActual.rotacion += 1
                    if not(validarMovimiento(fichaActual,matriz)):
                        fichaActual.rotacion -= 1
                if event.key == pygame.K_p:
                    pause=True
                    pygame.mixer_music.pause()
                    pausado(pantalla,pause,running) #linea 66
                    pygame.mixer_music.unpause()
                    pause=False
                if event.key == pygame.K_m:
                    if music:
                        pygame.mixer_music.pause()
                        music=False
                    else:
                        pygame.mixer_music.unpause()
                        music=True
                if event.key == pygame.K_l:
                    if grid:
                        grid=False
                    else:
                        grid=True
        
        posicionFicha = convertirForma(fichaActual) #Volvemos a tomar las posiciones ocupadas por la ficha que está cayendo
        
        # aquí es donde pasamos las posiciones de la ficha a la matriz principal (se encarga de la ficha que va cayendo)
        for i in range(len(posicionFicha)):
            y,x = posicionFicha[i]
            matriz[x][y] = fichaActual.color #tomando el color y guardandolo en el lugar de (0,0,0)
                
        if cambiarFicha: # si se define que se debe generar una nueva ficha
            for pos in posicionFicha:
                p = (pos[0],pos[1])
                posicionesBloqueadas[p] = fichaActual.color #guarda las coordenadas de la ficha que cayó en el diccionario posiciones bloqueadas
            fichaActual = nextFicha
            nextFicha = getFicha() # cambiamos a la siguiente ficha y generamos una nueva para la siguiente
            cambiarFicha=False #reiniciamos cambiar variable
                            #linea 108
            newPuntuacion=eliminarFilas(matriz,posicionesBloqueadas,puntuacion,pantalla) #con esta funcion se eliminan las filas y se suma puntuacion
            if newPuntuacion>puntuacion and velocidadCaida>0.1: #aqui se aumenta la dificultad del juego
                velocidadCaida=velocidadCaida-((newPuntuacion-puntuacion)*0.00002)
            puntuacion=newPuntuacion
        
        dibujarVentana(pantalla,matriz,grid)   #linea 89
        mostrarFichaSiguiente(nextFicha,pantalla) # muestra la ficha que sigue, linea 41
        mostrarPuntuacion(puntuacion,pantalla) #muestra la puntuación del usuario
        pygame.display.update()             
        
        if getGameOver(posicionesBloqueadas):
            pygame.mixer_music.stop()
            mostrarGameOver(pantalla,puntuacion,matriz,posicionesBloqueadas)
            running = False
        
def mainMenu():
    pygame.font.init()
    fuente = pygame.font.SysFont('timesnewroman',50)
    fuente2 = pygame.font.SysFont('timesnewroman',100)
    label1 = fuente2.render(("TETRIS"),1,"red")
    label2 = fuente.render("Presione espacio para iniciar",1,"white")
    label3 = fuente.render("Presione ESC para salir",1,"white")
    pygame.draw.rect(pantalla,"black",(0,0,ANCHO_PANTALLA,ALTO_PANTALLA))

    pantalla.blit(label1,(ANCHO_PANTALLA//2-label1.get_width()//2,INICIAL_Y))
    pantalla.blit(label2,(ANCHO_PANTALLA//2-label2.get_width()//2,ALTO_PANTALLA//2-50))
    pantalla.blit(label3,(ANCHO_PANTALLA//2-label3.get_width()//2,ALTO_PANTALLA//2))

    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    run=False
    pygame.display.update()
    main()

pantalla = pygame.display.set_mode((ANCHO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption("TETRIS")
mainMenu() #finalmente se inicia el juego

