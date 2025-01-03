
# Librerías para la interfaz
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Librerías para manejar matrices
import numpy as np
import re


operaciones_historial = []
#Condicionales 

dos_fases = 0
fase_1 = 0
gran_M = 0
problema_lineal_infactible = 0
solucion_no_acotada = 0
min_problem = 0
debug = 0

count_restricciones = 1
count_artificales = 1
contador_x = 0  # Contador de variables originales x₁, x₂, ..., xₙ
contador_s_pos = 0  # Contador de variables de holgura positivas (+ sᵢ)
contador_s_neg = 0  # Contador de variables de holgura negativas (- sⱼ)
contador_artificiales = 0  # Contador de variables artificiales (+ aⱼ₊ₖ)
matrix = np.array(["BVS"], dtype=object)
list_rest = []
last_x_index = 0  # Definir aquí la variable como global

# Variables globales para las funciones de variables negativas con límite inferior
list_x = []  # Lista para guardar las variables con límite inferior
conLimite = 0  # Indicador de si hay alguna variable con límite inferior
reservaObjetivo = 0  # Constante almacenada tras simplificar la función objetivo
list_secundaria = []  # Lista para almacenar las restricciones que se van a transformar
rest_inicial = []
variables_sinLimite = []
restricciones_finales = []
# Variables globales para las funciones de variables negativas sin límite inferior
list_xSinLimite = []  # Lista para guardar las variables sin límite por reemplazar
sinLimite = 0  # Indicador de si hay alguna variable sin límite inferior
list_secundariaSL = []


#==================================================================================================================

#                                               FUNCIONES PARA CREAR MATRIX

#==================================================================================================================

def contar_variables(funcion_objetivo, restricciones):
    global contador_x 
    global contador_s_pos 
    global contador_s_neg 
    global contador_artificiales
    
   
    # Identificar variables originales en la función objetivo (patrón de la forma "x1", "x2", etc.)
    variables_objetivo = re.findall(r'x\d+', funcion_objetivo)
    contador_x = len(set(variables_objetivo))  # Contar las variables originales únicas

    # Procesar restricciones
    for restriccion in restricciones:
        # Identificar si es una desigualdad <=, >= o una igualdad =
        if '<=' in restriccion:
            contador_s_pos += 1  # Variable de holgura positiva (+ sᵢ)
        elif '>=' in restriccion:
            contador_s_neg += 1  # Variable de holgura negativa (- sⱼ)
            contador_artificiales += 1  # Variable artificial (+ aⱼ₊ₖ)
        elif '=' in restriccion:
            contador_artificiales += 1  # Variable artificial (+ aⱼ₊ₖ)


# Procesar ecuación y restricciones
def procesar_ecuacion(ecuacion):
    coeficientes = []
    
    lado_izquierdo, lado_derecho = ecuacion.split('=')
    patrones = re.findall(r'([+-]?\d*\.?\d*)\*x(\d+)', lado_izquierdo)
    for coeficiente, variable in patrones:
        if coeficiente == '' or coeficiente == '+':
            coeficiente = 1
        elif coeficiente == '-':
            coeficiente = -1
        else:
            coeficiente = float(coeficiente)
        coeficientes.append((coeficiente, 'x' + variable))
    
    s_variables = re.findall(r'(s\d+)', ecuacion)
    
    for s_var in s_variables:
        if 's' in ecuacion and 'a' in ecuacion:
            coeficientes.append((-1.0, s_var))
        else:
            coeficientes.append((1.0, s_var))

    a_variables = re.findall(r'(a\d+)', ecuacion)

    for a_var in a_variables:
        coeficientes.append((1.0, a_var))

    coeficientes.append((float(lado_derecho.strip()), 'RHS'))

    return coeficientes

def transformar_ecuacion(ecuacion):
    global count_restricciones, last_x_index,count_artificales
    global contador_x,contador_s_pos,contador_s_neg, min_problem
    ecuacion = ecuacion.replace(" ", "")
    
    if '<' in ecuacion:
       
        pos = ecuacion.find('<')
        
        # Ajustar para colocar la variable de holgura correctamente
        ecuacion = ecuacion[:pos] + f'+ 1*s{contador_x + count_restricciones} ' + ecuacion[pos:]  
        count_restricciones += 1
        
        ecuacion = ecuacion.replace("<", "")
    #print("Original:", ecuacion)
    elif '>' in ecuacion:
        
        pos = ecuacion.find('>')

        # Ajustar para colocar la variable de holgura correctamente
        count_t = contador_x + contador_s_pos  + contador_s_neg
        
        ecuacion = ecuacion[:pos] + f'- 1*s{contador_x + count_restricciones} ' + f'+ 1*a{count_t + count_artificales} ' + ecuacion[pos:]  
        count_restricciones += 1
        count_artificales  += 1
        
        ecuacion = ecuacion.replace(">", "")
    elif '=' in ecuacion and '<' not in ecuacion and '>' not in ecuacion and 'max' not  in ecuacion and 'min' not in ecuacion:
        pos = ecuacion.find('=')
        count_t = contador_x + contador_s_pos  + contador_s_neg 
        ecuacion = ecuacion[:pos] + f'+ 1*a{count_t + count_artificales} ' + ecuacion[pos:]
        count_artificales += 1
    # Verificar si es la función objetivo 'max' o 'min'
    if 'max' in ecuacion :
        
        # Eliminar "maxz" o "minz" del texto y aislar la parte de la ecuación
        ecuacion = ecuacion.replace("maxz", "").replace("minz", "")
        
        # Remover el signo '=' de la ecuación
        ecuacion = ecuacion.replace("=", "")
        
        # Cambiar los signos de los coeficientes
        nueva_ecuacion = ""
        i = 0
        # Manejar el primer término si comienza con un número directamente
        if ecuacion[i].isdigit() or ecuacion[i] == '-':
            # Si empieza con un número o con un signo negativo, invertir el signo
            if ecuacion[i] == '-':
                i += 1  # Saltar el signo negativo
            else:
                nueva_ecuacion += '-'  # Cambiar positivo a negativo

        # Recorrer el resto de la ecuación
        while i < len(ecuacion):
            # Manejar operadores consecutivos +- y -- correctamente
            if ecuacion[i:i+2] == '+-':  # Caso de +- que es un negativo
                nueva_ecuacion += '+'
                i += 2  # Saltar ambos símbolos
            elif ecuacion[i:i+2] == '--':  # Caso de -- que es un positivo
                nueva_ecuacion += '-'
                i += 2  # Saltar ambos símbolos
            elif ecuacion[i] == '+':
                nueva_ecuacion += '-'
                i += 1
            elif ecuacion[i] == '-':
                nueva_ecuacion += '+'
                i += 1
            else:
                nueva_ecuacion += ecuacion[i]
                i += 1
        
        # Finalmente, añadir "=0" para que sea compatible con el formato de Simplex
        ecuacion = "max z" + nueva_ecuacion + "=0"
        
    if 'min' in ecuacion:
        min_problem = 1

        # Eliminar "maxz" o "minz" del texto y aislar la parte de la ecuación
        ecuacion = ecuacion.replace("minz", "")
        
        # Remover el signo '=' de la ecuación
        ecuacion = ecuacion.replace("=", "")
          
        ecuacion = "max z" + ecuacion + "=0"
        
    #print("Transformada:", ecuacion)
    if debug:
            print("Ecuacion")
            print(ecuacion)
    return ecuacion


    

def transformar_inecuacion(inecuacion):
    # Expresión regular para capturar los coeficientes, variables, signo de la inecuación, y el lado derecho
    patron = r'([\d\.\+\-\*x\s]+)\s*(>=|<=|=)\s*(-?\d+\.?\d*)'
    
    coincidencia = re.match(patron, inecuacion.strip())
    
    if not coincidencia:
        return "Formato no válido"
    
    # Parte izquierda, operador y parte derecha de la inecuación
    izquierda = coincidencia.group(1).strip()


    izquierda = izquierda.replace(" ","")
    if "+-" in izquierda:
        print(izquierda)
        izquierda=izquierda.replace("+-","-")
    print("Ine")
    print(izquierda)

    operador = coincidencia.group(2)
    derecha = float(coincidencia.group(3))
    
    # Si el lado derecho ya es positivo, no se hace nada
    if derecha >= 0:
        return inecuacion
    
    # Si el lado derecho es negativo, multiplicamos cada término de la parte izquierda por -1
    izquierda_modificada = invertir_signos(izquierda)
    nueva_derecha = abs(derecha)
    
    # Cambiar el operador de la inecuación
    if operador == '>=':
        nuevo_operador = '<='
    elif operador == '<=':
        nuevo_operador = '>='
    else:
        nuevo_operador = '='
    
    # Construir la nueva inecuación
    nueva_inecuacion = f'{izquierda_modificada} {nuevo_operador} {nueva_derecha}'
    
    return nueva_inecuacion

def invertir_signos(izquierda):
    # Función para invertir los signos de todos los coeficientes en la parte izquierda
    i = 0
    nueva_izquierda = ""
    for termino in izquierda:
        if termino == '-' and i == 0:
            nueva_izquierda += ""
        
        elif termino.isdigit() and i == 0:
            c = "-" + termino
            nueva_izquierda += c
        
        elif termino == "-" and i != 0:
            nueva_izquierda += "+"

        elif termino == "+" and i != 0:
            nueva_izquierda += "-"
        else:
            nueva_izquierda += termino
        i += 1
    return nueva_izquierda



def add_rest(rest_p):
    
    res = transformar_ecuacion(rest_p)
    if debug:
        print("Transformar:")
        print(res)
    rest = procesar_ecuacion(res)
    if debug:
        print("Procesar:")
        print(rest)
    global list_rest
    list_rest.append(rest)

