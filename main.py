import tkinter as tk
import math
import algoritmos, objetos as o

LARGURA = 800
ALTURA = 600
tela = None
points = []
pontoSelecao = []
elementosNaTela = []
elementosSelecionados = []
modoAtual = None
statusbar = None

xmin = 0
xmax = 0
ymin = 0
ymax = 0

def setModoLinha():
    global modoAtual
    modoAtual = "Linha"
    updateStatus("Clique para poder adicionar o primeiro ponto")

def setModoCirculo():
    global modoAtual
    modoAtual = "Circulo"
    updateStatus("Clique para definir onde será o raio do círculo")

def setModoTranslacao():
    global modoAtual
    modoAtual = "Translação"
    updateStatus("Clique para aonde deseja mover o(s) elemento(s) selecionado(s)")

def setModoRotacao():
    global modoAtual
    modoAtual = "Rotação"
    updateStatus("Digite em graus o quanto deseja rotacionar os elementos")

def setModoReflexao():
    global modoAtual
    modoAtual = "Reflexão"
    updateStatus("Escolha o tipo de Reflexão desejada")

def setModoSelecionar():
    global modoAtual
    modoAtual = "Selecionar"
    updateStatus("Clique para definir onde será a diagonal da área de seleção")

def updateStatus(texto):
    global statusbar
    if statusbar:
        statusbar.config(text=texto)


def getRotation():
    
    dialog = tk.Toplevel()
    dialog.title("Ângulo de Rotação")
    
    dialog.grab_set()
    
    tk.Label(dialog, text="Insira o ângulo em graus:").pack(padx=10, pady=5)
    
    angulo = tk.Entry(dialog)
    angulo.pack(padx=10, pady=5)
    
    # O botão de confirmar vai chamar uma função que lida com a rotação
    def on_confirm():
        try:
            result = float(angulo.get())
            dialog.destroy()
            # Chama a função principal de rotação
            modoRotacao(result)
        except ValueError:
            tk.messagebox.showerror("Erro! Insira um número válido.")
            
    tk.Button(dialog, text="OK", command=on_confirm).pack(pady=10)
    
    # Mantém o foco no diálogo
    dialog.focus_set()
    dialog.wait_window()

def getReflexao():
    dialog = tk.Toplevel()
    dialog.title("Tipo de Reflexão")
    dialog.grab_set()  # Faz a janela ser modal
    
    tk.Label(dialog, text="Selecione o tipo de reflexão:").pack(padx=10, pady=5)
    
    # Cria os botões para cada opção
    def reflectX():
        dialog.destroy()
        modoReflexao('x')
    
    def reflectY():
        dialog.destroy()
        modoReflexao('y')
        
    def reflectXY():
        dialog.destroy()
        modoReflexao('xy')

    tk.Button(dialog, text="Eixo X", command=reflectX).pack(pady=5)
    tk.Button(dialog, text="Eixo Y", command=reflectY).pack(pady=5)
    tk.Button(dialog, text="Eixo X e Y (Origem)", command=reflectXY).pack(pady=5)
    
    dialog.focus_set()
    dialog.wait_window()

def pintaPixel(x,y,cor):
    tela.create_rectangle(x, y, x + 1, y + 1, fill=cor, outline=cor)

def pintaLinha(linha, cor):
    x1 = linha.getInicial().getX()
    y1 = linha.getInicial().getY()
    x2 = linha.getFinal().getX()
    y2 = linha.getFinal().getY()

    coordenadas = algoritmos.bresenham(x1,x2,y1,y2)

    for i in range(0,len(coordenadas)):
        x, y = coordenadas[i]
        #print("("+ str(x) +","+ str(y) +")")
        pintaPixel(x,y,cor)

def pintaCirculo(c1,c2,r1,r2,cor):
    coordenadas = algoritmos.bresenhamCirculo(c1,c2,r1,r2)

    for i in range(0,len(coordenadas)):
        x, y = coordenadas[i]
        print("("+ str(x) +","+ str(y) +")")
        pintaPixel(x,y,cor)


