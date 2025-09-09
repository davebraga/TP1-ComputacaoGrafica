##Classe base
class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
def movePosicao(posAtual,novaPos): 
    return posAtual + (novaPos - posAtual)

## Definido por um ponto inicial e um final
class Linha:
    def __init__(self, x1,y1,x2,y2):
        self.inicial = Ponto(x1,y1)
        self.final = Ponto(x2,y2)
        self.tipo = "linha"
    
    def getInicial(self):
        return self.inicial
    
    def getFinal(self):
        return self.final

    def getPontos(self):
        return [self.inicial, self.final]
    
    def getTipo(self):
        return self.tipo
    
##Definido pelo ponto central e raio
class Circulo:
    def __init__(self, x1,y1, raio):
        self.centro = Ponto(x1,y1)
        self.raio = raio
        self.tipo = "circulo"

    def getCentro(self):
        return self.centro
    
    def getRaio(self):
        return self.raio
    
    def getTipo(self):
        return self.tipo
    

##Retangulo de seleção
class Retangulo:
    def __init__(self,x1,y1,x2,y2):
        self.p1 = Ponto(x1,y1)
        self.p2 = Ponto(x1,y2)
        self.p3 = Ponto(x2,y1)
        self.p4 = Ponto(x2,y2)
    
    def getPontos(self):
        return[self.p1,self.p2,self.p3,self.p4]
    

