import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import os
import copy

# =================================================================================================
#                           VARIABLES GLOBALES PARA LA PRIMERA Y SEGUNDA FASE
# =================================================================================================
matriz = None
esquinNor = stepping_stone = costoMin = modi = Vogel = False
maximizar = minimizar = False
iteraciones_primeraFase = []
variables_primeraFase = []
z_PrimeraFase = 0
iteraciones = []
matriz_original = None
oferta_original = None
demanda_original = None
matriz_final_global = None
iteraciones_segunda_fase = []
variables_segundaFase = []
z_segundaFase = 0


# =================================================================================================
#                                   transformar_para_maximizacion
# =================================================================================================
def transformar_para_maximizacion(matriz):
    max_val = max(
        int(matriz[i, j][0])
        for i in range(1, matriz.shape[0] - 1)
        for j in range(1, matriz.shape[1] - 1)
    )

    for i in range(1, matriz.shape[0] - 1):
        for j in range(1, matriz.shape[1] - 1):
            original_cost = int(matriz[i, j][0])
            transformed_cost = max_val - original_cost
            matriz[i, j][0] = transformed_cost

    return matriz

# =================================================================================================

#                             MÉTODOS PRIMERA FASE, SOLUCIÓN FACTIBLE

# =================================================================================================

# =================================================================================================
#                                         metodo_vogel
# =================================================================================================

def metodo_vogel(matriz):
    global iteraciones
    iteraciones = []
    variables = []
    z = 0

    iteracion_actual = copy.deepcopy(matriz)
    iteraciones.append(iteracion_actual)

    while True:
        # Cálculo de penalidades de filas
        row_penalties = []
        for i, row in enumerate(matriz[1:-1], start=1):
            costos_validos = [cell[0] for cell in row[1:-1] if cell and cell[1] is None and cell[2] != 'x' and cell[0] != 'M']
            if len(costos_validos) > 1:
                menor1, menor2 = np.partition(costos_validos, 1)[:2]
                row_penalties.append((menor2 - menor1, i))
            else:
                row_penalties.append((float('-inf'), i))

        # Cálculo de penalidades de columnas
        col_penalties = []
        for j in range(1, len(matriz[0]) - 1):
            col = [matriz[i][j] for i in range(1, len(matriz) - 1) if matriz[i][j] and matriz[i][j][1] is None and matriz[i][j][2] != 'x' and matriz[i][j][0] != 'M']
            costos_validos = [cell [0] for cell in col if cell]
            if len(costos_validos) > 1:
                menor1, menor2 = np.partition(costos_validos, 1)[:2]
                col_penalties.append((menor2 - menor1, j))
            else:
                col_penalties.append((float('-inf'), j))

        # Selección de la penalidad máxima
        max_row_penalty, row_idx = max(row_penalties)
        max_col_penalty, col_idx = max(col_penalties)

        if max_row_penalty >= max_col_penalty:
            row = matriz[row_idx][1:-1]
            sin_asignacion = [idx for idx, cell in enumerate(row, start=1) if cell and cell[1] is None and cell[2] != 'x' and cell[0] != 'M']
            if not sin_asignacion:
                break
            min_val_cell_idx = min(sin_asignacion, key=lambda x: row[x-1][0])
            i, j = row_idx, min_val_cell_idx
        else:
            col = [matriz[i][col_idx] for i in range(1, len(matriz) - 1)]
            sin_asignacion = [idx for idx, cell in enumerate(col, start=1) if cell and cell[1] is None and cell[2] != 'x' and cell[0] != 'M']
            if not sin_asignacion:
                break
            min_val_cell_idx = min(sin_asignacion, key=lambda x: col[x-1][0])
            i, j = min_val_cell_idx, col_idx

        # Realizar la asignación
        oferta = matriz[i][-1]
        demanda = matriz[-1][j]
        asignacion = min(oferta, demanda)

        # Actualizar matriz con la asignación y ajustar oferta y demanda
        matriz[i][j][1] = asignacion
        matriz[i][-1] -= asignacion
        matriz[-1][j] -= asignacion
        z += matriz[i][j][0] * asignacion

        variables.append(f"x{i}{j}={asignacion}")

        if matriz[i][-1] == 0:
            for cell in matriz[i][1:-1]:
                if cell and cell[1] is None:
                    cell[2] = 'x'
        if matriz[-1][j] == 0:
            for k in range(1, len(matriz) - 1):
                cell = matriz[k][j]
                if cell and cell[1] is None:
                    cell[2] = 'x'

        iteracion_actual = copy.deepcopy(matriz)
        iteraciones.append(iteracion_actual)

        if all(cell and cell[1] is not None for row in matriz[1:-1] for cell in row[1:-1]):
            break

    for i in range(1, len(matriz) - 1):
        for j in range(1, len(matriz[0]) - 1):
            if matriz[i][j] and matriz[i][j][1] is None and matriz[i][j][2] != 'x' and matriz[i][j][0] != 'M':
                oferta = matriz[i][-1]
                demanda = matriz[-1][j]
                asignacion = min(oferta, demanda)

                matriz[i][j][1] = asignacion
                matriz[i][-1] -= asignacion
                matriz[-1][j] -= asignacion
                z += matriz[i][j][0] * asignacion

                variables.append(f"x{i}{j}={asignacion}")

                iteracion_actual = copy.deepcopy(matriz)
                iteraciones.append(iteracion_actual)

    variables = sorted(variables, key=lambda var: (int(var[1]), int(var[2])))
    return iteraciones, variables, z