def limpaLinha(x1,y1,x2,y2):
    linha = o.Linha(x1,y1,x2,y2)
    pintaLinha(linha,"#0E1D24")

    ##Sefor uma linha inteira, ele irá excluir o seu todo do elemento
    for i in range(0,len(elementosNaTela)):
        if(elementosNaTela[i].getTipo() == "linha"):
            linha = elementosNaTela[i]
            xi = linha.getInicial().getX()
            yi = linha.getInicial().getY()
            xj = linha.getFinal().getX()
            yj = linha.getFinal().getY()
        if(x1 == xi and y1 == yi and x2 == xj and y2 == yj):
            elementosNaTela.pop(i)
            return

def limpaCirculo(x1,y1,raio):
    for i in range(0,len(elementosNaTela)):
        if(elementosNaTela[i].getTipo() == "circulo"):
            circulo = elementosNaTela[i]
            xi = circulo.getCentro().getX()
            yi = circulo.getCentro().getY()
            raioi = circulo.getRaio()
        if(x1 == xi and y1 == yi and raioi == raio):
            elementosNaTela.pop(i)
            pintaCirculo(x1,y1,x1+raio,y1,"#0E1D24")
            return

def modoLinha(event):
    global points, tela, elementosNaTela
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    #Adiciona o ponto na tela
    points.append((event.x, event.y))
    print("Ponto" + str(len(points)) +" : " + str(event.x) + "," + str(event.y))

    updateStatus("Clique novamente para poder adicionar o segundo ponto")

    if len(points) % 2 == 0:
        x1,y1 = points[len(points)-2]
        x2,y2 = points[len(points)-1]

        ##Adiciona o objeto linha nos elementos 
        linha = o.Linha(x1,y1,x2,y2)
        pintaLinha(linha,"white")
        elementosNaTela.append(linha)
        updateStatus("")
    
def modoCirculo(event):
    global points, tela, elementosNaTela

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    #Adiciona o ponto na tela
    points.append((event.x, event.y))
    print("Ponto" + str(len(points)) +" : " + str(event.x) + "," + str(event.y))

    updateStatus("Clique novamente para definir o raio do círculo")
    if len(points) % 2 == 0:
        x1,y1 = points[len(points)-2]
        x2,y2 = points[len(points)-1]

        pintaCirculo(x1,y1,x2,y2,"white")

        ##Adiciona o objeto circulo nos elementos 
        raio = algoritmos.distancia(x1,y1,x2,y2)
        circulo = o.Circulo(x1,y1,raio)
        elementosNaTela.append(circulo)
        updateStatus("")

