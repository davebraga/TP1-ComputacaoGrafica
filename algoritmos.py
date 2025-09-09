import math
import objetos

# Irá calcular quais as coordenadas serão usadas para pintar cada pixel de (x1,y1) até (x2,y2). Baseado no algoritmo passado durante a aula
# Retorna o vetor com as coordenadas devidamente calculadas
def bresenham(x1, x2, y1, y2):
    coordenadas =[]
    x =x1
    y = y1
    deltaX = x2-x1
    deltaY = y2-y1
    Xincr = 0
    Yincr = 0

    coordenadas.append((x,y))
    if(deltaX > 0): Xincr = 1
    else:
        Xincr = -1
        deltaX = deltaX * -1

    if(deltaY > 0): Yincr = 1
    else:
        Yincr = -1
        deltaY = deltaY * -1


    if(deltaX > deltaY): #Primeiro caso
        p = 2 * deltaY - deltaX
        const1 = 2 * deltaY
        const2 = 2 * (deltaY - deltaX)
        for i in range(0,deltaX):
            x+= Xincr
            if(p > 0):
                p += const2
                y += Yincr
            else:
                p += const1
            coordenadas.append((x,y))
    else: #Segundo caso
        p = 2 * deltaX - deltaY
        const1 = 2 * deltaX
        const2 = 2 * (deltaX - deltaY)
        for i in range(0,deltaY):
            y += Yincr
            if(p < 0):
                p += const1
            else:
                p += const2
                x += Xincr
            coordenadas.append((x,y))

    return coordenadas


# Irá calcular as coordenadas para a criação de um círculo simétrico com base no ponto inicial e o raio dele definido pela função distancia
# Baseado no algoritmo passado durante a aula
def bresenhamCirculo(xCentro, yCentro, xRaio,yRaio):

    raio =  distancia(xCentro, yCentro, xRaio,yRaio) 
    coordenadas = []
    x = 0
    y = raio
    p = 3 - 2 * raio

    # Função auxiliar para desenhar todos os pontos simétricos
    def desenharPontos(cx, cy, px, py):
        coordenadas.append((cx + px, cy + py))
        coordenadas.append((cx - px, cy + py))
        coordenadas.append((cx + px, cy - py))
        coordenadas.append((cx - px, cy - py))
        coordenadas.append((cx + py, cy + px))
        coordenadas.append((cx - py, cy + px))
        coordenadas.append((cx + py, cy - px))
        coordenadas.append((cx - py, cy - px))

    while x <= y:
        desenharPontos(xCentro, yCentro, x, y)
        x += 1
        if p < 0:
            p += 4 * x + 6
        else:
            p += 4 * (x - y) + 10
            y -= 1
            
    return coordenadas

##Código para o recorte usando o algoritmo de Liang-Barsky. Baseado no algoritmo passado durante a aula
def liangBarsky(x1,y1,x2,y2,xmin,ymin,xmax,ymax):
    u1=0.0
    u2=1.0
    dx = x2-x1
    dy = y2-y1
    result = None

    def cliptest(p,q):
        nonlocal u1,u2 #Tem a lógica semelhante a de um ponteiro
        r = 0.0

        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > u2:
                    return False
                elif r > u1:
                    u1 = r
            else: # p > 0
                if r < u1:
                    return False
                elif r < u2:
                    u2 = r
        return True


    if (cliptest(-dx, x1 - xmin) and #Borda esquerda
        cliptest(dx, xmax - x1) and  #Borda direita
        cliptest(-dy, y1 - ymin) and #Borda superior
        cliptest(dy, ymax - y1)):    #Borda inferior
        
        # Se a linha for viável, recalcula os pontos finais
        if u2 < 1.0:
            x2 = x1 + dx * u2
            y2 = y1 + dy * u2
        if u1 > 0.0:
            x1 = x1 + dx * u1
            y1 = y1 + dy * u1
            
        result = objetos.Linha(round(x1),round(y1),round(x2),round(y2))

    return result

#Cálculo da distância Euclideana entre os pontos (x1,y1) até (x2,y2)
def distancia(x1,y1,x2,y2):
    deltaX = x2-x1
    deltaY = y2-y1

    return math.floor(math.sqrt((deltaX ** 2)+(deltaY ** 2)))