# =================================================================================================
#                                      matriz_costo_minimo
# =================================================================================================
def matriz_costo_minimo(matriz):
    global iteraciones
    iteracion_actual = copy.deepcopy(matriz)
    iteraciones.append(iteracion_actual)
    variables = []
    demanda = matriz[-1, 1:-1].astype(int)
    oferta = matriz[1:-1, -1].astype(int)
    iteracion = matriz.copy()
    
    # Crear lista de celdas con sus costos, ordenadas de menor a mayor
    celdas_ordenadas = sorted(
        [(i, j, int(matriz[i, j][0])) for i in range(1, matriz.shape[0] - 1) 
         for j in range(1, matriz.shape[1] - 1) 
         if isinstance(matriz[i, j], list) and matriz[i, j][0] != 'M'],  # Ignorar celdas con 'M'
        key=lambda x: x[2]
    )
    
    while celdas_ordenadas:
        # Encontrar las celdas con el menor costo
        min_cost = celdas_ordenadas[0][2]
        min_cost_cells = [celda for celda in celdas_ordenadas if celda[2] == min_cost]

        # Si hay empate en el valor de costo, elegir la celda con mayor asignación posible
        if len(min_cost_cells) > 1:
            max_asignacion_celda = max(min_cost_cells, key=lambda x: min(oferta[x[0] - 1], demanda[x[1] - 1]))
            asignacion_posible = min(oferta[max_asignacion_celda[0] - 1], demanda[max_asignacion_celda[1] - 1])

            # En caso de empate en la asignación posible, priorizar de izquierda a derecha (por filas)
            max_asignacion_celdas = [celda for celda in min_cost_cells 
                                     if min(oferta[celda[0] - 1], demanda[celda[1] - 1]) == asignacion_posible]
            i, j, costo = min(max_asignacion_celdas, key=lambda x: (x[0], x[1]))  # Selección de izquierda a derecha
        else:
            i, j, costo = min_cost_cells[0]
            asignacion_posible = min(oferta[i - 1], demanda[j - 1])

        # Realizar la asignación
        asignacion = asignacion_posible
        
        # Actualizar la iteración en la celda con la asignación
        if isinstance(iteracion[i, j], list):
            iteracion[i, j][1] = asignacion
        else:
            iteracion[i, j] = [int(matriz[i, j][0]), asignacion, None]
        
        # Restar la asignación de la oferta y demanda
        oferta[i - 1] -= asignacion
        demanda[j - 1] -= asignacion
        
        # Actualizar la fila de demanda y la columna de oferta en la iteración
        iteracion[-1, j] = demanda[j - 1]
        iteracion[i, -1] = oferta[i - 1]
        
        # Registrar la variable de asignación
        variables.append(f"x{i}{j}={asignacion}") 
        
        # Guardar la iteración actual
        iteraciones.append(copy.deepcopy(iteracion))
        
        # Marcar la fila o columna con 'x' si la oferta o demanda queda en cero, eliminando celdas correspondientes
        if oferta[i - 1] == 0:
            celdas_ordenadas = [celda for celda in celdas_ordenadas if celda[0] != i]
        if demanda[j - 1] == 0:
            celdas_ordenadas = [celda for celda in celdas_ordenadas if celda[1] != j]
    
    # Calcular el valor de Z
    z = sum(
        int(iteracion[i, j][1]) * int(iteracion[i, j][0])
        for i in range(1, matriz.shape[0] - 1)
        for j in range(1, matriz.shape[1] - 1)
        if iteracion[i, j][1] is not None
    )
    
    # Ordenar las variables en orden de fila y columna variables = sorted(variables, key=lambda var: (int(var[1]), int(var[2])))
    return iteraciones, variables, z

# =================================================================================================
#                                        esquina_noroeste
# =================================================================================================

import copy

def esquina_noroeste(matriz):
    global iteraciones
    iteracion_actual = copy.deepcopy(matriz)
    iteraciones.append(iteracion_actual)
    variables = []
    demanda = matriz[-1, 1:-1].astype(int)
    oferta = matriz[1:-1, -1].astype(int)
    iteracion = matriz.copy()
    
    i, j = 1, 1  # Comienza en la esquina noroeste
    while i < matriz.shape[0] - 1 and j < matriz.shape[1] - 1:
        # Verificar que la celda actual no contenga 'M'
        if matriz[i, j][0] == 'M':
            j += 1  # Moverse a la derecha si hay 'M'
            continue  # Saltar a la siguiente iteración

        # Calcular el mínimo entre oferta y demanda
        minimo = min(oferta[i - 1], demanda[j - 1])
        
        # Asignar el valor mínimo a la matriz de iteraciones
        if isinstance(iteracion[i, j], list):
            iteracion[i, j][1] = minimo
        else:
            iteracion[i, j] = [int(matriz[i, j][0]), minimo, None]
        
        oferta[i - 1] -= minimo
        demanda[j - 1] -= minimo
        
        # Actualizar la matriz de iteraciones después de modificar oferta y demanda
        iteracion[-1, j] = demanda[j - 1]  # Actualizar la fila de demanda
        iteracion[i, -1] = oferta[i - 1]   # Actualizar la columna de oferta
        
        variables.append(f"x{i}{j}={minimo}")
        
        # Guardar la iteración actual
        iteraciones.append(copy.deepcopy(iteracion))  # Usa deepcopy para guardar una copia independiente
        
        # Decidir el movimiento
        if oferta[i - 1] == 0 and demanda[j - 1] == 0:
            i += 1
            j += 1
        elif oferta[i - 1] == 0:
            i += 1
        elif demanda[j - 1] == 0:
            j += 1
        else:
            j += 1  # Mover a la derecha si no hay restricciones

    # Calcular el valor de z
    z = sum(
        int(iteracion[i, j][1]) * int(iteracion[i, j][0])
        for i in range(1, matriz.shape[0] - 1)
        for j in range(1, matriz.shape[1] - 1)
        if iteracion[i, j][1] is not None
    )
   
    # Ordenar las variables en orden de fila y columna
    variables = sorted(variables, key=lambda var: (int(var[1]), int(var[2])))
    return iteraciones, variables, z



# =================================================================================================

#                            MÉTODOS SEGUNDA FASE, SOLUCIÓN ÓPTIMA

# =================================================================================================

#                                    Funciones solucion Modi


# =================================================================================================
#                                      contar_unidades
# =================================================================================================  
def contar_unidades():
    global matriz
    
    filas, columnas = len(matriz) - 2, len(matriz[0]) - 2  # Excluir encabezados y filas/columnas extra
    max_filas = -1
    max_columnas = -1
    max_filas_indice = -1
    max_columnas_indice = -1
    
    # Contar unidades en filas
    for i in range(1, filas + 1):
        conteo_fila = 0
        for j in range(1, columnas + 1):
            if isinstance(matriz[i][j], list):  
                if matriz[i][j][1] is not None:  # Si hay una unidad asignada
                    
                    conteo_fila += 1
        if conteo_fila > max_filas:
            max_filas = conteo_fila
            max_filas_indice = i

    # Contar unidades en columnas
    for j in range(1, columnas + 1):
        conteo_columna = 0
        for i in range(1, filas + 1):
            if isinstance(matriz[i][j], list):  
                if matriz[i][j][1] is not None:
                    conteo_columna += 1
        if conteo_columna > max_columnas:
            max_columnas = conteo_columna
            max_columnas_indice = j

    # Colocar un 0 en la fila o columna que tiene más unidades asignadas
    if max_filas >= max_columnas:
        return 'fila', max_filas_indice  # Indica que la fila será modificada
    else:
        return 'columna', max_columnas_indice  # Indica que la columna será modificada