def create_matrix(funcion_objetivo):
    global matrix, list_rest, count_restricciones, last_x_index,dos_fases
    global contador_x,contador_s_neg,contador_s_pos,contador_artificiales
    
    # Transformar la función objetivo
    if gran_M:
      mx_func = procesar_ecuacion_gran_M(funcion_objetivo)
      
    else:      
      mx_func = procesar_ecuacion(funcion_objetivo)
    
    # Determinar el índice de la última variable de decisión (x1, x2, ..., xn)
    last_x_index = max(int(var[1:]) for coef, var in mx_func if 'x' in var) if any('x' in var for coef, var in mx_func) else 0
    
    # Insertar las variables de decisión y holgura en la primera fila
    i = 1
    for coef, var in mx_func:
        if 'x' in var:
            if matrix.ndim == 1:
                matrix = matrix[:, np.newaxis]  # Convertir a 2D si es necesario
            matrix = np.insert(matrix, i, var, axis=1)
            i += 1

    # Añadir las variables de holgura según el número de restricciones
    count_t = contador_s_pos + contador_s_neg 
    for j in range(count_t):
        if matrix.ndim == 1:
            matrix = matrix[:, np.newaxis]  
        matrix = np.insert(matrix, i, f's{contador_x + j + 1}', axis=1)  # 's3' y 's4' para tus restricciones
        i += 1

     # Añadir las variables artificales según el número de restricciones
    
    for j in range(contador_artificiales):
        if matrix.ndim == 1:
            matrix = matrix[:, np.newaxis]  
        matrix = np.insert(matrix, i, f'a{(contador_x + contador_s_pos + contador_s_neg) + j + 1}', axis=1)  # 's3' y 's4' para tus restricciones
        i += 1

    

    if matrix.ndim == 1:
        matrix = matrix[:, np.newaxis]  
    matrix = np.insert(matrix, i, 'RHS', axis=1)

    # Crear la fila de coeficientes de la función objetivo
    num_cols = matrix.shape[1]
    if min_problem:
        list_coef = ['-Z'] + [0.0] * (num_cols - 1)
    else:
        list_coef = ['Z'] + [0.0] * (num_cols - 1)
    for coef, var in mx_func:
        if var in matrix[0]:
            list_coef[matrix[0].tolist().index(var)] = coef
    list_coef = list_coef + [0.0] * count_restricciones
    if len(list_coef) != num_cols:
        list_coef = list_coef[:num_cols] 
    matrix = np.vstack([matrix, list_coef])
    s = 1
    a = 1
    # Procesar las restricciones y añadir las filas correspondientes
    for count, restr in enumerate(list_rest):
        
        if verificar_variables_artificiales(restr):
            l = [f'a{(contador_x + contador_s_pos + contador_s_neg) + a}'] 
        else:
            l  = [f's{s + contador_x }']  # Las variables de holgura 's3', 's4', etc.
        l.extend([0.0] * (matrix.shape[1] - 1))  

        # Actualizar los coeficientes de la fila l
        for coef, var in restr:
            if var in matrix[0]:  
                index = matrix[0].tolist().index(var)
                l[index] = coef  

        # Colocar el 1 en la columna de la variable artificial correspondiente
        if verificar_variables_artificiales(restr):
            
            holgura_index = matrix[0].tolist().index(f'a{(contador_x + contador_s_pos + contador_s_neg) + a}')
            l[holgura_index] = 1.0  # Solo un '1' en la columna de la variable de holgura
            a += 1
            if verificar_variables_holgura(restr):
                s += 1
        else:
            holgura_index = matrix[0].tolist().index(f's{contador_x + s}')
            l[holgura_index] = 1.0  # Solo un '1' en la columna de la variable de holgura
            s += 1

        # Insertar la nueva fila l en la matriz
        matrix = np.vstack([matrix, l])

    #Ordenar matrix
    
    
    if dos_fases or gran_M:
        matrix = ordenar_filas(matrix)
        
        if dos_fases:
            matrix = insertar_fila_w(matrix)

    #print(matrix)
    matrix = convert_to_numeric(matrix)
    if dos_fases or gran_M:
        matrix = operaciones_fila_columna_w(matrix,funcion_objetivo)
    #print(matrix)
    simplex(matrix)
    #print(matrix)  # Imprimir la matriz resultante

def ordenar_filas(matrix):
    # Separar filas de holgura y artificiales
    filas_holgura = []
    filas_artificiales = []
    inicio = 2
    if dos_fases:
        inicio = 3
    for i in range(inicio, matrix.shape[0]):  # Empezar desde la fila 2 para no modificar las filas '-w' y 'Z'
        variable = matrix[i, 0]  # Primera columna 'BVS'
        
        if variable.startswith('s'):  # Filas de holgura
            filas_holgura.append(matrix[i])
        elif variable.startswith('a'):  # Filas artificiales
            filas_artificiales.append(matrix[i])
    
    # Reorganizar la matriz con las filas de holgura primero, luego las artificiales
    if dos_fases:
        matriz_ordenada = np.vstack([matrix[0], matrix[1], matrix[2], *filas_holgura, *filas_artificiales])
    else:
        matriz_ordenada = np.vstack([matrix[0], matrix[1], *filas_holgura, *filas_artificiales])
    
    return matriz_ordenada


def convert_to_numeric(matrix):
    # Crear una copia de la matriz para no modificar el original
    numeric_matrix = np.copy(matrix)
    
    # Recorrer la matriz y convertir los valores numéricos de cadena a enteros o flotantes
    for i in range(len(numeric_matrix)):
        for j in range(len(numeric_matrix[i])):
            try:
                # Intentar convertir a número (entero o flotante)
                numeric_matrix[i][j] = float(numeric_matrix[i][j])
                
                # Convertir a entero si no tiene decimales
                if numeric_matrix[i][j] == float(numeric_matrix[i][j]):
                    numeric_matrix[i][j] = float(numeric_matrix[i][j])
            except ValueError:
                # Si no se puede convertir a número, continuar con el valor actual (ej. 'x1', 'Z', etc.)
                pass
    
    return numeric_matrix

def verificar_variables_artificiales(sublista):
    for coeficiente, variable in sublista:
        if variable.startswith('a'):  # Verifica si la variable comienza con 'a'
            return True  # Se encontró una variable artificial

    return False  # No se encontraron variables artificiales

def verificar_variables_holgura(sublista):
    for coeficiente, variable in sublista:
        if variable.startswith('s'):  # Verifica si la variable comienza con 'a'
            return True  # Se encontró una variable artificial

    return False  # No se encontraron variables artificiales

def insertar_fila_w(matrix):
    # Crear la nueva fila con el primer elemento '-w' y el resto en 0 por defecto
    nueva_fila = ['-w'] + ['0.0'] * (matrix.shape[1] - 1)

    # Identificar las columnas con variables artificiales (variables que comienzan con 'a')
    for idx, variable in enumerate(matrix[0]):
        if variable.startswith('a'):  # Si la columna tiene una variable artificial
            nueva_fila[idx] = '1.0'  # Colocar un 1 en esa posición

    # Insertar la nueva fila entre la fila 0 y la fila 1
    matrix = np.insert(matrix, 1, nueva_fila, axis=0)

    return matrix

#---------------------------------
#Metodos para gran M
#---------------------------------
def determinar_coeficiente_var_artificiales_gran_M(funcion_objetivo):
        max_digitos = 0
        terminos = re.findall(r'([+-]?\d*\.?\d*)\*x\d+', funcion_objetivo)

        # Iterar por cada coeficiente para obtener el máximo número de dígitos
        for coef in terminos:
            # Remover cualquier signo y contar dígitos
            coef_limpio = coef.replace('-', '').replace('+', '').replace('.', '')
            max_digitos = max(max_digitos, len(coef_limpio))

        # Generar las variables artificiales con coeficientes del doble de dígitos que los coeficientes originales
        coef_variable_artificial = 10 ** (max_digitos  )  # El doble de dígitos menos uno
        return coef_variable_artificial

# Procesar ecuación y restricciones
def procesar_ecuacion_gran_M(ecuacion):
    global contador_x,contador_s_pos,contador_s_neg
    global contador_artificiales
    
    coeficientes = []

    lado_izquierdo, lado_derecho = ecuacion.split('=')
    patrones = re.findall(r'([+-]?\d*\.?\d*)\*x(\d+)', lado_izquierdo)
    for coeficiente, variable in patrones:
        if coeficiente == '' or coeficiente == '+':
            coeficiente = 1
        elif coeficiente == '-':
            coeficiente = -1
        else:
            coeficiente = float(coeficiente)
        coeficientes.append((coeficiente, 'x' + variable))


    inicio =  contador_x + contador_s_pos + contador_s_neg

    coef_variable_artificial = determinar_coeficiente_var_artificiales_gran_M(ecuacion)
    for i in range(0, contador_artificiales):
        a_var = f'a{inicio + i + 1}'
        coeficientes.append((coef_variable_artificial, a_var))


    coeficientes.append((float(lado_derecho.strip()), 'RHS'))
    return coeficientes


# *****************************************************************************************************************
#==================================================================================================================

#                               FUNCIONES PARA VARIABLES NEGATIVAS CON LÍMITE INFERIOR

#==================================================================================================================



#==================================================================================================================
#                                               revisar_rest_conLim
#==================================================================================================================

# Función para revisar restricciones con límites inferiores
def revisar_rest_conLimite(restricciones):
    global conLimite
    global list_secundaria
    global list_x
    for restriccion in restricciones:
        # Solo procesar restricciones con el símbolo ">="
        if ">=" in restriccion:
            # Separamos la parte izquierda de la derecha
            lhs, rhs = restriccion.split(">=")

            # Convertimos la parte izquierda en términos
            terms = lhs.split("+")
            coef_positivos = []  # Lista para coeficientes positivos
            coeficientes_validos = True

            # Recorrer los términos buscando coeficientes 1.0 y 0.0
            for term in terms:
                term = term.strip()  # Limpiamos espacios en blanco

                # Asegurarnos de que el término tiene la forma coeficiente*variable
                if "*" not in term:
                    coeficientes_validos = False
                    break

                # Intentar dividir el término
                try:
                    coef, var = term.split("*")
                    coef = coef.strip()
                    var = var.strip()
                except ValueError:
                    coeficientes_validos = False
                    break

                # Si encontramos coeficiente diferente de 0.0 o 1.0, no es válido
                if coef != "0.0" and coef != "1.0":
                    coeficientes_validos = False
                    break

                # Si el coeficiente es 1.0, guardamos la variable
                if coef == "1.0":
                    coef_positivos.append(var)

                # Si hay más de una variable con coeficiente 1.0, no es válido
                if len(coef_positivos) > 1:
                    coeficientes_validos = False
                    break

            # Validar que el lado derecho de la restricción sea >= -número para límites inferiores
            try:
                limite = float(rhs.strip())
                if limite >= 0:  # Si el límite es no negativo, no es válido
                    coeficientes_validos = False
            except ValueError:
                coeficientes_validos = False

            # Si cumple con las características y tiene exactamente un coeficiente 1.0
            if coeficientes_validos and len(coef_positivos) == 1:
                variable_seleccionada = coef_positivos[0]  # La variable con coeficiente 1
                list_x.append(f"{variable_seleccionada}={variable_seleccionada}-{abs(limite)}")  # Almacenamos la nueva forma de la variable
                conLimite = 1
            else:
                # Guardamos la restricción en list_secundaria si no es negativa con límite inferior
                list_secundaria.append(restriccion)
        else:
            # Guardamos las restricciones que no tienen el símbolo ">=" en list_secundaria
            list_secundaria.append(restriccion)

    # Imprimir el contenido de list_x después de procesar las restricciones
    print("Valores en list_x:", list_x)
    print("Restricciones guardadas en list_secundaria:", list_secundaria)
    return list_secundaria


