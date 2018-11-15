import numpy as np
import copy
class conecta_cuatro:
    def __init__(self):
        self.FILAS = 6
        self.COLUMNAS = 7
        self.MOVIMIENTOS = [x+1 for x in range(self.COLUMNAS)]
        #Variables
        self.tablero = np.ones((self.FILAS,self.COLUMNAS)) 
        self.mov_disponibles = [1 for _ in range(self.COLUMNAS)]
        self.indice = [self.FILAS-1 for _ in range(self.COLUMNAS)]
        self.tiradas =[x+1 for x in range(self.COLUMNAS)]
        # Mensajes
        self.mensaje_columna_llena = 'La tirada no es valida, la columna esta llena'
        self.mensaje_tirada_invalida = 'La tirada no es valida debe selecionar una de las siguientes teclas: ' + str([x+1 for x in range(self.COLUMNAS)])
        # Variables de simulacion
        self.simulando = False
        self.copia_tablero = False 
        self.copia_mov_disponibles = False
        self.copia_indice = False
        
    def movimientos_disponibles(self):
        self.tiradas = []
        for columna in range(self.COLUMNAS):
            if self.tablero[0,columna] == 1:
                self.mov_disponibles[columna] = 1
                self.tiradas.append(columna+1)
            else:
                self.mov_disponibles[columna] = 0
        return self.mov_disponibles
    
    # las posiciones deven ir del 1 al 7
    def tirar(self,posicion,jugador):
        self.movimientos_disponibles()
        if posicion in self.MOVIMIENTOS:
            posicion -= 1 
            if self.mov_disponibles[posicion] == 0:
                self.mensaje = self.mensaje_columna_llena
            else:
                self.tablero[self.indice[posicion],posicion] = jugador
                self.indice[posicion] = self.indice[posicion]-1
                self.mensaje = False
        else:
            self.movimientos_disponibles()
            self.mensaje = self.mensaje_tirada_invalida    
    
    def obtener_entorno(self):
        return self.tablero,self.movimientos_disponibles(),self.indice
    
    def establecer_entorno(self,Datos):
        self.tablero,self.mov_disponibles,self.indice = Datos
        
    
    def con_num(self,s):
        try:
            return int(s)
        except ValueError:
            self.mensaje = self.mensaje_tirada_invalida
            return False

    def juego_terminado(self):
        if np.sum(self.mov_disponibles) == 0:
            return 3
        
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS-3):
                temp = np.array(copy.deepcopy(self.tablero[fila,columna:columna+4]))
                if np.sum(temp) == 0:
                    return 0
                elif np.sum(temp) == 8:
                    return 2
        
        for columna in range(self.COLUMNAS):
            for fila in range(self.FILAS-3):
                temp = np.array(copy.deepcopy(self.tablero[fila:fila+4,columna]))
                if np.sum(temp) == 0:
                    return 0
                elif np.sum(temp) == 8:
                    return 2

        t = copy.deepcopy(self.tablero)
        for fila in range(self.FILAS-3):
            for columna in range(self.COLUMNAS-3):
                temp = np.array(copy.deepcopy([t[fila,columna],t[fila+1,columna+1],t[fila+2,columna+2],t[fila+3,columna+3]]))
                if np.sum(temp) == 0:
                    return 0
                elif np.sum(temp) == 8:
                    return 2
        t = copy.deepcopy(self.tablero)  
        
        for fila in range(self.FILAS-3):
            for columna in range(3,self.COLUMNAS):
                temp = np.array(copy.deepcopy([t[fila,columna],t[fila+1,columna-1],t[fila+2,columna-2],t[fila+3,columna-3]]))   
                if np.sum(temp) == 0:
                    return 0
                elif np.sum(temp) == 8:
                    return 2
        return 1
            
if __name__ == '__main__':
    conecta_4 = conecta_cuatro()
    jugador = False
    for i in range(10):
        x = conecta_4.con_num(input('Tira jugador '+str(int(jugador)+1)+': '))
        if x:
            if jugador == False:
                conecta_4.tirar(x,0)
            else:
                conecta_4.tirar(x,2)
        print(conecta_4.tablero)
        print(conecta_4.mensaje)
        jugador = not(jugador)
    