def modoSelecionar(event):
    global tela, elementosNaTela, elementosSelecionados, pontoSelecao
    global xmin,xmax,ymin,ymax


    #Adiciona o ponto na tela
    pontoSelecao.append((event.x, event.y))
    print("Ponto" + str(len(pontoSelecao)) +" : " + str(event.x) + "," + str(event.y))

    updateStatus("Clique novamente para definir onde será a outra diagonal da área de seleção")

    if (len(pontoSelecao) % 2 == 0):
        x1,y1 = pontoSelecao[len(pontoSelecao)-2]
        x2,y2 = pontoSelecao[len(pontoSelecao)-1]

        if (len(elementosSelecionados)>1 or xmin !=0): #Caso a ferramenta de seleção já tenha sido usada, irá limpar a seleção

            pintaLinha(o.Linha(xmin,ymin,xmin,ymax),"#0E1D24")
            pintaLinha(o.Linha(xmin,ymin,xmax,ymin),"#0E1D24")
            pintaLinha(o.Linha(xmax,ymin,xmax,ymax),"#0E1D24")
            pintaLinha(o.Linha(xmin,ymax,xmax,ymax),"#0E1D24")

            for i in range(0,len(elementosSelecionados)):
                if(elementosSelecionados[i].getTipo()=="linha"):
                    pintaLinha(elementosSelecionados[i],"white")

                elif(elementosSelecionados[i].getTipo()=="circulo"):
                    pintaCirculo(elementosSelecionados[i].getCentro().getX(),elementosSelecionados[i].getCentro().getY(),elementosSelecionados[i].getCentro().getX() + elementosSelecionados[i].getRaio(),elementosSelecionados[i].getCentro().getY(),"white")

            elementosSelecionados.clear()

        xmin = min(x1, x2)
        ymin = min(y1, y2)
        xmax = max(x1, x2)
        ymax = max(y1, y2)

        pintaLinha(o.Linha(xmin,ymin,xmin,ymax),"grey")
        pintaLinha(o.Linha(xmin,ymin,xmax,ymin),"grey")
        pintaLinha(o.Linha(xmax,ymin,xmax,ymax),"grey")
        pintaLinha(o.Linha(xmin,ymax,xmax,ymax),"grey")
        

        for i in range(0,len(elementosNaTela)):
            if (elementosNaTela[i].getTipo() == "linha"):
                x1 = elementosNaTela[i].getInicial().getX()
                y1 = elementosNaTela[i].getInicial().getY()
                x2 = elementosNaTela[i].getFinal().getX()
                y2 = elementosNaTela[i].getFinal().getY()

                elemento = algoritmos.liangBarsky(x1,y1,x2,y2,xmin,ymin,xmax,ymax)
                if(elemento!=None):
                    elementosSelecionados.append(elemento)
                    pintaLinha(elemento,"yellow")
            elif(elementosNaTela[i].getTipo()=="circulo"):
                x1 = elementosNaTela[i].getCentro().getX()
                y1 = elementosNaTela[i].getCentro().getY()
                if(x1>xmin and x1<xmax and y1>ymin and y1<ymax):
                    pintaCirculo(x1,y1, x1 + elementosNaTela[i].getRaio(),y1,"yellow")
                    elementosSelecionados.append(elementosNaTela[i])
            
        pontoSelecao.clear()


def modoTranslacao(event):
    global tela, elementosNaTela, elementosSelecionados
    global xmin,xmax,ymin,ymax
    pontoMov = []

    if(len(elementosSelecionados)<1): 
        updateStatus("É preciso selecionar um elemento primeiro!")
        return
    
    pontoMov.append((event.x, event.y))
    xMov,yMov = pontoMov[0]

    ##Irá se movimentar com base no centro do retangulo de seleção
    xCentro= round(xmin + (xmax-xmin)/2)
    yCentro= round(ymin + (ymax-ymin)/2)

    xDif = o.movePosicao(xCentro,xMov) - xCentro
    yDif = o.movePosicao(yCentro,yMov) - yCentro
    for i in range (0,len(elementosSelecionados)):
        if(elementosSelecionados[i].getTipo() == "linha"):

            #Limpa o elemento atual do quadro
            linha = elementosSelecionados[i]
            x1 = linha.getInicial().getX()
            y1 = linha.getInicial().getY()
            x2 = linha.getFinal().getX()
            y2 = linha.getFinal().getY()
            limpaLinha(x1,y1,x2,y2)

            #Adiciona o elemento transladado
            x1 = x1 + xDif
            y1 = y1 + yDif
            x2 = x2 + xDif 
            y2 = y2 + yDif 

            print("Nova posição Inicial: ("+str(x1)+","+str(y1)+")")
            print("Nova posição Final: ("+str(x2)+","+str(y2)+")")

            linha = o.Linha(x1,y1,x2,y2)
            pintaLinha(linha,"white")
            elementosNaTela.append(linha)
            updateStatus("")

        elif(elementosSelecionados[i].getTipo() == "circulo"):    
            circulo = elementosSelecionados[i]
            #Limpa o elemento atual do quadro
            x1 = circulo.getCentro().getX()
            y1 = circulo.getCentro().getY()
            raio = circulo.getRaio()
            limpaCirculo(x1,y1,raio)

            x1 = o.movePosicao(x1,xMov)
            y1 = o.movePosicao(y1,yMov)

            circulo = o.Circulo(x1,y1,raio)
            pintaCirculo(x1,y1,x1+raio,y1,"white")
            elementosNaTela.append(circulo)
            updateStatus("")
        
    elementosSelecionados.clear()