#==================================================================================================================
#                                           transformar_funcion_ConLimite
#==================================================================================================================
# Función para transformar la función objetivo sin usar eval
def transformar_funcion_ConLimite(funcion_objetivo):
    global reservaObjetivo
    constantes = 0  # Variable para almacenar los valores constantes
    nueva_funcion = funcion_objetivo  # Creamos una copia de la función para transformarla
    
    for var in list_x:
        variable, valor_asociado = var.split("=")
        valor_asociado = valor_asociado.strip()
        
        # Reemplazamos la variable en la función objetivo
        nueva_funcion = nueva_funcion.replace(variable, f"({valor_asociado})")
    
    # Ahora simplificamos la función expandiendo los términos
    nueva_funcion = nueva_funcion.replace(" ", "")  # Quitamos espacios
    partes = nueva_funcion.split("=")
    
    # Agregar un espacio después de 'max' o 'min' antes de 'z'
    if "maxz" in partes[0]:
        partes[0] = partes[0].replace("maxz", "max z")
    elif "minz" in partes[0]:
        partes[0] = partes[0].replace("minz", "min z")

    lado_derecho = partes[1]
    
    # Descomponemos los términos y manejamos las operaciones
    terminos = lado_derecho.split("+")
    nuevo_lado_derecho = []
    
    for termino in terminos:
        if "*" in termino:
            coeficiente, variable = termino.split("*")
            if "(" in variable:  # Si hay una sustitución como (x1 - 5)
                sub_termino = variable[1:-1].split("-")
                nuevo_lado_derecho.append(f"{coeficiente}*{sub_termino[0]}")
                constantes += float(coeficiente) * float(sub_termino[1])  # Sumamos la constante
            else:
                nuevo_lado_derecho.append(termino)
        else:
            nuevo_lado_derecho.append(termino)
    
    # Almacenamos la constante en reservaObjetivo y rearmamos la función
    reservaObjetivo = -constantes  # Almacenamos como valor negativo
    return f"{partes[0]} = {' + '.join(nuevo_lado_derecho)}"


#==================================================================================================================
#                                        reemplazar_enRestriccion_variable
#==================================================================================================================
# Función para sustituir nueva variable en las restricciones
def reemplazar_enRestriccion_variable(restriccion):
    global list_x
    for var in list_x:
        variable, valor_asociado = var.split("=")
        valor_asociado = valor_asociado.strip()
        # Reemplazamos la variable en la restricción
        restriccion = restriccion.replace(variable, f"({valor_asociado})")
    return restriccion

#==================================================================================================================
#                                           transformar_rest_conLimite
#==================================================================================================================
def transformar_rest_conLimite(expression):
    # Paso 1: Distribuir el término multiplicado en el paréntesis
    def distribute(match):
        factor = float(match.group(1))  # El número que multiplica
        inner_expr = match.group(2)  # Lo que está dentro del paréntesis
        
        # Separar los términos dentro del paréntesis
        distributed_terms = []
        const_to_move = 0
        terms = re.split(r'([+-])', inner_expr)
        
        for i, term in enumerate(terms):
            term = term.strip()
            if term and term not in ['+', '-']:  # Ignorar signos
                if 'x' in term:
                    distributed_terms.append(f"{factor}*{term}")
                else:
                    # Convertir el número si es un término numérico
                    num_term = float(term)
                    if i > 0 and terms[i-1] == '-':  # Si el término es negativo
                        const_to_move = factor * abs(num_term)  # Siempre positivo
                        distributed_terms.append(f"{-const_to_move}")  # Mantener signo correcto en la distribución
                    else:
                        const_to_move = factor * num_term
                        distributed_terms.append(f"{const_to_move}")
            elif term in ['+', '-']:
                distributed_terms.append(term)
        
        return " ".join(distributed_terms), const_to_move

    # Paso 2: Distribuir los términos y capturar constantes para mover
    const_moved = 0
    
    def replace_and_collect_constants(match):
        result, const_to_move = distribute(match)
        nonlocal const_moved
        const_moved += abs(const_to_move)  # Aseguramos que la constante que se mueve siempre sea positiva
        return result

    # Reemplazar todas las instancias de la forma "n*(expr)" o "n(expr)"
    expression = re.sub(r'(\d*\.?\d+)\s*\*\s*\((.*?)\)', lambda m: replace_and_collect_constants(m), expression)
    expression = re.sub(r'(\d*\.?\d+)\s*\((.*?)\)', lambda m: replace_and_collect_constants(m), expression)

    # Paso 3: Identificar el operador de la restricción (<=, >=, =)
    operator = None
    if "<=" in expression:
        operator = "<="
    elif ">=" in expression:
        operator = ">="
    elif "=" in expression:
        operator = "="

    if operator is None:
        raise ValueError("No se encontró un operador de restricción válido.")

    # Paso 4: Reorganizar la expresión para mover las constantes al lado derecho
    left_side, right_side = expression.split(operator)

    # Encontrar términos con variables
    variable_terms = re.findall(r'[+-]?\s*\d*\.?\d*\*?x\d*', left_side.replace(" ", ""))

    # Crear la nueva expresión moviendo solo la constante distribuida
    new_left_side = ' + '.join(variable_terms).replace("+ -", "- ").replace(" -", " - ").replace("+ +", "+ ").replace("- +", "- ")
    new_expression = f"{new_left_side} {operator} {float(right_side) + const_moved}"

    # Resultado final
    print(f"\nNueva expresión final: {new_expression}\n")
    return new_expression

#FIN DE FUNCIONES PARA VARIABLES NEGATIVAS CON LÍMITE INFERIOR
# *****************************************************************************************************************

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#==================================================================================================================
#                             FUNCIONES PARA VARIABLES NEGATIVAS SIN LÍMITE INFERIOR
#==================================================================================================================

#==================================================================================================================
#                                          obtener_reemplazosSinLimite
#==================================================================================================================
# Función para obtener los reemplazos sin límite
def obtener_reemplazosSinLimite(variables_sinLimite, restOriginales):
    global list_xSinLimite
    list_xSinLimite = []  # Reiniciar la lista cada vez que se llama la función
    
    # Contar el número de variables diferentes en las restricciones
    variables_en_restricciones = set()
    for restriccion in restOriginales:
        terms = re.split(r'[\+\-\*\/\s]', restriccion)  # Dividimos la restricción en términos sin símbolos
        for term in terms:
            if term.startswith("x"):  # Detectamos variables que empiezan con "x"
                variables_en_restricciones.add(term.strip())

    n = len(variables_en_restricciones)  # Contador de variables en restricciones
    contador = n  # Empezamos el conteo desde n

    # Reemplazar variables en variables_sinLimite
    for variable in variables_sinLimite:
        if variable in variables_en_restricciones:  # Solo reemplazar si la variable está en las restricciones
            contador += 1
            list_xSinLimite.append(f"{variable} = {variable} - x{contador}")

    # Retornar el contenido de list_xSinLimite
    return list_xSinLimite


#==================================================================================================================
#                                reemplazar_enRestriccion_variableSinLimite
#==================================================================================================================
# Función para sustituir nuevas variables en las restricciones y la función objetivo
def reemplazar_enRestriccion_variableSinLimite(expresion):
    global list_xSinLimite
    for var in list_xSinLimite:
        variable, valor_asociado = var.split("=")
        variable = variable.strip()
        valor_asociado = valor_asociado.strip()

        # Reemplazar solo si es una coincidencia exacta de la variable, sin anidar más reemplazos
        expresion = re.sub(rf'\b{re.escape(variable)}\b', f"({valor_asociado})", expresion)

    return expresion

#==================================================================================================================
#                                transformar_rest_sinLimite
#==================================================================================================================
# Función para distribuir los paréntesis y transformar la restricción
def transformar_rest_sinLimite(restriccion):
    print("\ntransformar_rest_sinLimite PRUEBA.PY:  restricciones\n", restriccion)
    # Distribuir los coeficientes fuera del paréntesis en las variables dentro del paréntesis
    restriccion_transformada = re.sub(r'([\d\.]+)\*\(([^)]+)\)', lambda m: distribuir_coefs(m.group(1), m.group(2)), restriccion)
    return restriccion_transformada

#==================================================================================================================
#                                     distribuir_coefs
#==================================================================================================================
# Función auxiliar para distribuir los coeficientes
def distribuir_coefs(coef, variables):
    coef = float(coef)  # Convertir el coeficiente a número flotante
    terminos = variables.split()  # Dividimos los términos dentro del paréntesis por espacios
    print("\nvariables -distribuir_coefs- PRUEBA.PY:\n", variables)
    print("\nterminoss -distribuir_coefs- PRUEBA.PY:\n", terminos)
    
    # Generar la nueva expresión con el coeficiente distribuido
    terminos_transformados = []
    signo = 1  # Para manejar los signos dentro de los términos
    for term in terminos:
        if term == "-":
            signo = -1
        elif term == "+":
            signo = 1
        else:
            if "*" in term:
                num, var = term.split("*")
                num = float(num) * coef * signo
            else:
                var = term
                num = coef * signo
            terminos_transformados.append(f"{num}*{var}")
    print("\nTERMINOS TRANSFORMADOS -distribuir_coefs- PRUEBA.PY:\n", terminos_transformados)
    return " ".join(terminos_transformados)