# =================================================================================================
#                                      agregar_fila_columna
# =================================================================================================
def agregar_fila_columna():
    global matriz
    # Verificar la forma de la matriz antes de operar
    

    # Chequear que matriz tenga más de una dimensión
    if matriz.ndim < 2:
        raise ValueError("La matriz no tiene la forma correcta.")

    # Agrega la fila V(j) y la columna U(i)
    nueva_fila = np.array([None] * (matriz.shape[1]), dtype=object)
    nueva_fila[0] = "V(j)"
    matriz = np.vstack([matriz, nueva_fila])  # Añadir fila al final

    nueva_columna = np.array([None] * (matriz.shape[0]), dtype=object)
    nueva_columna[0] = "U(i)"
    matriz = np.hstack([matriz, nueva_columna.reshape(-1, 1)])  # Añadir columna

    # Verificar la forma después de la operación
    

    
# =================================================================================================
#                                        asignar_valor_0
# =================================================================================================
def asignar_valor_0(fila_o_columna, indice):
    global matriz
    if fila_o_columna == 'fila':
        # Asignar valores a la fila V(j)
        matriz[indice,-1] = 0
    else:
        # Asignar valores a la columna U(i)
        matriz[-1,indice] = 0

    
# =================================================================================================
#                                           calcular_u_v
# =================================================================================================
def calcular_u_v():
    global matriz
    filas, columnas = matriz.shape
    cambios = True  # Indicador de si ha habido algún cambio en la iteración

    # Seguimos calculando mientras haya cambios
    while cambios:
        cambios = False
        for i in range(1, filas - 2):  # Excluimos la fila de demanda y V(j)
            for j in range(1, columnas - 2):  # Excluimos la columna de oferta y U(i)
                if isinstance(matriz[i, j], list) and matriz[i, j][1] is not None:  # Si la celda está ocupada
                    if matriz[i, j][0] != 'M':  # Ignorar celdas con 'M'
                        # Calcular V(j) si U(i) ya está asignado y V(j) no lo está
                        if matriz[i, -1] is not None and matriz[-1, j] is None:
                            matriz[-1, j] = matriz[i, j][0] - matriz[i, -1]
                            cambios = True
                        # Calcular U(i) si V(j) ya está asignado y U(i) no lo está
                        elif matriz[i, -1] is None and matriz[-1, j] is not None:
                            matriz[i, -1] = matriz[i, j][0] - matriz[-1, j]
                            cambios = True

    return matriz

# =================================================================================================
#                                        calculo_costo_minimo
# =================================================================================================
def calculo_costo_minimo():
    global matriz
    filas, columnas = matriz.shape
    
    min_value = [None, 0, 0]  # costo, fila, columna
    for i in range(1, filas - 2):
        for j in range(1, columnas - 2):
            if isinstance(matriz[i, j], list) and matriz[i, j][1] is None:
                if matriz[i, j][0] != 'M':  # Ignorar celdas con 'M'
                    costo_op = matriz[i, j][0] - (matriz[i, -1] + matriz[-1, j])
                    if costo_op < 0 and min_value[0] is None:
                        min_value[0] = costo_op
                        min_value[1] = i
                        min_value[2] = j
                    elif costo_op < 0 and costo_op < min_value[0]:
                        min_value[0] = costo_op
                        min_value[1] = i
                        min_value[2] = j
    return min_value



# =================================================================================================
#                                  Solucion con Backtracking
# =================================================================================================
# =================================================================================================
#                                            Celda
# =================================================================================================
class Celda():
    def __init__(self, x, y, esRaiz, busqueda):
        self.x = x
        self.y = y
        self.raiz = esRaiz
        self.bus = busqueda
    
    def verificarRaiz(self, x, y):
        return self.x == x and self.y == y
    def __repr__(self):
        return f"Celda(x={self.x}, y={self.y}, raiz={self.raiz}, busqueda='{self.bus}')"

# =================================================================================================
#                                         buscar_ciclo
# =================================================================================================
def buscar_ciclo(celda, lista):
    global matriz
    global stepping_stone
    final = 1 if stepping_stone else 2
    
    filas, columnas = matriz.shape

    # Verificar si estamos de vuelta en la raíz (completamos un ciclo)
    if len(lista) > 1 and celda.verificarRaiz(lista[0].x, lista[0].y):
        return True

    if celda.bus == "fila":
        # Buscar en la fila actual
        for j in range(1, columnas - final):  # Excluyendo la columna de oferta
            if j != celda.y and isinstance(matriz[celda.x, j], list) and matriz[celda.x, j][1] is not None and matriz[celda.x, j][0] != 'M':
                nueva_celda = Celda(celda.x, j, False, "col")
                lista.append(nueva_celda)
                if buscar_ciclo(nueva_celda, lista):
                    return True
                lista.pop()  # Eliminar la última celda si no encontramos el ciclo
        return False

    else:
        # Buscar en la columna actual
        for i in range(1, filas - final):  # Excluyendo la fila de demanda
            if i != celda.x and isinstance(matriz[i, celda.y], list) and matriz[i, celda.y][1] is not None and matriz[i, celda.y][0] != 'M':
                nueva_celda = Celda(i, celda.y, False, "fila")
                lista.append(nueva_celda)
                if buscar_ciclo(nueva_celda, lista):
                    return True
                lista.pop()  # Eliminar la última celda si no encontramos el ciclo
        return False

# =================================================================================================
#                                         asignar_signos
# =================================================================================================
def asignar_signos(ciclo):
    
    global matriz  # Usamos la matriz global
    signo_actual = '+'  # Comenzamos con el signo '+'

    # Iterar sobre los elementos del ciclo
    for coordenada in ciclo:
        fila, columna = coordenada.x, coordenada.y

        # Asignar el signo actual a la sublista en la matriz
        if isinstance(matriz[fila, columna], list):
            matriz[fila, columna][2] = signo_actual  # Asignar el signo en la tercera posición de la sublista

        # Alternar el signo
        signo_actual = '-' if signo_actual == '+' else '+'