def modoRotacao(angulo):
    global tela, elementosNaTela, elementosSelecionados
    global xmin,xmax,ymin,ymax

    if(len(elementosSelecionados)<1): 
        updateStatus("É preciso selecionar um elemento primeiro!")
        return
    
    ##O centro do retângulo é o pivô de rotação dos elementos
    xPivo= round(xmin + (xmax-xmin)/2)
    yPivo= round(ymin + (ymax-ymin)/2)

    radianos = math.radians(angulo)
    cosTheta = math.cos(radianos)
    sinTheta = math.sin(radianos)

    for i in range (0,len(elementosSelecionados)):
        if(elementosSelecionados[i].getTipo() == "linha"):

            #Limpa o elemento atual do quadro
            linha = elementosSelecionados[i]
            x1 = linha.getInicial().getX()
            y1 = linha.getInicial().getY()
            x2 = linha.getFinal().getX()
            y2 = linha.getFinal().getY()
            limpaLinha(x1,y1,x2,y2)

            # Rotação do ponto inicial
            x1_rot = (x1 - xPivo) * cosTheta - (y1 - yPivo) * sinTheta
            y1_rot = (x1 - xPivo) * sinTheta + (y1 - yPivo) * cosTheta
            x1 = x1_rot + xPivo
            y1 = y1_rot + yPivo
            
            # Rotação do ponto final
            x2_rot = (x2 - xPivo) * cosTheta - (y2 - yPivo) * sinTheta
            y2_rot = (x2 - xPivo) * sinTheta + (y2 - yPivo) * cosTheta
            x2 = x2_rot + xPivo
            y2 = y2_rot + yPivo

            linha = o.Linha(round(x1),round(y1),round(x2),round(y2))
            pintaLinha(linha,"white")
            elementosNaTela.append(linha)
            updateStatus("")

        elif(elementosSelecionados[i].getTipo() == "circulo"):
            circulo = elementosSelecionados[i]
            #Limpa o elemento atual do quadro
            x1 = circulo.getCentro().getX()
            y1 = circulo.getCentro().getY()
            raio = circulo.getRaio()
            limpaCirculo(x1,y1,raio)

            # Rotação do ponto central do círculo
            x1_rot = (x1 - xPivo) * cosTheta - (y1 - yPivo) * sinTheta
            y1_rot = (x1 - xPivo) * sinTheta + (y1 - yPivo) * cosTheta
            x1 = x1_rot + xPivo
            y1 = y1_rot + yPivo

            print("Nova posição: ("+str(x1)+","+str(y1)+")")

            circulo = o.Circulo(round(x1),round(y1),raio)
            pintaCirculo(x1,y1,x1+raio,y1,"white")
            elementosNaTela.append(circulo)
            updateStatus("")
        
    elementosSelecionados.clear()
             