#==================================================================================================================
#                                     transformar_funcionObjetivo
#==================================================================================================================
# función para transformar la función objetivo
def transformar_funcionObjetivo(funcion):
    # Primero reemplazamos las variables sin límite
    funcion_reemplazada = reemplazar_enRestriccion_variableSinLimite(funcion)
    # Luego distribuimos los coeficientes en la función objetivo
    funcion_transformada = transformar_rest_sinLimite(funcion_reemplazada)
    return funcion_transformada


#==================================================================================================================
#                                     sustituir_valoresSolucionSL
#==================================================================================================================
def sustituir_valoresSolucionSL(variables_decision):
    global list_xSinLimite
    print("\nvariables_decision", variables_decision)
    print("\nlist_xSinLimite", list_xSinLimite)
    resultado_finalSL = []  # Lista final donde se almacenarán los resultados
    # Crear un conjunto de las variables que no deben guardarse (las que están después del "-")
    variables_a_excluir = set()
    for expr in list_xSinLimite:
        partes = expr.split(" = ")
        if "-" in partes[1]:
            var_derecha = partes[1].split(" - ")[1].strip()  # Obtenemos la variable después del "-"
            variables_a_excluir.add(var_derecha)

    # Realizar las sustituciones
    for expr in list_xSinLimite:
        partes = expr.split(" = ")
        var_izquierda = partes[0].strip()  # La variable a la izquierda del "="
        var_derecha, var_resta = partes[1].split(" - ")

        # Obtener los valores de las variables correspondientes en variables_decision
        valor_var_derecha = variables_decision.get(var_derecha.strip(), 0.0)
        valor_var_resta = variables_decision.get(var_resta.strip(), 0.0)

        # Realizar la operación de resta
        resultado = valor_var_derecha - valor_var_resta

        # Guardar el resultado solo si la variable izquierda no está excluida y es diferente de 0.0
        if var_izquierda not in variables_a_excluir:
            if resultado != 0.0:
                resultado_finalSL.append(f"{var_izquierda}: {resultado}*")
            else:
                resultado_finalSL.append(f"{var_izquierda}: {resultado}")

    # Agregar variables de decision que no han sido sustituidas ni excluidas
    for var, valor in variables_decision.items():
        if var not in variables_a_excluir and var not in [v.split(" = ")[0] for v in list_xSinLimite]:
            if valor != 0.0:
                resultado_finalSL.append(f"{var}: {valor}*")
            else:
                resultado_finalSL.append(f"{var}: {valor}")

    return resultado_finalSL

#FIN DE FUNCIONES PARA VARIABLES NEGATIVAS SIN LÍMITE INFERIOR
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#==================================================================================================================

#                                               FUNCIONES SIMPLEX

#==================================================================================================================

# Función para encontrar la variable entrante (mínimo valor negativo en la fila Z)
# Función para encontrar la variable entrante (mínimo valor negativo en la fila Z)
def variable_entrante(matrix):
    z_row = matrix[1, 1:-1].astype(float)  # Convertir a float solo la parte numérica
    min_value = min(z_row)
    if min_value >= 0:
        return None  # No hay más variables negativas, el algoritmo termina
    # Obtener los índices que tienen el valor mínimo
    indices_minimos = [i + 1 for i, val in enumerate(z_row) if val == min_value]

    # Si solo hay un valor mínimo, lo retornamos directamente
    if len(indices_minimos) == 1:
        return indices_minimos[0]
    # Si hay un empate, aplicamos las reglas de prioridad:
    decision_vars = [i for i in indices_minimos if matrix[0, i].startswith('x')]
    slack_vars = [i for i in indices_minimos if matrix[0, i].startswith('s')]
    artiffical_vars = [i for i in indices_minimos if matrix[0, i].startswith('a')]

    if decision_vars:
        return min(decision_vars)  # Priorizar la variable de decisión con subíndice menor
    elif slack_vars != []:
        return min(slack_vars)  # Si solo hay variables de holgura, elegir la de subíndice menor
    else:
        return min(artiffical_vars)


# Función para calcular los radios y encontrar la variable saliente
def variable_saliente(matrix, col_entrante):
    global solucion_no_acotada,fase_1,dos_fases
    radios = []
    indices_salientes = []
    inicio = 2
    if dos_fases:
        inicio = 3
    
    for i in range(inicio, matrix.shape[0]):  # Ignorar la fila Z (fila 1) 
        rhs = float(matrix[i, -1])  # RHS de la restricción
        coef_entrante = float(matrix[i, col_entrante])
        if coef_entrante > 0:
            radios.append(rhs / coef_entrante)
            indices_salientes.append(i)  # Guardar índice de la fila
        else:
            radios.append(float('inf'))  # Radio es infinito si coeficiente es <= 0
            indices_salientes.append(i)

    # Asegurarse de que estamos eligiendo el radio más pequeño
    min_radio = min(radios)
    #print(min_radio)
    #print(radios)
    #print(indices_salientes)
    if min_radio == float('inf'):
        print("El problema es no acotado")
        solucion_no_acotada = 1
        return None  # No hay solución acotada

    indices_minimos = [indices_salientes[i]  for i, val in enumerate(radios) if abs(val) == abs(min_radio)]
    #print(indices_minimos)
    if len(indices_minimos) == 1:
        return indices_minimos[0]  # Solo hay un índice mínimo, lo retornamos

    # Si hay un empate, priorizar las variables de holgura sobre las de decisión
    artiffical_vars = [i for i in indices_minimos if matrix[i, 0].startswith('s')]
    holgura_vars = [i for i in indices_minimos if matrix[i, 0].startswith('s')]
    decision_vars = [i for i in indices_minimos if matrix[i, 0].startswith('x')]

    if artiffical_vars:
        return artiffical_vars[0]
    elif holgura_vars:
        return holgura_vars[0]  # Priorizar la salida de variable de holgura con menor subíndice
    else:
        return decision_vars[0]  # Salir la variable de decisión con menor subíndice
   # else:
    #    return indices_minimos[0]  # Si no hay holgura ni decisión, regresar el primer índice




operaciones = []

def operaciones_fila_columna(matrix, fila_saliente, col_entrante):
    global operaciones
    pivot = float(matrix[fila_saliente, col_entrante])
    # Dividir la fila saliente por el pivote
    for j in range(1, matrix.shape[1]):
        matrix[fila_saliente, j] = round(float(matrix[fila_saliente, j]) / pivot, 2)
    
    operaciones.append(f"fila {fila_saliente - 1} / {pivot:.2f} --> fila {fila_saliente - 1}")
    
    for i in range(1, matrix.shape[0]):  # Iterar por todas las filas excepto la saliente
        if i != fila_saliente:
            factor = float(matrix[i, col_entrante])
            for j in range(1, matrix.shape[1]):
                matrix[i, j] = round(float(matrix[i, j]) - factor * float(matrix[fila_saliente, j]), 2)
            if factor != 0:
                operaciones.append(f" {-factor:.2f} * fila {fila_saliente - 1} + fila {i - 1} -->   fila {i - 1}")
    
    return matrix

def operaciones_fila_columna_w(matrix,funcion_objetivo):
    global operaciones
    fila_w = 1  # Asumimos que la fila '-w' es la fila 1
    
    for col in range(1, matrix.shape[1]):  # Iterar por todas las columnas excepto la primera (BVS)
        valor_w = float(matrix[fila_w, col])
        if gran_M:
            num = determinar_coeficiente_var_artificiales_gran_M(funcion_objetivo)
        else:
            num = 1
        if valor_w == num:  # Si encontramos un 1 en la fila -w
            # Encontrar la fila que tiene un pivote 1 en esa columna
            for fila in range(2, matrix.shape[0]):  # Saltar las filas 0 y 1
                if float(matrix[fila, col]) == 1.0:  # Encontrar la fila pivote
                    factor = valor_w
                    # Restar la fila pivote multiplicada por el valor de la fila -w en esa columna
                    for j in range(1, matrix.shape[1]):
                        matrix[fila_w, j] = round(float(matrix[fila_w, j]) - factor * float(matrix[fila, j]), 2)
                    operaciones.append(f" -{factor:.2f} * fila {fila - 1} + fila {fila_w - 1} --> fila {fila_w - 1}")
    
    return matrix

def variables_artificiales_no_basicas(matrix):
    # Extraer la primera columna de la matriz (columna de las variables básicas)
    primera_columna = matrix[2:, 0]  # Desde la fila 2 para evitar 'BVS' y '-w'
    
    # Verificar si hay alguna variable que contenga "a"
    return not any('a' in str(variable) for variable in primera_columna)


def eliminar_fila_w(matrix):
    # Verifica si la fila "-w" (segunda fila) tiene únicamente valores positivos (excluyendo la primera columna 'BVS')
    fila_w = matrix[1, 1:]  # Ignorar la columna 'BVS'
    
    # Si todos los valores son mayores o iguales a 0, eliminamos la fila
    if all(float(x) >= 0 for x in fila_w):
        # Eliminar la segunda fila (-w)
        matrix = np.delete(matrix, 1, axis=0)
    
    return matrix

def eliminar_columnas_artificiales(matrix):
    # Identificar las columnas que contienen una variable artificial (aquellas que contienen "a")
    columnas_a_eliminar = [i for i, col in enumerate(matrix[0, 1:], start=1) if 'a' in str(col)]
    
    # Eliminar las columnas que contienen variables artificiales
    matrix_sin_artificiales = np.delete(matrix, columnas_a_eliminar, axis=1)
    
    return matrix_sin_artificiales

def fila_w_positiva(matrix):
    # Verifica si la fila "-w" (segunda fila) tiene únicamente valores positivos o cero (excluyendo la primera columna 'BVS')
    fila_w = matrix[1, 1:]  # Ignorar la columna 'BVS'
    
    # Verificar si todos los valores son mayores o iguales a 0
    return all(float(x) >= 0 for x in fila_w)

# Función para actualizar la tabla tras cada iteración
variable_entrante_global = None
variable_saliente_global = None

