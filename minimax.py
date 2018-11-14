# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 22:34:00 2018

@author: delga
"""
import numpy as np
import conecta_cuatro
import copy
class minimax:
    def __init__(self,conecta_4, nivel):
        self.mundo = copy.deepcopy(conecta_4)
        self.nivel = nivel
        self.jugador = [2,0]
        self.actualizar = False
    
    def minmax(self,entorno):
        queue = []
        self.actualizar = False
        self.mundo.establecer_entorno(copy.deepcopy(entorno))
        estado = self.optener_valores()
        queue.append(estado)
        nivel = 0
        jugador = False
        while(not(queue[0][2]) or queue[1][1] == queue[1][4]):
            #print('nivel: ', nivel,' Valor:', queue[nivel][5],self.nivel)
            #1
            #0print(self.mundo.tablero)
            if nivel != self.nivel:
                if queue[nivel][1] != queue[nivel][4]:
                    self.mundo.tirar(queue[nivel][3][queue[nivel][1]],self.jugador[int(jugador)])
                    queue[nivel][1] += 1
                    jugador = not(jugador)

                    if len(queue)<=self.nivel and self.actualizar == False:
                        #print(nivel,' len(q): ',len(queue))
                        queue.append(self.optener_valores())
                    if self.actualizar:
                        nivel += 1
                        self.actualizar = False
                        queue[nivel][0] = copy.deepcopy(self.mundo.obtener_entorno())
                    else:
                        nivel += 1

                else:
                    jugador = not(jugador)
                    if jugador:        # Minimiza             # Si tiro la maquina jugador es verdadero pero se almacenara en el nivel anterior por lo tanto se minimiza 
                        if not(queue[nivel][2]) or queue[nivel][2]>queue[nivel+1][2]: #Si el nivel anterior no tiene valor o el valor del tablero es menor al guardado 
                            queue[nivel][2] = queue[nivel+1][2]     # Actualiza  valor del nivel anterior
                            queue[nivel][5] = queue[nivel-1][1]-1  # Actualiza indice del nivel anterior   
                        if nivel - 1 >=0:
                            nivel -= 1
                            queue[nivel+1][1] = 0
                            self.actualizar = True
                            self.mundo.establecer_entorno(copy.deepcopy(queue[nivel][0]))
                            queue.pop()
                    else:
                        if not(queue[nivel][2]) or queue[nivel][2]<queue[nivel+1][2]:
                                queue[nivel][2] = queue[nivel+1][2]
                                queue[nivel][5] = queue[nivel-1][1]-1
                        if nivel - 1 >=0:
                            nivel -= 1
                            queue[nivel+1][1] = 0
                            self.mundo.establecer_entorno(copy.deepcopy(queue[nivel][0]))
                            self.actualizar = True
                            queue.pop()
                    
            #########################################################################################
            #########################################################################################
            else:
                valor_tablero = self.funcion_de_evaluacion()
                if queue[nivel-1][1] < queue[nivel-1][4]:  # Si no se evaluara la ultima hoja
                    if not(queue[nivel][2]):                # Si no se tiene un valor
                        queue[nivel][2] = valor_tablero        # asigno el valor del tablero
                        queue[nivel][5] = queue[nivel-1][1]-1  # asigno el indice del tablero
                    else:                                      # Si se tiene un valor previo
                        if jugador:        # Maximizar         # Si tiro la maquina jugador es verdadero
                            if valor_tablero > queue[nivel][2]:# Si el tablero es mayor que el valor almacenado 
                                queue[nivel][2] = valor_tablero  # Se actualiza el valor
                                queue[nivel][5] = queue[nivel-1][1]-1# Se actualiza el indice
                        else:              # Minimizar      # Si tiro el adverzario
                            if valor_tablero < queue[nivel][2]: #Si el tablero es menor que el almacenado actualiza
                                queue[nivel][2] = valor_tablero# Actuliza tablero
                                queue[nivel][5] = queue[nivel-1][1]-1#actualiza indice
                    nivel -= 1                             #retorna un nivel  se avansa a la siguiente iteracion
                    jugador = not(jugador)
                    self.mundo.establecer_entorno(copy.deepcopy(queue[nivel][0]))
                else:                                          # si se evaluara la ultima hoja
                    if jugador:        # Minimiza             # Si tiro la maquina jugador es verdadero pero se almacenara en el nivel anterior por lo tanto se minimiza 
                        if valor_tablero > queue[nivel][2]:    # Si elvalor del tablero es mayor que el almacenado
                            if not(queue[nivel-1][2]) or queue[nivel-1][2]>valor_tablero: #Si el nivel anterior no tiene valor o el valor del tablero es menor al guardado 
                                queue[nivel-1][2] = valor_tablero      # Actualiza  valor del nivel anterior
                                queue[nivel-1][5] = queue[nivel-2][1]-1  # Actualiza indice del nivel anterior                
                        else:
                            if not(queue[nivel-1][2]) or queue[nivel-1][2]>queue[nivel][2]: #Si el nivel anterior no tiene valor o el valor guardado es menor del tablero  
                                queue[nivel-1][2] = queue[nivel][2]            # Actualiza  valor del nivel anterior
                                queue[nivel-1][5] = queue[nivel-2][1] -1         # Actualiza indice del nivel anterior
                        if nivel - 2 >=0:
                            nivel -= 2
                            queue[nivel+1][1] = 0
                            self.mundo.establecer_entorno(copy.deepcopy(queue[nivel][0]))
                            self.actualizar = True
                            queue.pop()
                    else:    # Maximizar  
                        if valor_tablero < queue[nivel][2]:                     # Si elvalor del tablero es mayor que el almacenado
                            if not(queue[nivel-1][2]) or queue[nivel-1][2]<valor_tablero:
                                queue[nivel-1][2] = valor_tablero
                                queue[nivel-1][5] = queue[nivel-2][1]-1
                        else:
                            if not(queue[nivel-1][2]) or queue[nivel-1][2]<queue[nivel][2]:
                                queue[nivel-1][2] = queue[nivel][2]
                                queue[nivel-1][5] = queue[nivel-2][1]-1
                        if nivel - 2 >=0:
                            nivel -= 2
                            queue[nivel+1][1] = 0
                            self.mundo.establecer_entorno(copy.deepcopy(queue[nivel][0]))
                            self.actualizar = True
                            queue.pop()
        print(queue[0][5])
        return queue[1][3][queue[1][5]]
                
    def optener_valores(self):
        estado = [copy.deepcopy(self.mundo.obtener_entorno()),   #0 Tablero
                  0,                              #1 Indice
                  False,                          #2 Valor  
                  self.mundo.tiradas,             #3 Tiradas disponibles
                  sum(self.mundo.mov_disponibles),#4 Numero de movimientos disponibles
                  False]                          #5 mejor movimiento
        return estado
                    
    def funcion_de_evaluacion(self):
        acomulador = 0
        for fila in range(self.mundo.FILAS):
            for columna in range(self.mundo.COLUMNAS-3):
                temp = np.array(copy.deepcopy(self.mundo.tablero[fila,columna:columna+4]))
                acomulador += (np.sum(temp)/2)*min(temp)-(np.sum(abs(temp-2))/2)*min(abs(temp-2))
                if np.sum(temp) == 0:
                    return 0

        
        valor_tablero = acomulador
        acomulador = 0
        for columna in range(self.mundo.COLUMNAS):
            for fila in range(self.mundo.FILAS-3):
                temp = np.array(copy.deepcopy(self.mundo.tablero[fila:fila+4,columna]))
                acomulador += (np.sum(temp)/2)*min(temp)-(np.sum(abs(temp-2))/2)*min(abs(temp-2))
                if np.sum(temp) == 0:
                    return 0
        
        valor_tablero = acomulador
        t = copy.deepcopy(self.mundo.tablero)
        acomulador = 0
        for fila in range(self.mundo.FILAS-3):
            for columna in range(self.mundo.COLUMNAS-3):
                temp = np.array(copy.deepcopy([t[fila,columna],t[fila+1,columna+1],t[fila+2,columna+2],t[fila+3,columna+3]]))
                acomulador += (np.sum(temp)/2)*min(temp)-(np.sum(abs(temp-2))/2)*min(abs(temp-2))  
                if np.sum(temp) == 0:
                    return 0
                
        valor_tablero = acomulador
        t = copy.deepcopy(self.mundo.tablero)
        acomulador = 0
        for fila in range(self.mundo.FILAS-3):
            for columna in range(3,self.mundo.COLUMNAS):
                temp = np.array(copy.deepcopy([t[fila,columna],t[fila+1,columna-1],t[fila+2,columna-2],t[fila+3,columna-3]]))
                acomulador += (np.sum(temp)/2)*min(temp)-(np.sum(abs(temp-2))/2)*min(abs(temp-2))   
                if np.sum(temp) == 0:
                    return 0
        valor_tablero = acomulador
        return valor_tablero
    
        
if __name__ == '__main__':
    conecta_4 = conecta_cuatro.conecta_cuatro()
    mnx = minimax(conecta_4,3)
    jugador = False
    while(conecta_4.juego_terminado()==1):
        if jugador == False:
            x = mnx.minmax(copy.deepcopy(conecta_4.obtener_entorno()))
            conecta_4.tirar(x,2)
        else:
            x = conecta_4.con_num(input('Tira jugador '+str(int(jugador)+1)+': '))
            conecta_4.tirar(x,0)
        print(conecta_4.tablero)
        jugador = not(jugador)
    print('gano jugador: ',conecta_4.juego_terminado())