def modoReflexao(opcao):

    #O centro do retangulo de seleção será a base X/Y para espelhamento
    xCentro= round(xmin + (xmax-xmin)/2)
    yCentro= round(ymin + (ymax-ymin)/2)

    for i in range (0,len(elementosSelecionados)):
        if(elementosSelecionados[i].getTipo() == "linha"):

            #Limpa o elemento atual do quadro
            linha = elementosSelecionados[i]
            x1 = linha.getInicial().getX()
            y1 = linha.getInicial().getY()
            x2 = linha.getFinal().getX()
            y2 = linha.getFinal().getY()
            limpaLinha(x1,y1,x2,y2)

            match opcao:
                case 'x':
                    x1 = x1 + 2*(xCentro-x1) if xCentro >= x1  else x1 - 2*(xCentro-x1)
                    x2 = x2 + 2*(xCentro-x2) if xCentro >= x2  else x2 - 2*(xCentro-x2)
                case 'y':
                    y1 = y1 + 2*(yCentro-y1) if xCentro >= y1  else y1 - 2*(xCentro-y1)
                    y2 = y2 + 2*(yCentro-y2) if xCentro >= y2  else y2 - 2*(xCentro-y2)
                case 'xy':    
                    x1 = x1 + 2*(xCentro-x1) if xCentro >= x1  else x1 - 2*(xCentro-x1)
                    x2 = x2 + 2*(xCentro-x2) if xCentro >= x2  else x2 - 2*(xCentro-x2)
                    y1 = y1 + 2*(yCentro-y1) if xCentro >= y1  else y1 - 2*(xCentro-y1)
                    y2 = y2 + 2*(yCentro-y2) if xCentro >= y2  else y2 - 2*(xCentro-y2)
            
            linha = o.Linha(x1,y1,x2,y2)
            pintaLinha(linha,"white")
            elementosNaTela.append(linha)
            updateStatus("")
        
        elif(elementosSelecionados[i].getTipo() == "circulo"):
            circulo = elementosSelecionados[i]
            #Limpa o elemento atual do quadro
            x1 = circulo.getCentro().getX()
            y1 = circulo.getCentro().getY()
            raio = circulo.getRaio()
            limpaCirculo(x1,y1,raio)

            match opcao:
                case 'x':
                    x1 = x1 + 2*(xCentro-x1) if xCentro >= x1  else x1 - 2*(xCentro-x1)
                case 'y':
                    y1 = y1 + 2*(yCentro-y1) if xCentro >= y1  else y1 - 2*(xCentro-y1)
                case 'xy':    
                    x1 = x1 + 2*(xCentro-x1) if xCentro >= x1  else x1 - 2*(xCentro-x1)
                    y1 = y1 + 2*(yCentro-y1) if xCentro >= y1  else y1 - 2*(xCentro-y1)

            print("Nova posição: ("+str(x1)+","+str(y1)+")")

            circulo = o.Circulo(round(x1),round(y1),raio)
            pintaCirculo(x1,y1,x1+raio,y1,"white")
            elementosNaTela.append(circulo)
            updateStatus("")

    elementosSelecionados.clear()    


# Mapeia os modos para as funções de tratamento
modoHandlers = {
    "Linha": modoLinha,
    "Circulo": modoCirculo,
    "Selecionar": modoSelecionar,
    "Translação": modoTranslacao,
    "Rotação": modoRotacao,
    "Reflexão": modoReflexao
}

def on_click(event):
    # Obtém a função correta do dicionário e a executa
    handler = modoHandlers.get(modoAtual)
    if handler:
        handler(event)


def main():

    global tela,statusbar

    # Janela Principal
    root = tk.Tk()
    root.title("TP1 CG")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Cria o menu de Transformações
    transfmenu = tk.Menu(menubar, tearoff=0)
   
    statusbar = tk.Label(root, text="Pronto", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    menubar.add_command(label="Linha", command= setModoLinha)
    menubar.add_command(label="Círculo", command= setModoCirculo)
    menubar.add_command(label="Selecionar", command= setModoSelecionar)

    menubar.add_cascade(label="Transformações", menu=transfmenu)

    transfmenu.add_command(label="Translação", command=setModoTranslacao)
    transfmenu.add_command(label="Rotação", command=getRotation)
    transfmenu.add_command(label="Reflexão", command=getReflexao)

    tela = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="#0E1D24", highlightthickness=1, highlightbackground="white")
    tela.pack(pady=10, padx=10)
    tela.bind("<Button-1>", on_click)

    root.mainloop()

if __name__ == "__main__": main()