def actualizar_tabla(matrix):
    global variable_entrante_global
    global variable_saliente_global
    col_entrante = variable_entrante(matrix)
    if col_entrante is None:
        return matrix, False  # No hay más variables entrantes, se terminó
    
    fila_saliente = variable_saliente(matrix, col_entrante)
    if fila_saliente is None:
        return matrix, False  # Solución no acotada

    # Actualizar las variables básicas (primera columna)
    print("Variable entrante:")
    variable_entrante_global = matrix[0,col_entrante]
    print(matrix[0,col_entrante])
    print("Variable salida:")
    variable_saliente_global = matrix[fila_saliente, 0]
    print(matrix[fila_saliente, 0])
    matrix[fila_saliente, 0] = matrix[0, col_entrante]  # Cambiar la BVS por la nueva variable básica
    matrix = operaciones_fila_columna(matrix, fila_saliente, col_entrante)
    
    return matrix, True

# Función para imprimir la matriz 
def imprimir_matriz(matrix):
    for row in matrix:
        print(" ".join(f"{elem:10}" if isinstance(elem, str) else f"{float(elem):10.2f}" for elem in row))

#============================================================================
# Sustituye los valores de las variables que fueron negativas con limite inferior
def sustituir_valoresSolucion(variables_decision):
    global list_x
    # Creamos un conjunto con las variables de list_x para fácil acceso
    variables_list_x = {expresion.split('=')[0].strip() for expresion in list_x}
    
    # Creamos un conjunto para marcar las variables que eran básicas desde el inicio
    variables_basicas = {var for var, valor in variables_decision.items() if valor != 0.0}
    
    # Primero procesamos las expresiones que están en list_x
    for expresion in list_x:
        # Dividimos la expresión en dos partes (ejemplo: 'x1=x1-8.0')
        var, operacion = expresion.split('=')
        
        # Identificamos la variable (ejemplo: 'x1') y su valor en el diccionario 'variables_decision'
        var = var.strip()
        valor_inicial = variables_decision[var]
        
        # Si la variable tiene un valor diferente de 0.0, realizamos la transformación
        if valor_inicial != 0.0:
            # Reemplazamos todas las variables que aparecen en la operación
            for variable in variables_decision:
                if variable in operacion:
                    operacion = operacion.replace(variable, str(variables_decision[variable]))
            
            # Evaluamos la operación
            resultado = eval(operacion)
            
            # Actualizamos el valor en variables_decision con el resultado
            variables_decision[var] = resultado
        else:
            # Si la variable es 0.0, no se realiza la operación y se mantiene el valor
            variables_decision[var] = valor_inicial
    
    # Crear una lista para almacenar el resultado final
    resultado_final = []
    
    # Validación: Guardar las variables de decisión con los valores finales en lugar de imprimir directamente
    for var, valor in variables_decision.items():
        # Resaltamos las variables que eran básicas desde el inicio con un asterisco (*)
        if var in variables_basicas:
            resultado_final.append(f"{var}: {valor}*")
        else:
            resultado_final.append(f"{var}: {valor}")
    
    # Retornamos el resultado en una variable
    return resultado_final

#============================================================================


def imprimir_solucion_optima(matrix):
    solucion = ""
    # Mostrar el valor óptimo de Z
    FinalZ = 0
    valor_Z = float(matrix[1, -1])  # Última columna de la fila Z
    if conLimite:
        if min_problem:
            originalZ = -1*valor_Z
            FinalZ = originalZ+reservaObjetivo
            solucion += f"Valor óptimo de Z: {FinalZ}\n"
        else:
            FinalZ = valor_Z+reservaObjetivo
            solucion += f"Valor óptimo de Z: {FinalZ}\n"
    else: 
        if min_problem:
            FinalZ = -1*valor_Z
            solucion += f"Valor óptimo de Z: {FinalZ}\n"
        else:
            FinalZ = valor_Z
            solucion += f"Valor óptimo de Z: {FinalZ}\n"
    
    # Obtener todas las variables (excepto Z y RHS)
    todas_las_vars = matrix[0, 1:-1]  # Encabezados de las columnas de variables
    
    # Crear un diccionario para almacenar las variables y sus valores
    valores_variables = {var: 0 for var in todas_las_vars}  # Inicializar todas en 0
    
    # Asignar valores a las variables que están en la base
    for i in range(2, matrix.shape[0]):  # Filas de variables básicas
        var_basica = matrix[i, 0]
        valor_rhs = float(matrix[i, -1])  # Última columna (RHS)
        valores_variables[var_basica] = valor_rhs
    
    # Separar variables de decisión y de holgura
    variables_decision = {var: valores_variables[var] for var in todas_las_vars if var.startswith('x')}
    variables_holgura = {var: valores_variables[var] for var in todas_las_vars if var.startswith('s')}
    variablesHolguraSol = []
    variablesDesicionSol = []
    if conLimite:
        # Imprimir las variables de decisión
        solucion += "\nVariables de decisión:\n"
        variablesDesicionSol = sustituir_valoresSolucion(variables_decision)
        for variable in variablesDesicionSol:
            solucion += variable + "\n"
        # Imprimir las variables de holgura
        solucion += "\nVariables de holgura:\n"
        for var, valor in variables_holgura.items():
            if valor != 0.0:
                variablesHolguraSol.append(f"{var}: {valor}*")
                solucion += f"{var}: {valor}*\n"
            else:
                variablesHolguraSol.append(f"{var}: {valor}")
                solucion += f"{var}: {valor}\n"
    elif sinLimite:
        # Imprimir las variables de decisión
        solucion += "\nVariables de decisión:\n"
        variablesDesicionSol = sustituir_valoresSolucionSL(variables_decision)
        for variable in variablesDesicionSol:
            solucion += variable + "\n"
        # Imprimir las variables de holgura
        solucion += "\nVariables de holgura:\n"
        for var, valor in variables_holgura.items():
            if valor != 0.0:
                variablesHolguraSol.append(f"{var}: {valor}*")
                solucion += f"{var}: {valor}*\n"
            else:
                variablesHolguraSol.append(f"{var}: {valor}")
                solucion += f"{var}: {valor}\n"
    else:
        # Imprimir las variables de decisión solucion += "\nVariables de decisión:\n"
        solucion += "\nVariables de decisión:\n"
        for var, valor in variables_decision.items():
            if valor != 0.0:
                variablesDesicionSol.append(f"{var}: {valor}*")
                solucion += f"{var}: {valor}*\n"
            else:
                variablesDesicionSol.append(f"{var}: {valor}")
                solucion += f"{var}: {valor}\n"
        # Imprimir las variables de holgura
        solucion += "\nVariables de holgura:\n"
        for var, valor in variables_holgura.items():
            if valor != 0.0:
                variablesHolguraSol.append(f"{var}: {valor}*")
                solucion += f"{var}: {valor}*\n"
            else:
                variablesHolguraSol.append(f"{var}: {valor}")
                solucion += f"{var}: {valor}\n"
    if problema_lineal_infactible:
        solucion += "Problema Lineal Infactible\n"
    elif solucion_no_acotada:
        solucion += "Solución no acotada\n"
    for variable in variablesDesicionSol:
            solucion += variable + "\n"
    solucion += "\nVariables de Holgura\n"
    for variable in variablesHolguraSol:
            solucion += variable + "\n"
    return solucion
    

# Inicializar una matriz para almacenar los cambios
resumen_iteraciones = []

# Función para imprimir la matriz resumen
def imprimir_resumen(resumen):
    print("\n--- Resumen de Iteraciones ---")
    encabezados = resumen[0]
    print("    |     ".join(encabezados))  # Imprimir encabezados
    print("-" * (len(encabezados) * 10 + 10))  # Separador
    for fila in resumen[1:]:
        print(" | ".join(f"{elem:10.2f}" if isinstance(elem, (int, float)) else str(elem) for elem in fila))




# =================================================================================================

#                                               SIMPLEX
# =================================================================================================
# Proceso iterativo del método simplex
def simplex(matrix):
    global operaciones, solucion_no_acotada, problema_lineal_infactible, dos_fases, fase_1
    iteracion = 0
    global operaciones_historial 
    # Encabezados para el resumen, obtener desde la fila de las variables
    if dos_fases and min_problem:
        variables = ["Iteración", "-Z"] + ["-w"] + [f"{var}" for var in matrix[0, 1:-1]]
    elif dos_fases:
        variables = ["Iteración", "Z"] + ["-w"] + [f"{var}" for var in matrix[0, 1:-1]]
    elif min_problem:
        variables = ["Iteración", "-Z"] + [f"{var}" for var in matrix[0, 1:-1]]
    else:
        variables = ["Iteración", "Z"] + [f"{var}" for var in matrix[0, 1:-1]]

    resumen_iteraciones.append(variables)
    
    # Mostrar la matriz inicial como iteración 0
    print(f"Iteración {iteracion}:")
    imprimir_matriz(matrix)
    continuar = mostrar_iteracion(matrix, iteracion, resumen_iteraciones)  # Mostrar iteración 0

    while continuar:
        # Almacenar los valores actuales de Z y variables en la matriz de resumen
        fila_resumen = [iteracion]  # Comenzar con el número de iteración
        if dos_fases:
            fila_resumen.append(float(matrix[2, -1]))  # Agregar el valor de Z
            fila_resumen.append(float(matrix[1, -1]))  # Agregar el valor de -w
        elif fase_1 == 1:
            fila_resumen.append(float(matrix[1, -1]))  # Agregar el valor de Z
            fila_resumen.append(float(0.0))  # Agregar el valor de -w
        else:
            fila_resumen.append(float(matrix[1, -1]))  # Agregar el valor de Z

        # Inicializar un diccionario para las variables básicas con sus valores
        valores_basicos = {matrix[i, 0]: float(matrix[i, -1]) for i in range(2, matrix.shape[0])}
        
        # Agregar los valores de las variables de decisión y holgura
        for var in matrix[0, 1:-1]:  # Recorre las variables de decisión y holgura desde la fila 0
            if var in valores_basicos:  # Si la variable está en las básicas
                fila_resumen.append(valores_basicos[var])
            else:
                fila_resumen.append(0.0)  # Si no está en las básicas, su valor es 0.0
        
        resumen_iteraciones.append(fila_resumen)  # Agregar la fila a la matriz de resumen
        
        iteracion += 1
        
        # Actualizar la tabla y verificar si se continúa
        matrix, continuar = actualizar_tabla(matrix)

        if dos_fases and not continuar:
            if variables_artificiales_no_basicas(matrix):
                matrix = eliminar_fila_w(matrix)
                matrix = eliminar_columnas_artificiales(matrix)
                dos_fases = 0
                fase_1 = 1
                matrix, continuar = actualizar_tabla(matrix)
            else:
                problema_lineal_infactible = 1

        if operaciones != []:
            print(f"\nIteración {iteracion}:")
            operaciones_historial.append(operaciones[:])  # Almacenar las operaciones en la lista
            imprimir_matriz(matrix)
            print("\nOperaciones realizadas en esta iteración:")
            for op in operaciones:
                print(op)
            operaciones.clear()  # Limpiar la lista de operaciones después de imprimirlas
        
        # Mostrar la iteración actual
        if continuar:
            continuar = mostrar_iteracion(matrix, iteracion, resumen_iteraciones)
    
    # Imprimir la solución óptima y el resumen de iteraciones
    print("------------------------------------------------------")
    if solucion_no_acotada:
        print(f"\nSolucion optima alacanzada hasta la iteracion {iteracion}")

    elif problema_lineal_infactible:
        print("Problema Lineal Infactibles")

    else:
        print("\nSolución óptima alcanzada.")

    print("------------------------------------------------------")
    imprimir_solucion_optima(matrix)
    imprimir_resumen(resumen_iteraciones)
    mostrar_resultados(matrix)
    
    return matrix