# =================================================================================================
#                                         aplicar_ciclo
# =================================================================================================
def aplicar_ciclo():
    global matriz
    global stepping_stone
    if stepping_stone:
        final = 1
    else:
        final = 2
    filas, columnas = matriz.shape
    min_value = encontrar_minimo_unidades()
    for i in range(1, filas - final):
        for j in range(1, columnas - final):
            if isinstance(matriz[i, j], list):
                
                if matriz[i,j][2] == '+':
                    matriz[i,j][1] += min_value
                elif matriz[i,j][2] == '-':
                    matriz[i,j][1] -= min_value
                    if matriz[i,j][1] == 0:
                        matriz[i,j][1] = None
                
                matriz[i,j][2] = None

# =================================================================================================
#                                   encontrar_minimo_unidades
# =================================================================================================
def encontrar_minimo_unidades():
    global matriz
    filas, columnas = matriz.shape
    valor_minimo = None  # Inicializar como None
    

    for fila in range(1, filas - 2):  # Excluyendo encabezados y fila de demanda
        for col in range(1, columnas - 2):  # Excluyendo columna de oferta
            # Verificar si la celda es una lista y si su signo es "-"
            if isinstance(matriz[fila, col], list) and matriz[fila, col][2] == '-':
                unidades = matriz[fila, col][1]  # Obtener el valor de unidades

                # Actualizar el valor mínimo si es necesario
                if valor_minimo is None or unidades < valor_minimo:
                    valor_minimo = unidades
                    

    return valor_minimo


# =================================================================================================
#                                        set_none_columns
# =================================================================================================
def set_none_columns():
    global matriz
    filas, columnas = matriz.shape
    # Establecer toda la columna U(i) en None
    for col in range(1, columnas - 2):
        matriz[-1,col] = None
    for fila in range(1, filas - 1): 
        matriz[fila,-1] = None
    


# =================================================================================================
#                                    Funciones Stepping Stone
# =================================================================================================
# =================================================================================================
#                                minimo_valor_red_celdas_desocupadas
# =================================================================================================
def minimo_valor_red_celdas_desocupadas():
    global matriz
    filas, columnas = matriz.shape
    valor_minimo = [None,None,None]  # Inicializar como None
    

    for fila in range(1, filas - 1):  # Excluyendo encabezados y fila de demanda
        for col in range(1, columnas - 1):  # Excluyendo columna de oferta
            # Verificar si la celda es una lista y si su signo es "-"
            if isinstance(matriz[fila, col], list) and matriz[fila, col][1] == None:
                valor_de_red = valor_cambio_red(fila,col)
                
                # Actualizar el valor mínimo si es necesario
                if valor_de_red < 0:
                    if valor_minimo[0] is None or valor_de_red < valor_minimo[0]:
                        valor_minimo[0] = valor_de_red
                        valor_minimo[1] = fila
                        valor_minimo[2] = col 

    return valor_minimo
# =================================================================================================
#                                       valor_cambio_red
# =================================================================================================
def valor_cambio_red(x, y):
    global matriz
    filas, columnas = matriz.shape
    matriz[x, y][1] = 0
    cel = Celda(x, y, True, "fila")
    lista = []
    lista.append(cel)
    buscar_ciclo(cel, lista)
    asignar_signos(lista)
    value = 0

    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            if isinstance(matriz[i, j], list):
                # Verificar que el primer elemento sea un número
                if matriz[i, j][2] == '+':
                    if isinstance(matriz[i, j][0], (int, float)):  # Asegúrate de que sea un número
                        value += matriz[i, j][0]
                    else:
                        print(f"Advertencia: valor no numérico en [{i}, {j}]: {matriz[i, j][0]}")
                elif matriz[i, j][2] == '-':
                    if isinstance(matriz[i, j][0], (int, float)):  # Asegúrate de que sea un número
                        value -= matriz[i, j][0]
                    else:
                        print(f"Advertencia: valor no numérico en [{i}, {j}]: {matriz[i, j][0]}")
                matriz[i, j][2] = None

    matriz[x, y][1] = None
    
    return value

# =================================================================================================
#                                     solucion_optima_MODI
# =================================================================================================
def solucion_optima_MODI():  
    
    global iteraciones_segunda_fase, matriz
    agregar_fila_columna()
    while True:
        degradacion()
        iteraciones_segunda_fase.append(copy.deepcopy(matriz.copy()))
        fila_o_columna, indice = contar_unidades()
        
        
        
        # Asignar los valores según la fila o columna modificada
        asignar_valor_0(fila_o_columna, indice)
        
        calcular_u_v()
        
        
        min_value = calculo_costo_minimo()  # Selecciona la celda con el costo mínimo
        
        if min_value[0] == None:
            break
        matriz[min_value[1],min_value[2]][1] = 0
        cel = Celda(min_value[1],min_value[2],True,"fila")
        lista = [cel]
        buscar_ciclo(cel, lista)
        asignar_signos(lista)

        aplicar_ciclo()                # Aplica las actualizaciones de unidades
       
        set_none_columns()

    set_none_columns()
    calcular_Variables_Z()

# =================================================================================================
#                                     solucion_stepping_stone
# =================================================================================================
def solucion_stepping_stone():
    global iteraciones_segunda_fase
    while True:
        degradacion()
        iteraciones_segunda_fase.append(copy.deepcopy(matriz.copy()))
        min_value = minimo_valor_red_celdas_desocupadas()
        
        if min_value[0] == None:
            break
        matriz[min_value[1],min_value[2]][1] = 0
        cel = Celda(min_value[1],min_value[2],True,"fila")
        lista = [cel]
        buscar_ciclo(cel, lista)
        asignar_signos(lista)
        aplicar_ciclo()                # Aplica las actualizaciones de unidades
    calcular_Variables_Z()


# =================================================================================================
#                                     calcular_Variables_Z
# =================================================================================================    
def calcular_Variables_Z():
    global matriz, variables_segundaFase, z_segundaFase, matriz_original, maximizar
    filas, columnas = matriz.shape
    resultado = 0
    
    for i in range(1, filas - 1):
        for j in range(1, columnas - 1):
            if isinstance(matriz[i, j], list) and matriz[i, j][1] is not None:
                variables_segundaFase = sorted(variables_segundaFase, key=lambda var: (int(var[1]), int(var[2])))
                variables_segundaFase.append(f"x{i}{j}={matriz[i, j][1]}")
                
                # Si es maximización, usamos los valores de la matriz_original
                if maximizar:
                    valor_original = matriz_original[i, j][0]  # Obtener el valor de la matriz original en la misma posición
                    resultado += valor_original * matriz[i, j][1]  # Calcular z usando el valor original y la asignación
                else:
                    resultado += matriz[i, j][0] * matriz[i, j][1]  # Calcular z normalmente

    z_segundaFase = resultado