#TERMINA LÓGICA
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#==================================================================================================================

#                                                 INTERFAZ GRÁFICA

#==================================================================================================================


#==================================================================================================================
#                                                 mostrar_iteracion
#==================================================================================================================
# Variables globales para almacenar variables de iteración anterior
variable_entrante_anterior = None
variable_saliente_anterior = None

def mostrar_iteracion(matrix, iteracion, resumen_iteraciones):
    global ventana_matriz, variable_entrante_anterior, variable_saliente_anterior

    # Crear ventana secundaria para mostrar la matriz
    ventana_matriz = tk.Toplevel(root)
    ventana_matriz.title(f"Iteración {iteracion}")
    ventana_matriz.geometry("800x600")
    ventana_matriz.configure(bg="black")  # Color de fondo de la ventana
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview", background="#060270", foreground="white", rowheight=25, fieldbackground="#060270")  
    estilo.map("Treeview", background=[("selected", "#060270")])
    # Frame para centrar la tabla
    frame_centrado = tk.Frame(ventana_matriz)
    frame_centrado.pack(padx=20, pady=20)

    # Crear la tabla para la matriz con barras de desplazamiento
    matriz_tree = ttk.Treeview(frame_centrado, selectmode="browse", show="headings")
    matriz_tree.pack(side="left")

    # Barras de desplazamiento
    scrollbar_y = tk.Scrollbar(frame_centrado, orient="vertical", command=matriz_tree.yview)
    scrollbar_y.pack(side="left", fill="y")
    scrollbar_x = tk.Scrollbar(ventana_matriz, orient="horizontal", command=matriz_tree.xview)
    scrollbar_x.pack(fill="x")
    
    matriz_tree.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Definir las columnas de la tabla
    columnas = [f"Columna {i}" for i in range(matrix.shape[1])]
    matriz_tree["columns"] = columnas

    # Formatear las columnas
    for columna in columnas:
        matriz_tree.column(columna, anchor="center", width=100)
        matriz_tree.heading(columna, text=columna)

    # Insertar los datos en la tabla
    for i, fila in enumerate(matrix):
        matriz_tree.insert("", "end", values=[str(elem) for elem in fila])

    # Mostrar la variable entrante y saliente si es iteración 1 o superior
    if iteracion >= 0:
        # Mostrar la variable entrante y saliente de la iteración anterior
        if variable_entrante_anterior is not None and variable_saliente_anterior is not None:
            tk.Label(ventana_matriz, text=f"Variable entrante: {variable_entrante_anterior}",background="black", font=("Arial black", 8),foreground="white").pack(pady=10)
            tk.Label(ventana_matriz, text=f"Variable saliente: {variable_saliente_anterior}",background="black",font=("Arial black", 8), foreground="white").pack(pady=10)

        # Calcular la variable entrante y saliente para la iteración actual
        col_entrante = variable_entrante(matrix)
        if col_entrante is not None:
            fila_saliente = variable_saliente(matrix, col_entrante)
            variable_entrante_anterior = matrix[0, col_entrante]
            variable_saliente_anterior = matrix[fila_saliente, 0]

            # Mostrar las variables de la iteración actual
            #tk.Label(ventana_matriz, text=f"Variable entrante: {matrix[0, col_entrante]}").pack(pady=10)
            #tk.Label(ventana_matriz, text=f"Variable saliente: {matrix[fila_saliente, 0]}").pack(pady=10)
        else:
           print("No hay más variables entrantes")

    # Mostrar las operaciones fila-columna realizadas
    if iteracion > 0:
        texto_operaciones = tk.Text(ventana_matriz, width=80, height=10)
        texto_operaciones.pack(pady=10)
        texto_operaciones.insert(tk.END, "\n".join(operaciones_historial[iteracion-1]))
        texto_operaciones.config(state="disabled")
    
    # Frame para los botones
    frame_botones = tk.Frame(ventana_matriz)
    frame_botones.pack(pady=10)

    def avanzar():
        ventana_matriz.destroy()
        return True

    def regresar():
        nonlocal iteracion
        iteracion -= 1
        ventana_matriz.destroy()
        mostrar_iteracion(matrix, iteracion, resumen_iteraciones)
        return False

    tk.Button(frame_botones, text="Regresar", command=regresar, bg="#f44336", fg="white", activebackground="#e60000", activeforeground="white", font=("Arial black", 9)).pack(side=tk.LEFT)
    tk.Button(frame_botones, text="Continuar", command=avanzar, bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", font=("Arial black", 9)).pack(side=tk.LEFT)
    
    ventana_matriz.wait_window()
    return avanzar()


#==================================================================================================================
#                                             mostrar_resultados
#==================================================================================================================

# Inicializar ventana_resultados al inicio del programa
ventana_resultados = None

def mostrar_resultados(matrix):
    global ventana_resultados
    global resumen_iteraciones

    # Verificar si ya existe una ventana de resultados abierta y eliminarla
    if ventana_resultados is not None and ventana_resultados.winfo_exists():
        ventana_resultados.destroy()  # Cerrar la ventana anterior

    # Crear ventana secundaria para mostrar los resultados
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados del Simplex")
    ventana_resultados.geometry("900x700")
    ventana_resultados.configure(bg="black")  # Color de fondo de la ventana

    # Frame principal con canvas y scrollbars
    frame_principal = tk.Frame(ventana_resultados, bg="black")
    frame_principal.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_principal, bg="black")
    canvas.pack(side="left", fill="both", expand=True)

    # Barras de desplazamiento
    scrollbar_y = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview, bg="white")  # Lila
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x = tk.Scrollbar(ventana_resultados, orient="horizontal", command=canvas.xview, bg="white")  # Lila
    scrollbar_x.pack(fill="x")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Frame dentro del canvas para el contenido
    contenido_frame = tk.Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=contenido_frame, anchor="nw")
    contenido_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Frame para centrar la tabla de matriz final
    frame_centrado_matriz = tk.Frame(contenido_frame, bg="black")
    frame_centrado_matriz.pack(padx=20, pady=20)

    # Crear la tabla para la matriz final con scrollbars
    matriz_tree = ttk.Treeview(frame_centrado_matriz, selectmode="browse", show="headings")
    matriz_tree.pack(side="left")

    scrollbar_y_matriz = tk.Scrollbar(frame_centrado_matriz, orient="vertical", command=matriz_tree.yview, bg="white")  # Lila
    scrollbar_y_matriz.pack(side="left", fill="y")
    scrollbar_x_matriz = tk.Scrollbar(contenido_frame, orient="horizontal", command=matriz_tree.xview, bg="white")  # Lila
    scrollbar_x_matriz.pack(fill="x")

    matriz_tree.config(yscrollcommand=scrollbar_y_matriz.set, xscrollcommand=scrollbar_x_matriz.set)

    # Definir las columnas de la tabla
    columnas = [f"Columna {i}" for i in range(matrix.shape[1])]
    matriz_tree["columns"] = columnas

    # Formatear las columnas
    for columna in columnas:
        matriz_tree.column(columna, anchor="center", width=100)
        matriz_tree.heading(columna, text=columna)

    # Insertar los datos en la tabla
    for i, fila in enumerate(matrix):
        matriz_tree.insert("", "end", values=[str(elem) for elem in fila])

    # Estilo de la tabla
    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview", background="#0B7272", foreground="black", rowheight=25, fieldbackground="#0B7272")  
    estilo.map("Treeview", background=[("selected", "#ff5722")])

    # Mostrar la solución óptima
    tk.Label(contenido_frame, text="Solución Óptima", bg="black", fg= "white", font=("Arial", 12, "bold")).pack(pady=10)
    texto_solucion = tk.Text(contenido_frame, width=80, height=10, bg="#ffffff")
    texto_solucion.pack(pady=10)
    texto_solucion.insert(tk.END, imprimir_solucion_optima(matrix))
    texto_solucion.config(state="disabled")

    # Frame para el resumen de iteraciones
    frame_centrado_resumen = tk.Frame(contenido_frame, bg="#9B99E0")
    frame_centrado_resumen.pack(padx=20, pady=20)

    # Crear la tabla para el resumen de iteraciones con scrollbars
    resumen_tree = ttk.Treeview(frame_centrado_resumen, selectmode="browse", show="headings")
    resumen_tree.pack(side="left")

    scrollbar_y_resumen = tk.Scrollbar(frame_centrado_resumen, orient="vertical", command=resumen_tree.yview, bg="white")  # Lila
    scrollbar_y_resumen.pack(side="left", fill="y")
    scrollbar_x_resumen = tk.Scrollbar(contenido_frame, orient="horizontal", command=resumen_tree.xview, bg="white")  # Lila
    scrollbar_x_resumen.pack(fill="x")

    resumen_tree.config(yscrollcommand=scrollbar_y_resumen.set, xscrollcommand=scrollbar_x_resumen.set)

    # Definir las columnas de la tabla
    columnas_resumen = resumen_iteraciones[0]
    resumen_tree["columns"] = columnas_resumen

    # Formatear las columnas
    for columna in columnas_resumen:
        resumen_tree.column(columna, anchor="center")
        resumen_tree.heading(columna, text=columna)

    # Insertar los datos en la tabla
    for fila in resumen_iteraciones[1:]:
        resumen_tree.insert("", "end", values=[str(elem) for elem in fila])

    # Botón para regresar a la ventana principal
    boton_regresar = tk.Button(contenido_frame, text="Regresar", command=regresar_a_principal_resultados, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
    boton_regresar.pack(pady=10)
    
    # Botón para volver al inicio
    boton_inicio = tk.Button(contenido_frame, text="Volver al Inicio", command=reiniciar_aplicacion, bg="#ff5722", fg="white", font=("Arial", 10, "bold"))
    boton_inicio.pack(pady=10)




def reiniciar_aplicacion():
    global num_variables, num_restricciones, operaciones, solucion_no_acotada, problema_lineal_infactible
    global dos_fases, fase_1, gran_M, count_restricciones, count_artificales, contador_x, contador_s_pos, contador_s_neg, contador_artificiales, matrix, list_rest, last_x_index, list_x, conLimite, reservaObjetivo, list_secundaria, rest_inicial, variables_sinLimite, restricciones_finales, list_xSinLimite, sinLimite, list_secundariaSL
    global variable_entrante_anterior, variable_saliente_anterior
    variable_entrante_anterior = None
    variable_saliente_anterior = None
    num_variables = 0
    num_restricciones = 0
    operaciones.clear()
    solucion_no_acotada = 0
    problema_lineal_infactible = 0
    dos_fases = 0
    fase_1 = 0
    gran_M = 0
    count_restricciones = 1
    count_artificales = 1
    contador_x = 0
    contador_s_pos = 0
    contador_s_neg = 0
    contador_artificiales = 0
    matrix = np.array(["BVS"], dtype=object)
    list_rest.clear()
    last_x_index = 0
    list_x.clear()
    conLimite = 0
    reservaObjetivo = 0
    list_secundaria.clear()
    rest_inicial.clear()
    variables_sinLimite.clear()
    restricciones_finales.clear()
    list_xSinLimite.clear()
    sinLimite = 0
    list_secundariaSL.clear()
    resumen_iteraciones.clear()  # Limpiar el resumen de iteraciones
    global ventana_matriz
    ventana_matriz.withdraw()
    global operaciones_historial
    operaciones_historial.clear() 
    #ventana_matriz.destroy()
    # Cerrar las ventanas secundarias
    if 'ventana_matriz' in globals():
        ventana_matriz.configure(bg="black")  # Color de fondo de la ventana
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#060270", foreground="#060270", rowheight=25, fieldbackground="#060270")  
        estilo.map("Treeview", background=[("selected", "#060270")])

    if 'ventana_resultados' in globals():
        ventana_resultados.configure(bg="black")  # Color de fondo de la ventana
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#060270", foreground="white", rowheight=25, fieldbackground="black") 
        estilo.map("Treeview", background=[("selected", "#060270")])
    
    if 'ventana_funcion' in globals():
        ventana_funcion.destroy()
    if 'ventana_resultados' in globals():
        ventana_resultados.destroy()
    
    root.deiconify()  # Mostrar la ventana principal de nuevo

def regresar_a_principal_resultados():
    ventana_resultados.destroy()

def regresar_a_principal():
    ventana_funcion.destroy()
    root.deiconify()  # Mostrar la ventana principal de nuevo



# ===============================================================================================
#                                     validar_entero_positivo
# ===============================================================================================

def validar_entero_positivo(valor):
    return valor == "" or (valor.isdigit() and int(valor) > 0)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                           NUEVAS VENTANAS PARA EL MANEJO DE MÉTODOS


def seleccionar_metodo_resolucion():
    global metodo_var
    global ventana_metodo
    
    ventana_metodo = tk.Toplevel(ventana_funcion)
    ventana_metodo.title("Seleccione el método de resolución")
    ventana_metodo.geometry("400x300")
    ventana_metodo.configure(bg="black")
    ventana_metodo.resizable(False, False)  # False para ancho y alto

    tk.Label(ventana_metodo, text="Seleccione el método con el que desea resolver el problema:", 
             bg="black", fg="white", font=("Arial black", 9)).pack(pady=10)

    metodo_var = tk.StringVar()
    opciones_metodo = [
        "Solución estándar",
        "Gran M",
        "Dos fases",
        "Sin límite (estándar)",
        "Sin límite (dos fases)",
        "Con límite (estándar)",
        "Con límite (dos fases)"
    ]
    
    metodo_combo = ttk.Combobox(ventana_metodo, textvariable=metodo_var, values=opciones_metodo, state="readonly")
    metodo_combo.pack(pady=10)

    tk.Button(ventana_metodo, text="Confirmar", command=confirmar_metodo_resolucion, 
              bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", font=("Arial black", 9)).pack(pady=10)

def confirmar_metodo_resolucion():
    global gran_M, dos_fases, sinLimite, conLimite, variables_sinLimite

    metodo_seleccionado = metodo_var.get()
    
    if metodo_seleccionado == "Gran M":
        gran_M = 1
    elif metodo_seleccionado == "Dos fases":
        dos_fases = 1
    elif metodo_seleccionado == "Sin límite (estándar)":
        sinLimite = 1
        ventana_metodo.destroy()
        mostrar_seleccion_variables_libres()
        return  # Retornar para esperar la selección de variables
    elif metodo_seleccionado == "Sin límite (dos fases)":
        sinLimite = 1
        dos_fases = 1
        ventana_metodo.destroy()
        mostrar_seleccion_variables_libres()
        return  # Retornar para esperar la selección de variables
    elif metodo_seleccionado == "Con límite (estándar)":
        conLimite = 1
    elif metodo_seleccionado == "Con límite (dos fases)":
        conLimite = 1
        dos_fases = 1

    ventana_metodo.destroy()  # Cerrar la ventana de selección del método
    confirmar_funcion_objetivo()  # Llamar al proceso principal después de confirmar el método

def mostrar_seleccion_variables_libres():
    global ventana_variables_libres, checkboxes, variables_seleccionadas
    
    ventana_variables_libres = tk.Toplevel(ventana_funcion)
    ventana_variables_libres.title("Seleccione las variables sin límite")
    ventana_variables_libres.geometry("500x500")
    ventana_variables_libres.configure(bg="black")
    ventana_variables_libres.resizable(False, True)  # False para ancho y alto
    tk.Label(ventana_variables_libres, text="Seleccione las variables sin límite:", 
             bg="black", fg="white", font=("Arial black", 12)).pack(pady=10)
    
    checkboxes = []
    variables_seleccionadas = []

    # Mostrar las variables disponibles (basado en el número de variables)
    for i in range(num_variables):
        var = tk.IntVar()  # Crea una IntVar para cada checkbox
        check = tk.Checkbutton(ventana_variables_libres, text=f"x{i+1}", variable=var, 
                               bg="black", fg="white", selectcolor="#4CAF50", 
                               font=("Arial black", 10))
        check.pack(anchor="w")
        checkboxes.append((check, var))  # Guarda el checkbox y su IntVar
    
    tk.Button(ventana_variables_libres, text="Confirmar", command=confirmar_variables_libres, 
              bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", 
              font=("Arial black", 9)).pack(pady=10)

def confirmar_variables_libres():
    global variables_sinLimite
    variables_sinLimite = [f"x{i+1}" for i, (check, var) in enumerate(checkboxes) if var.get() == 1]

    if not variables_sinLimite:
        messagebox.showerror("Error", "Debe seleccionar al menos una variable sin límite")
        return

    ventana_variables_libres.destroy()  # Cerrar la ventana de selección de variables
    confirmar_funcion_objetivo()  # Llamar al proceso principal después de confirmar las variables


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def mostrar_funcion_objetivo():
    global ventana_funcion
    global entradas_funcion
    global entradas_restricciones
    global operadores_restricciones
    global objetivo_var

    # Crear ventana secundaria para la función objetivo y restricciones
    ventana_funcion = tk.Toplevel(root)
    ventana_funcion.title("Simplex")
    ventana_funcion.geometry("600x400")
    ventana_funcion.configure(bg="black")

    # Sección de objetivo de la función
    tk.Label(ventana_funcion, text="¿Cuál es el objetivo de la función?", bg="black", fg="white", font=("Arial black", 12)).pack(pady=8)
    objetivo_var = tk.StringVar(value="Maximizar")
    ttk.Combobox(ventana_funcion, textvariable=objetivo_var, values=["Maximizar", "Minimizar"]).pack()

    # Crear sección de función objetivo
    tk.Label(ventana_funcion, text="Función:", bg="black", fg="white", font=("Arial black", 12)).pack(pady=8)
    frame_funcion = tk.Frame(ventana_funcion, bg="black")
    frame_funcion.pack(pady=10)

    entradas_funcion = []
    for i in range(num_variables):
        entrada_coeficiente = tk.Entry(frame_funcion, width=5, bg="white", fg="black")
        entrada_coeficiente.grid(row=0, column=3 * i, padx=5, pady=5)  # Ajuste de espacio
        entradas_funcion.append(entrada_coeficiente)
        tk.Label(frame_funcion, text=f"x{i+1}", bg="black", fg="white", font=("Arial black", 9)).grid(row=0, column=3 * i + 1, padx=5, pady=5)

        if i < num_variables - 1:
            tk.Label(frame_funcion, text="+", bg="black", fg="white", font=("Arial black", 12)).grid(row=0, column=3 * i + 2)

    # Sección de restricciones
    tk.Label(ventana_funcion, text="Restricciones:", bg="black", fg="white", font=("Arial black", 12)).pack(pady=8)
    frame_restricciones = tk.Frame(ventana_funcion, bg="black")
    frame_restricciones.pack(pady=10)

    entradas_restricciones = []
    operadores_restricciones = []
    
    for i in range(num_restricciones):
        fila = []
        for j in range(num_variables):
            entrada_coeficiente = tk.Entry(frame_restricciones, width=5, bg="white", fg="black")
            entrada_coeficiente.grid(row=i, column=3 * j, padx=5, pady=5)  # Ajuste de espacio
            fila.append(entrada_coeficiente)
            tk.Label(frame_restricciones, text=f"x{j+1}", bg="black", fg="white", font=("Arial black", 12)).grid(row=i, column=3 * j + 1, padx=5, pady=5)
            
            if j < num_variables - 1:
                tk.Label(frame_restricciones, text="+", bg="black", fg="white", font=("Arial black", 12)).grid(row=i, column=3 * j + 2)

        # Combo box para el operador
        operador = ttk.Combobox(frame_restricciones, values=["≤", "≥", "="], width=3, state="readonly")
        operador.grid(row=i, column=3 * num_variables, padx=2, pady=2)
        operadores_restricciones.append(operador)

        # Campo para el valor de la restricción
        entrada_valor = tk.Entry(frame_restricciones, width=5, bg="white", fg="black")
        entrada_valor.grid(row=i, column=3 * num_variables + 1, padx=5, pady=5)
        fila.append(entrada_valor)

        entradas_restricciones.append(fila)

    # Botón para confirmar
    tk.Button(ventana_funcion, text="Confirmar", command=seleccionar_metodo_resolucion, 
              bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white", font=("Arial black", 9)).pack(pady=10)

    # Botón para regresar
    tk.Button(ventana_funcion, text="Regresar", command=regresar_a_principal, 
              bg="#f44336", fg="white", activebackground="#e60000", activeforeground="white", font=("Arial black", 9)).pack(pady=10)

    

# ===============================================================================================
#                                     confirmar_funcion_objetivo
# ===============================================================================================

def confirmar_funcion_objetivo():
    global funcion
    global rest_inicial  
    global conLimite  
    global reservaObjetivo  
    global list_secundaria
    global restricciones_finales
    global variables_sinLimite
    global sinLimite
    global list_xSinLimite
    global list_secundariaSL
    try:
        coeficientes = [float(entry.get()) for entry in entradas_funcion]
        restricciones = []

        # Formatear y guardar las restricciones
        for i, fila in enumerate(entradas_restricciones):
            coeficientes_restriccion = [float(entry.get()) for entry in fila[:-1]]
            valor_restriccion = fila[-1].get()
            operador = operadores_restricciones[i].get()

            # Convertir ≤ a <= y ≥ a >=
            if operador == "≤":
                operador = "<="
            elif operador == "≥":
                operador = ">="

            # Crear la expresión para la restricción
            restriccion_str = " + ".join([f"{coef}*x{j+1}" for j, coef in enumerate(coeficientes_restriccion)])
            restriccion_str += f" {operador} {valor_restriccion}"
            restricciones.append(restriccion_str)

        # Convertir la función objetivo
        funcion_objetivo = " + ".join([f"{coef}*x{i+1}" for i, coef in enumerate(coeficientes)])
        objetivo = objetivo_var.get()

        # Determinar si es maximización o minimización
        if objetivo == "Maximizar":
            funcion = f"max z = {funcion_objetivo}"
        else:
            funcion = f"min z = {funcion_objetivo}"
        restricciones_list = []
        # Mostrar la función objetivo y restricciones
        print("Función objetivo:", funcion)
        #------------------------------------------
        #para variables negativas con límite inferior
        for restriccion in restricciones:
            print(restriccion)
            rest_inicial += [restriccion]
            print( rest_inicial)
        #revisa si hay restricciones con las condiciones de variables negativas con límite inferior
        list_secundaria = revisar_rest_conLimite(rest_inicial)
        #print(list_secundaria)
        # Si hay variables con límites, transformar la función objetivo
        if conLimite == 1:
            funcion = transformar_funcion_ConLimite(funcion)
            print("Función objetivo transformada:", funcion)
            print("Constante almacenada en reservaObjetivo:", reservaObjetivo)
            list_secundaria = [reemplazar_enRestriccion_variable(rest) for rest in list_secundaria]
            for rest in list_secundaria:
                print("Restricciones transformadas:", rest)
            for rest in list_secundaria:
                restriccion = transformar_rest_conLimite(rest)
                restricciones_finales += [restriccion]
            for restriccion in restricciones_finales:
                restriccion = transformar_inecuacion(restriccion)
                restricciones_list += [restriccion]
                print("restricion de inecuacion",restriccion)
            print("restricciones list",restricciones_list )
            contar_variables(funcion,restricciones_list)
            for restriccion in restricciones_list:
                add_rest(restriccion)  # Enviar restricción a add_rest en basic_func_simplex
            print("funcion entrada",funcion)
            # Enviar la función objetivo a transformar_ecuacion en basic_func_simplex
            funcion = transformar_ecuacion(funcion)
            print("funcion de transformar_ecuacion",funcion )

            # Crear la matriz usando las restricciones y función objetivo
            create_matrix(funcion)
        elif sinLimite == 1:
            # Obtener los reemplazos de las variables sin límite
            a = obtener_reemplazosSinLimite(variables_sinLimite, restricciones)
            print("\nPOR REEMPLAZAR X:\n", a)
            print("\nrestricciones originales:\n", restricciones)
            print("\nFunción objetivo antes:\n", funcion)
            funcion = transformar_funcionObjetivo(funcion)
            print("\nFunción objetivo transformada sin limite:\n", funcion)
            for restriccion in restricciones:
                nuevasRestriccionesSL = reemplazar_enRestriccion_variableSinLimite(restriccion)
                list_secundariaSL.append(nuevasRestriccionesSL)
            for rest in list_secundariaSL:
                print("Restricciones con reemplazo SL:", rest)
            for rest in list_secundariaSL:
                rest2 = transformar_rest_sinLimite(rest)
                restricciones_finales.append(rest2)
                # Imprimir las restricciones finales transformadas
            for restriccion in restricciones_finales:
                print("\nRestricción sin límite final:\n", restriccion)
            for restriccion in restricciones_finales:
                restriccion = transformar_inecuacion(restriccion)
                restricciones_list += [restriccion]
                print("restricion de inecuacion",restriccion)
            print("restricciones list",restricciones_list )
            contar_variables(funcion,restricciones_list)
            for restriccion in restricciones_list:
                add_rest(restriccion)  # Enviar restricción a add_rest en basic_func_simplex
            print("funcion entrada",funcion)
            # Enviar la función objetivo a transformar_ecuacion en basic_func_simplex
            funcion = transformar_ecuacion(funcion)
            print("funcion de transformar_ecuacion",funcion )

            # Crear la matriz usando las restricciones y función objetivo
            create_matrix(funcion)
            
        else:
            print("No hay variables con límite inferior.")
            for restriccion in restricciones:
                restriccion = transformar_inecuacion(restriccion)
                restricciones_list += [restriccion]
                print(restriccion)
            contar_variables(funcion,restricciones_list)
            for restriccion in restricciones_list:
                add_rest(restriccion)  # Enviar restricción a add_rest en basic_func_simplex
           
            # Enviar la función objetivo a transformar_ecuacion en basic_func_simplex
            funcion = transformar_ecuacion(funcion)
            print("funcion transformada",funcion)
            # Crear la matriz usando las restricciones y función objetivo
            create_matrix(funcion)
        #------------------------------------------
        # Llamar a la función simplex al final
        simplex(matrix)
        ventana_funcion.destroy()

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos para los coeficientes")



def continuar():
    global num_variables
    global num_restricciones
    
    try:
        num_variables = int(entry_variables.get())
        num_restricciones = int(entry_restricciones.get())
        if num_variables <= 0 or num_restricciones < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingrese números enteros positivos válidos")
        return

    root.withdraw()  # Ocultar la ventana principal
    mostrar_funcion_objetivo()

def salir():
    if messagebox.askyesno("Confirmar", "¿Está seguro que desea salir?"):
        root.destroy()

def regresar_a_principal():
    ventana_funcion.destroy()
    root.deiconify()  # Mostrar la ventana principal de nuevo


# Ruta de la imagen
image_path = os.path.join("images", "cerebro2.png")

# Crear la ventana principal
root = tk.Tk()
root.title("Simplex")
root.geometry("600x600")
root.configure(bg="#000000")  # Cambia el color de fondo de la ventana principal
# Deshabilitar el redimensionamiento horizontal y vertical
root.resizable(False, False)  # False para ancho y alto
# Mostrar la imagen en la ventana principal
try:
    img = Image.open(image_path)  # Abrir la imagen
    img = img.resize((200, 200))  # Redimensionar la imagen si es necesario
    img_tk = ImageTk.PhotoImage(img)  # Convertir a formato compatible con Tkinter
    img_label = tk.Label(root, image=img_tk, bg="black")  # Asegúrate de que el fondo de la etiqueta coincida
    img_label.pack(pady=10)
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# Crear los campos de entrada para el número de variables y restricciones
tk.Label(root, text="¿Cuántas variables de decisión tiene el problema?", bg="black", fg="white", font=("Arial black", 12)).pack(pady=8)
entry_variables = tk.Entry(root, validate="key", width=10, font=("Arial", 13))  # Cambia 30 al ancho deseado
entry_variables.pack(pady=10)
entry_variables.config(validate="key", validatecommand=(root.register(validar_entero_positivo), "%P"))

tk.Label(root, text="¿Cuántas restricciones?", bg="black", fg="white", font=("Arial black", 12)).pack(pady=8)
entry_restricciones = tk.Entry(root, validate="key", width=10, font=("Arial", 13))
entry_restricciones.pack(pady=10)
entry_restricciones.config(validate="key", validatecommand=(root.register(validar_entero_positivo), "%P"))

# Botón para continuar
continuar_boton = tk.Button(root, text="Continuar", command=continuar, bg="#4CAF50", fg="white", activebackground="#45a049", font=("Arial black", 11))
continuar_boton.pack(pady=20)

# Botón para salir con confirmación
salir_boton = tk.Button(root, text="Salir", command=salir, bg="#f44336", fg="white", activebackground="#e60000", font=("Arial black", 11))
salir_boton.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()