def print_Iteraciones():
    global iteraciones_segunda_fase

    for iteracion in iteraciones_segunda_fase:
        col_widths = []
        for col in range(iteracion.shape[1]):
            max_width = max(len(str(iteracion[row][col])) for row in range(iteracion.shape[0]))
            col_widths.append(max_width)
        # Imprimir la matriz formateada
        for row in iteracion:
            formatted_row = ""
            for i, item in enumerate(row):
                # Formatear cada celda y alinear a la izquierda
                formatted_row += str(item).ljust(col_widths[i] + 2)
            print(formatted_row)
    

# =================================================================================================
#                                          degradacion
# =================================================================================================   

def degradacion():
    global matriz
    global stepping_stone
    final = 2
    if stepping_stone:
        final = 1
    
    filas, columnas = matriz.shape
    lista_menores = []

    # Determina la cantidad de variables necesarias para una solución factible
    if stepping_stone:
        required_variables = (filas - 2) + (columnas - 2) - 1
    else:
        required_variables = (filas - 3) + (columnas - 3) - 1
    
    while True:
        contador_varaibles = 0
        lista_menores = []

        # Recuenta las variables asignadas y recolecta las celdas sin asignar (costo más bajo)
        for i in range(1, filas - final):
            for j in range(1, columnas - final):
                if isinstance(matriz[i, j], list) and matriz[i, j][1] != None:
                    contador_varaibles += 1
                elif isinstance(matriz[i, j], list) and matriz[i, j][1] == None:
                    lista_menores.append([matriz[i, j][0]] + [i, j])

        # Condición de salida: si ya se ha alcanzado el número requerido de variables
        if contador_varaibles == required_variables:
            break
        
       
        lista_ordenada = sorted(lista_menores, key=lambda x: x[0])
        
        
        for ele in lista_ordenada:
            matriz[ele[1], ele[2]][1] = 0  
            cel = Celda(ele[1], ele[2], True, "fila")
            lista = [cel]
            buscar_ciclo(cel, lista)  
            
            if len(lista) == 1:
                
                break
            else:
               
                matriz[ele[1], ele[2]][1] = None

        


# ==============================================================================================

#                    FUNCIONES PARA MOSTRAR LAS ITERACIONES Y RESULTADOS 

# ==============================================================================================


# =================================================================================================
#                                     mostrar_iteracion
# =================================================================================================
def mostrar_iteracion(iteracion_index):
    global iteraciones_primeraFase
    if iteracion_index >= len(iteraciones_primeraFase):
        mostrar_resultados()
        return
    
    iteracion = iteraciones_primeraFase[iteracion_index]
    
    ventana_iteracion = tk.Toplevel(ventana)
    ventana_iteracion.title(f"Iteración {iteracion_index}")
    ventana_iteracion.config(bg="black")
    ventana_iteracion.geometry("800x400")

    filas, columnas = iteracion.shape

    # Crear tabla en la interfaz
    frame_tabla = tk.Frame(ventana_iteracion)
    frame_tabla.pack(pady=10)

    for i in range(filas):
        for j in range(columnas):
            # Configurar el valor a mostrar en la celda
            if isinstance(iteracion[i, j], list):
                valor = str(iteracion[i, j][0]) if iteracion[i, j][1] is None else f"{iteracion[i, j][0]}({iteracion[i, j][1]})"
            else:
                valor = str(iteracion[i, j])

            # Crear entrada de tabla
            entry = tk.Entry(frame_tabla, width=10, justify='center', font=("Arial Black", 10))

            # Configuración de colores y permisos de edición según posición
            if i == 0 or j == 0:  # Encabezados en gris
                entry.insert(0, valor)
                entry.config(state="readonly", bg="#BDBDBD", fg="black")
            elif i == filas - 1 and j == columnas - 1:  # Última celda como None
                entry.insert(0, "None")
                entry.config(state="readonly", bg="#E0E0E0")
            elif i == filas - 1 or j == columnas - 1:  # Demanda y oferta en azul claro
                entry.insert(0, valor)
                entry.config(bg="#AED6F1")
            else:  # Celdas de entrada en verde claro
                entry.insert(0, valor)
                entry.config(bg="#D5F5E3")

            entry.grid(row=i, column=j, padx=1, pady=1)

    # Botón para continuar a la siguiente iteración
    btn_continuar = tk.Button(
        ventana_iteracion, text="Continuar", font=("Georgia", 10, "bold"), bg="#5DADE2", fg="white",
        command=lambda: (ventana_iteracion.destroy(), mostrar_iteracion(iteracion_index + 1))
    )
    btn_continuar.pack(pady=10)
# =================================================================================================
#                                     mostrar_iteracion_optima
# =================================================================================================
def mostrar_iteracion_optima(iteracion_index):
    global iteraciones_segunda_fase
    if iteracion_index >= len(iteraciones_segunda_fase):
        mostrar_resultados_optimos()
        return
    
    iteracion = iteraciones_segunda_fase[iteracion_index]
    
    ventana_iteracion_optima = tk.Toplevel(ventana)
    ventana_iteracion_optima.title(f"Iteración {iteracion_index}")
    ventana_iteracion_optima.config(bg="black")
    ventana_iteracion_optima.geometry("800x400")

    filas, columnas = iteracion.shape

    # Crear tabla en la interfaz
    frame_tabla = tk.Frame(ventana_iteracion_optima)
    frame_tabla.pack(pady=10)

    for i in range(filas):
        for j in range(columnas):
            # Configurar el valor a mostrar en la celda
            if isinstance(iteracion[i, j], list):
                valor = str(iteracion[i, j][0]) if iteracion[i, j][1] is None else f"{iteracion[i, j][0]}({iteracion[i, j][1]})"
            else:
                valor = str(iteracion[i, j])

            # Crear entrada de tabla
            entry = tk.Entry(frame_tabla, width=10, justify='center', font=("Arial Black", 10))

            # Configuración de colores y permisos de edición según posición
            if i == 0 or j == 0:  # Encabezados en gris
                entry.insert(0, valor)
                entry.config(state="readonly", bg="#BDBDBD", fg="black")
            elif i == filas - 1 and j == columnas - 1:  # Última celda como None
                entry.insert(0, "None")
                entry.config(state="readonly", bg="#E0E0E0")
            elif i == filas - 1 or j == columnas - 1:  # Demanda y oferta en azul claro
                entry.insert(0, valor)
                entry.config(bg="#AED6F1")
            else:  # Celdas de entrada en verde claro
                entry.insert(0, valor)
                entry.config(bg="#D5F5E3")

            entry.grid(row=i, column=j, padx=1, pady=1)

    # Botón para continuar a la siguiente iteración
    btn_continuar = tk.Button(
        ventana_iteracion_optima, text="Continuar", font=("Georgia", 10, "bold"), bg="#5DADE2", fg="white",
        command=lambda: (ventana_iteracion_optima.destroy(), mostrar_iteracion_optima(iteracion_index + 1))
    )
    btn_continuar.pack(pady=10)



# =================================================================================================
#                                    mostrar_resultados
# =================================================================================================
def mostrar_resultados():
    global matriz, oferta_original, demanda_original, iteraciones_primeraFase
    global matriz_final_global  
    global stepping_stone, modi

    # Obtener la última iteración
    ultima_iteracion = iteraciones_primeraFase[-1]

    # Crear una nueva matriz para mostrar la última iteración
    matriz_final = copy.deepcopy(ultima_iteracion)

    # Restaurar los valores originales de oferta y demanda
    filas, columnas = matriz_final.shape
    for j in range(1, columnas - 1):  # Fila de demanda
        matriz_final[filas - 1, j] = demanda_original[j - 1]
    for i in range(1, filas - 1):  # Columna de oferta
        matriz_final[i, columnas - 1] = oferta_original[i - 1]

    # Guardar la matriz final en la variable global
    matriz_final_global = matriz_final
    print("Matriz final", matriz_final_global)

    # Crear una ventana para mostrar resultados
    ventana_resultado = tk.Toplevel(ventana)
    ventana_resultado.title("Resultados de la Primera Fase")
    ventana_resultado.config(bg="black")
    ventana_resultado.geometry("600x400")

    # Mostrar variables
    tk.Label(ventana_resultado, text="\nVariables:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(pady=5)
    for var in variables_primeraFase:
        tk.Label(ventana_resultado, text=var, font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack()

    

    tk.Label(ventana_resultado, text=f"\nValor de Z: {z_PrimeraFase}", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(pady=10)

    # Crear un botón para continuar a la siguiente fase
    btn_continuar = tk.Button(
        ventana_resultado, text="Continuar a la Segunda Fase", font=("Georgia", 10, "bold"), bg="#5DADE2", fg="white",
        command=lambda: (ventana_resultado.destroy(), continuar_a_segunda_fase())
    )
    btn_continuar.pack(pady=10)


# =================================================================================================
#                                   continuar_a_segunda_fase
# =================================================================================================
def continuar_a_segunda_fase():
    global matriz_final_global
    global matriz_original
    matriz = transformar_matriz(matriz_final_global)
    print("\nmatriz transformada", matriz)
    matriz_original = transformar_matriz(matriz_original)
    print("\nmatriz original", matriz_original)
    if stepping_stone:
        print("steppin", stepping_stone)
        solucion_stepping_stone()
        print("entró steppin")
        print_Iteraciones()
        mostrar_iteracion_optima(0)
    elif modi:
        solucion_optima_MODI()
        print_Iteraciones()
        mostrar_iteracion_optima(0)
      
    
# =================================================================================================
#                                  mostrar_resultados_optimos
# =================================================================================================
def mostrar_resultados_optimos():
    global matriz, oferta_original, demanda_original, iteraciones_primeraFase
    global matriz_final_global  
    global stepping_stone, modi

    # Obtener la última iteración
    ultima_iteracion = iteraciones_segunda_fase[-1]

    # Crear una nueva matriz para mostrar la última iteración
    matriz_final = copy.deepcopy(ultima_iteracion)

    # Restaurar los valores originales de oferta y demanda
    filas, columnas = matriz_final.shape
    
    # Si se está utilizando el método MODI
    if modi:
        for j in range(1, len(demanda_original) + 1):  # Solo hasta el tamaño de demanda_original
            matriz_final[filas - 2, j] = demanda_original[j - 1]  # Fila de demanda (sin contar la fila adicional V(j))
        
        for i in range(1, len(oferta_original) + 1):  # Solo hasta el tamaño de oferta_original
            matriz_final[i, columnas - 2] = oferta_original[i - 1]  # Columna de oferta (sin contar la columna adicional U(i))

    else:  # Si se está utilizando el método Stepping Stone
        for j in range(1, columnas - 1):  # Fila de demanda
            matriz_final[filas - 1, j] = demanda_original[j - 1]
        for i in range(1, filas - 1):  # Columna de oferta
            matriz_final[i, columnas - 1] = oferta_original[i - 1]

    # Guardar la matriz final en la variable global
    matriz_final_global = matriz_final
    print("Matriz final", matriz_final_global)

    # Crear una ventana para mostrar resultados
    ventana_resultado = tk.Toplevel(ventana)
    ventana_resultado.title("Resultados de la Segunda Fase")
    ventana_resultado.config(bg="black")
    ventana_resultado.geometry("600x400")
    # Mostrar variables
    tk.Label(ventana_resultado, text="\nVariables:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(pady=5)
    for var in variables_segundaFase:
        tk.Label(ventana_resultado, text=var, font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack()

    # Mostrar el valor de Z
    tk.Label(ventana_resultado, text=f"\nValor de Z: {z_segundaFase}", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(pady=10)

    # Botón para regresar a la ventana principal
    btn_regresar = tk.Button(ventana_resultado, text="Regresar", command=lambda: [limpiar_variables(), ventana.deiconify(), ventana_resultado.destroy()], font=("Georgia", 12), bg="#D3BFA7", fg="black")
    btn_regresar.pack(pady=20)
 
# =================================================================================================
# =================================================================================================
#                                     limpiar_variables
# =================================================================================================
def limpiar_variables():
    global matriz, esquinNor, stepping_stone, costoMin, modi, Vogel
    global maximizar, minimizar, iteraciones_primeraFase, variables_primeraFase
    global z_PrimeraFase, iteraciones, matriz_original, oferta_original
    global demanda_original, matriz_final_global, iteraciones_segunda_fase
    global variables_segundaFase, z_segundaFase

    # Reiniciar todas las variables globales
    matriz = None
    esquinNor = stepping_stone = costoMin = modi = Vogel = False
    maximizar = minimizar = False
    iteraciones_primeraFase = []
    variables_primeraFase = []
    z_PrimeraFase = 0
    iteraciones = []
    matriz_original = None
    oferta_original = None
    demanda_original = None
    matriz_final_global = None
    iteraciones_segunda_fase = []
    variables_segundaFase = []
    z_segundaFase = 0


        
# =================================================================================================
#                                      transformar_matriz
# =================================================================================================  
def transformar_matriz(matriz):
    filas, columnas = matriz.shape
    nueva_matriz = np.empty((filas, columnas), dtype=object)

    for i in range(filas):
        for j in range(columnas):
            valor = matriz[i, j]

            # Verifica si el valor es una lista
            if isinstance(valor, list):
                # Si el primer elemento es 'M', asigna None o un valor apropiado
                if valor[0] == 'M':
                    nueva_matriz[i, j] = [None, None, None]  # O cualquier otra forma de manejarlo
                else:
                    # Convierte el valor a int si es posible
                    nueva_matriz[i, j] = [int(valor[0]), valor[1], valor[2]] if valor[0] is not None else [None, None, None]
            else:
                # Manejar valores que no son listas (por ejemplo, encabezados)
                nueva_matriz[i, j] = valor

    return nueva_matriz
    
    
# ===============================================================================================
# =================================================================================================
#                                      desbalance_solFactible
# =================================================================================================  
def desbalance_solFactible():
    global matriz
    global oferta_original, demanda_original
    
    # Calcular la suma de las ofertas y demandas
    suma_oferta = matriz[1:-1, -1].sum()
    suma_demandas = matriz[-1, 1:-1].sum()
    
    # Verificar si hay desbalance
    if suma_oferta < suma_demandas:
        # Caso: Oferta < Demanda
        # Agregar una fila adicional justo encima de la fila de demanda
        nueva_fila = ['F' + str(matriz.shape[0] - 1)]  # Nombre de la nueva fila
        nueva_fila += [[0, None, None]] * (matriz.shape[1] - 2)  # Ceros y None
        nueva_fila.append(suma_demandas - suma_oferta)  # Valor de la oferta que falta
        nueva_fila = np.array(nueva_fila, dtype=object) 
        
        # Insertar la nueva fila en la posición correcta
        matriz = np.insert(matriz, matriz.shape[0] - 1, nueva_fila, axis=0)
        print(f"Agregada nueva fila para balancear: {nueva_fila}")

    elif suma_oferta > suma_demandas:
        # Caso: Oferta > Demanda
        # Agregar una columna adicional
        nueva_columna = [0]  # Cero en la primera posición
        for i in range(1, matriz.shape[0] - 1):
            nueva_columna.append([0, None, None])  # 0 en la primera posición y None en las demás
        nueva_columna.append(suma_oferta - suma_demandas)  # Valor de la demanda que falta
        nueva_columna = np.array(nueva_columna, dtype=object) 
        
        # Insertar la nueva columna en la posición correcta
        matriz = np.insert(matriz, matriz.shape[1] - 1, nueva_columna, axis=1)

        # Actualizar encabezados de la columna
        num_columnas = matriz.shape[1] - 2  # Número de columnas sin la columna de oferta
        matriz[0, num_columnas] = f'W{num_columnas}'  # Asignar encabezado W con el número correspondiente
        matriz[0, -1] = 'Oferta'  # Encabezado de la columna de oferta
        
        print(f"Agregada nueva columna para balancear: {nueva_columna}")

    # Copiar los valores originales de oferta y demanda
    oferta_original = matriz[1:-1, -1].copy()  # Copia de la columna de oferta
    print("OFERTA ORIGINAL", oferta_original)
    demanda_original = matriz[-1, 1:-1].copy()  # Copia de la fila de demanda
    print("DEMANDA ORIGINAL", demanda_original)

    


# =================================================================================================

#                                            INTERFAZ

# =================================================================================================

# =================================================================================================
#                                            resolver
# =================================================================================================
def resolver():
    global matriz, esquinNor, stepping_stone, costoMin, modi, Vogel, maximizar, minimizar
    global iteraciones_primeraFase, variables_primeraFase, z_PrimeraFase
    global matriz_original
    global oferta_original, demanda_original
    
    if matriz is None:
        messagebox.showerror("Error", "Primero debe crear la tabla.")
        return
    opcion1 = opcion_maximizar.get()
    maximizar = opcion1 in ["Maximizar"]  
    opcion = opcion_metodo.get()
    esquinNor = opcion in ["Esquina noroeste y Modi", "Esquina noroeste y Stepping Stone"]
    costoMin = opcion in ["Matriz de costo mínimo y Modi", "Matriz de costo mínimo y Stepping Stone"]
    Vogel = opcion in ["Vogel y Modi", "Vogel y Stepping Stone"]  
    opcion2 = opcion_metodo.get()
    stepping_stone = opcion2 in ["Vogel y Stepping Stone", "Esquina noroeste y Stepping Stone", "Matriz de costo mínimo y Stepping Stone"]
    modi = opcion2 in ["Esquina noroeste y Modi", "Matriz de costo mínimo y Modi", "Vogel y Modi"]

    # Leer los datos de la tabla sin formatearla como texto
    for i in range(1, matriz.shape[0] - 1):
        for j in range(1, matriz.shape[1] - 1):
            valor = frame_tabla.grid_slaves(row=i, column=j)[0].get()
            if valor == "M":
                matriz[i, j] = ["M", None, None]  # Mantener "M" en la matriz
            elif valor.isdigit():
                matriz[i, j] = [int(valor), None, None]  # Convertir a entero
            else:
                matriz[i, j] = [0, None, None]  # Otras entradas se convierten a 0

        oferta = frame_tabla.grid_slaves(row=i, column=matriz.shape[1] - 1)[0].get()
        matriz[i, -1] = int(oferta) if oferta.isdigit() else 0

    for j in range(1, matriz.shape[1] - 1):
        demanda = frame_tabla.grid_slaves(row=matriz.shape[0] - 1, column=j)[0].get()
        matriz[-1, j] = int(demanda) if demanda.isdigit() else 0

    desbalance_solFactible()
    matriz_original = copy.deepcopy(matriz)  
    print("matriz_original", matriz_original)
    
    # Guardar los valores originales de oferta y demanda
    oferta_original = matriz[1:-1, -1].copy()  # Copia de la columna de oferta
    print("OFERTA ORIGINAL", oferta_original)
    demanda_original = matriz[-1, 1:-1].copy()  # Copia de la fila de demanda
    print("DEMANDA ORIGINAL", demanda_original)

    if maximizar:
        matriz = transformar_para_maximizacion(matriz)

    if esquinNor:
        iteraciones_primeraFase, variables_primeraFase, z_PrimeraFase = esquina_noroeste(matriz)
        mostrar_iteracion(0)      
    elif costoMin:
        iteraciones_primeraFase, variables_primeraFase, z_PrimeraFase = matriz_costo_minimo(matriz)
        mostrar_iteracion(0)
    else:
        iteraciones_primeraFase, variables_primeraFase, z_PrimeraFase = metodo_vogel(matriz)
        mostrar_iteracion(0)
        
    # Ocultar ventana actual
    ventana.withdraw()


# =================================================================================================
#                                        validar_entrada
# =================================================================================================
# Función para validar entradas (permite valores vacíos para borrar)
def validar_entrada(texto):
    return texto == "" or (texto.isdigit() and int(texto) > 0)

# Función para crear la tabla
def crear_tabla():
    try:
        fuentes = int(entry_fuentes.get())
        destinos = int(entry_destinos.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores válidos.")
        return

    global matriz
    matriz = np.empty((fuentes + 2, destinos + 2), dtype=object)
    for i in range(1, fuentes + 1):
        matriz[i, 0] = f"F{i}"
    matriz[0, 1:destinos + 1] = [f"W{j}" for j in range(1, destinos + 1)]
    matriz[fuentes + 1, 0] = "Demanda"
    matriz[0, destinos + 1] = "Oferta"

    for i in range(1, fuentes + 1):
        for j in range(1, destinos + 1):
            matriz[i, j] = [0, None, None]
        matriz[i, destinos + 1] = 0

    matriz[fuentes + 1, 1:destinos + 1] = [0] * destinos
    matriz[fuentes + 1, destinos + 1] = None

    for widget in frame_tabla.winfo_children():
        widget.destroy()

    for i in range(fuentes + 2):
        for j in range(destinos + 2):
            valor = str(matriz[i, j][0]) if isinstance(matriz[i, j], list) else str(matriz[i, j])
            entry = tk.Entry(frame_tabla, width=10, justify='center', font=("Arial Black", 10))

            if i == 0 or j == 0:
                entry.insert(0, valor)
                entry.config(state="readonly", bg="#BDBDBD", fg="black")  
            elif i == fuentes + 1 and j == destinos + 1:
                entry.insert(0, "None")
                entry.config(state="readonly", bg="#E0E0E0")
            elif i == fuentes + 1 or j == destinos + 1:
                entry.insert(0, valor)
                entry.config(bg="#AED6F1")
            else:
                entry.insert(0, valor)
                entry.config(bg="#D5F5E3")

            entry.grid(row=i, column=j, padx=1, pady=1)

# =================================================================================================
#                                        limpiar_tabla
# =================================================================================================
# Función para limpiar la tabla
def limpiar_tabla():
    entry_fuentes.delete(0, tk.END)
    entry_destinos.delete(0, tk.END)
    for widget in frame_tabla.winfo_children():
        widget.destroy()


# =================================================================================================

#                                      INTERFAZ, VENTANA PRINCIPAL

# =================================================================================================   
 
    
    

# Configuración de ventana principal
ventana = tk.Tk()
ventana.title("Transporte")
ventana.geometry("900x700")
ventana.config(bg="black")



# Título centrado
tk.Label(ventana, text="Bienvenido al solucionador de problemas de transporte", 
         font=("Georgia", 15, "bold"), fg="#D3BFA7", bg="black").pack(pady=20)

# Ruta de la imagen
image_path = os.path.join("images", "mapa2.png")
# Mostrar la imagen en la ventana principal
try:
    img = Image.open(image_path)  # Abrir la imagen
    img = img.resize((150, 150))  # Redimensionar la imagen 
    img_tk = ImageTk.PhotoImage(img)  # Convertir a formato compatible con Tkinter
    img_label = tk.Label(ventana, image=img_tk, bg="black")
    img_label.pack(pady=5)
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# Frame para entradas y botones
frame_entrada = tk.Frame(ventana, bg="black")
frame_entrada.pack(pady=20)

# Campos de entrada y etiquetas
tk.Label(frame_entrada, text="Ingrese el número de fuentes:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").grid(row=0, column=0)
entry_fuentes = tk.Entry(frame_entrada, validate="key", font=("Georgia", 12, "bold"), width=10) 
entry_fuentes['validatecommand'] = (ventana.register(validar_entrada), '%P')
entry_fuentes.grid(row=0, column=1)

tk.Label(frame_entrada, text="Ingrese el número de destinos:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").grid(row=1, column=0)
entry_destinos = tk.Entry(frame_entrada, validate="key", font=("Georgia", 12, "bold"), width=10)  
entry_destinos['validatecommand'] = (ventana.register(validar_entrada), '%P')
entry_destinos.grid(row=1, column=1)

# Botones de Crear tabla y Limpiar
tk.Button(frame_entrada, text="Crear tabla", command=crear_tabla, font=("Georgia", 10, "bold"), bg="#5DADE2", fg="white").grid(row=0, column=2, padx=6, pady=9)
tk.Button(frame_entrada, text="Limpiar", command=limpiar_tabla, font=("Georgia", 10, "bold"), bg="#E74C3C", fg="white").grid(row=1, column=2, padx=5, pady=5)

# Frame para tabla
frame_tabla = tk.Frame(ventana, bg="black")
frame_tabla.pack()

# Opciones de método y maximización/minimización
frame_opciones = tk.Frame(ventana, bg="black")
frame_opciones.pack(pady=20)

tk.Label(frame_opciones, text="Seleccione el método:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(side="left")

# Crear estilo para el Combobox
style = ttk.Style()
style.configure("TCombobox", font=("Georgia", 12, "bold"))  

# Crear Combobox con estilo personalizado
opcion_metodo = ttk.Combobox(
    frame_opciones, 
    values=["Esquina noroeste y Modi", "Esquina noroeste y Stepping Stone", 
            "Matriz de costo mínimo y Modi", "Matriz de costo mínimo y Stepping Stone", 
            "Vogel y Modi", "Vogel y Stepping Stone"], 
    state="readonly", 
    style="TCombobox",
    width=30
)

opcion_metodo.pack(side="left")

tk.Label(frame_opciones, text="Optimización:", font=("Georgia", 12, "bold"), fg="#D3BFA7", bg="black").pack(side="left", padx=10)
opcion_maximizar = ttk.Combobox(frame_opciones, values=["Maximizar", "Minimizar"], state="readonly")
opcion_maximizar.current(0)
opcion_maximizar.pack(side="left")

# Botón de resolver
tk.Button(ventana, text="Resolver", command=resolver, font=("Georgia", 10, "bold"), bg="#58D68D", fg="white").pack(pady=10)

ventana.mainloop()