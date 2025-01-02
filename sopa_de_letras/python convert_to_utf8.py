#LIBRERÍAS
import csv #Se importa el módulo cvs para importar o exportar hojas de cálculo o base de datos
import time #Se importa el módulo time para poder utilizar el cronómetro
from tkinter import *#Se importa el módulo tkinter para poder crear una interfaz gráfica
from tkinter import messagebox#Se importa el widget messabox con el fin de poder mostrar mensajes al usuario
from PIL import ImageTk, Image#Se importa la librería PiL con el fin de obtener una mejor interfaz con imágenes
from googletrans import Translator#Se importa googletrans con el fin de cambiar el idioma de español a inglés y viceversa
from datetime import datetime#Se importa el módulo datatime con el fin de utilizar el cronómetro
import pygame#Se importa la librería Pygame con el fin de utilizar sus eventos 
import random as random#Se importa el módulo random con el fin de mezclar letras y palabras de manera aleatoria


"""
Nombre de la clase: InterfazPrincipal

Entrada del constructor: recibe la ventana raíz llamada interfaz_principal

Salidas: retorna a los diferentes métodos, según el evento que sea escogido

Métodos:
1.actualizacion_tiempo
2.lenguaje
3.modos_de_juego
4.nivel_de_juego
5.modo_principiante
6.modo_intermedio
7.modo_avanzado
8.destruir_interfaz_principal
Restricciones: no hay
"""

class InterfazPrincipal:#Clase principal donde se forma la ventana de inicio 
	global palabra_a_buscar #Variable global para buscar las palabras en la sopa de letras
	palabra_a_buscar = "" #Se realizó de esta forma porque el parametro "event" de los botones no admite el "self"
	global lista_de_eventos
	lista_de_eventos=[]
	global posicion_palabras
	posicion_palabras=[]
	def __init__(self, interfaz_principal):#Constructor de la ventana de inicio con sus debidos botones
		self.palabras_aleatorias=[]
		self.jugador = 0
		self.modo = 0 #Cero es Básico, 1 es Con Reloj, 2 es Contra Reloj.
		self.lenguajes = 0 #Cero es Español y 1 es Inglés.
		self.contador_de_palabras_encontradas=0 #Se realizó de esta forma porque el parametro "event" de los botones no admite el "self"
		self.interfaz_principal = interfaz_principal
		interfaz_principal.resizable(0,0)
		interfaz_principal.iconbitmap("./IMAGENES/ICONO-BMP.ico")
		interfaz_principal.title("SOPA DE LETRAS")
		interfaz_principal.config(bg = "brown")
		#Fondo de la Interfaz Principal
		self.fondo_interfaz_principal = Label(interfaz_principal, image = fondo, bg = "black")
		self.fondo_interfaz_principal.pack(side = "right")
		self.hora=Label(bg = "black", foreground = "white", relief="flat",text=time.strftime('%I:%M:%S %p'),font=('Calibri',12,"bold"))
		self.hora.place(x = 500, y = 1)
	        
		#Nombre:actualizacion_tiempo
		#Entradas: no recibe ninguna entrada directamente, llama a la ventana interfaz_principal
		#Salidas: método que permite mostrar la hora en la interfaz principal
		#Restricciones: no hay
		def actualizacion_tiempo():#Método para mostrar la hora en la interfaz
			try:
				self.contador_tiempo = time.strftime('%I:%M:%S %p')
				while self.hora['text']!=self.contador_tiempo:
					self.hora['text']=self.contador_tiempo
				self.interfaz_principal.after(1000, actualizacion_tiempo)
			except:
				pass
		#Etiquetas principales del idioma
		self.etiquetaIdioma = Label(interfaz_principal)
		self.etiquetaIdioma.config(bg = "black", text = "IDIOMAS", font = ("Calibri", 19, "bold"), foreground = "gold")
		self.etiquetaIdioma.place(x=245, y=10)
		self.cambiar_lenguaje_es = Label(interfaz_principal)
		self.cambiar_lenguaje_es.config(bg = "black", text = "Inglés", font = ("Calibri", 12, "bold"), width = 14, foreground = "blue", relief="raised")
		self.cambiar_lenguaje_es.place(x=160, y=70)
		self.cambiar_lenguaje_en = Label(interfaz_principal)
		self.cambiar_lenguaje_en.config(bg = "black", text = "Español", font = ("Calibri", 12, "bold"), width = 14, foreground = "blue", relief="raised")
		self.cambiar_lenguaje_en.place(x=310, y=70)
		self.salir = Button(interfaz_principal)
		self.salir.config(bg = "red", text = "Salir", font = ("Calibri", 14, "bold"), width = 5, foreground = "black", relief="raised", command=quit)
		self.salir.place(x=260, y=570)
		
		
		
		#Llamada para actualizar el tiempo
		actualizacion_tiempo()

	        #Nombre: lenguaje
		#Entradas: recibe la palabra event, que es cuando el usuario seleccionó un idioma en la interfaz principal
		#Salidas: método que permite destruir las etiquetas y botones que estaban en la interfaz, para lograr
		#mostrar las otras etiquetas y botones de los métodos de juego
		#Restricciones: no hay
		#Función de los botones
		def lenguaje(event):#Método para cambiar los lenguajes
			#Destruyendo botones de idioma
			self.cambiar_lenguaje_es.destroy()
			self.cambiar_lenguaje_en.destroy()
			self.etiquetaIdioma.destroy()
			self.boton_es.destroy()
			self.boton_en.destroy()
			boton_de_accion = str(event.widget)
			#Construyendo nueva interfaz, sin destruir la principal
			#Automáticamente carga en español
			self.modo_de_juego = Label(interfaz_principal)
			self.modo_de_juego.config(bg = "black", text = "Modos de Juego", font = ("Calibri", 18, "bold"), foreground = "white")
			self.modo_de_juego.place(x=240, y=25)
			self.boton_basico = Button(image = basico, text = "Modo Básico", activebackground = "cyan", activeforeground = "red")
			self.boton_basico.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.boton_basico.place(x = 100, y = 70)
			self.boton_basico.bind("<Button-1>", modos_de_juego)
			self.boton_reloj = Button(text = "Con Tiempo", image = reloj, width = 111, activebackground = "cyan", activeforeground = "red")
			self.boton_reloj.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.boton_reloj.place(x = 250, y = 70)
			self.boton_reloj.bind("<Button-1>", modos_de_juego)
			self.boton_contra_reloj = Button(text = "Contra Reloj", image = contra_reloj, width = 111, activebackground = "cyan", activeforeground = "red")
			self.boton_contra_reloj.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.boton_contra_reloj.place(x = 400, y = 70)
			self.boton_contra_reloj.bind("<Button-1>", modos_de_juego)
			#Entonces se valida el botón clickeado para cambiar el idioma a inglés
			if boton_de_accion == ".!button2":
				self.lenguajes = 1
				self.modo_de_juego.config(text = "Game Mode")
				self.boton_basico.config(text = "Basic Mode")
				self.boton_reloj.config(text = "With Clock")
				self.boton_contra_reloj.config(text = "Against The Clock")
		#Nombre: modos_de_juego
		#Entradas: recibe la palabra event, que es el evento cuando el usuario seleccionó un modo de juego
		#Salidas: alamacena el modo de juego escogido por el usuario, destruye las etiquetas de modo y muestra las etiquetas
		#y botones de los niveles de juego
		#Restricciones: no hay
		#Funcion de validación para los modos de juego
		def modos_de_juego(event):#Método para cambiar los modos de juego
			boton_de_accion = str(event.widget)
			if boton_de_accion == ".!button4":
				self.modo = 0
			if boton_de_accion == ".!button5":
				self.modo = 1
			if boton_de_accion == ".!button6":
				self.modo = 2
			#Destruyendo los botones anteriores
			self.modo_de_juego.destroy()
			self.boton_basico.destroy()
			self.boton_reloj.destroy()
			self.boton_contra_reloj.destroy()
			#Iniciando el menú nuevo de las dificultades de juego
			self.tipo_de_jugador = Label(interfaz_principal)
			self.tipo_de_jugador.config(bg = "black", text = "Niveles de Juego", font = ("Calibri", 18, "bold"), foreground = "white")
			self.tipo_de_jugador.place(x=250, y=25)
			self.jugador_principiante = Button(text = "Principiante", image = principiante, width = 111, activebackground = "cyan", activeforeground = "red")
			self.jugador_principiante.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.jugador_principiante.place(x = 120, y = 70)
			self.jugador_principiante.bind("<Button-1>", nivel_de_juego)
			self.jugador_intermedio = Button(text = "Intermedio", image = intermedio, width = 111, activebackground = "cyan", activeforeground = "red")
			self.jugador_intermedio.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.jugador_intermedio.place(x = 250, y = 70)
			self.jugador_intermedio.bind("<Button-1>", nivel_de_juego)
			self.jugador_avanzado = Button(text = "Avanzado", image = avanzado, width = 111, activebackground = "cyan", activeforeground = "red")
			self.jugador_avanzado.config(font=("Calibri", 11, "bold"),borderwidth=2, width=111, relief="raised", compound="top")
			self.jugador_avanzado.place(x = 380, y = 70)
			self.jugador_avanzado.bind("<Button-1>", nivel_de_juego)
			if self.lenguajes == 1:
				self.tipo_de_jugador.config(text = "Player Level")
				self.jugador_principiante.config(text = "Newbie")
				self.jugador_intermedio.config(text = "Intermedium")
				self.jugador_avanzado.config(text = "Advanced")
			#Leyendo el documento a utilizar para las palabras aleatorias
			documento = open("Diccionario.txt","r")
			self.documento_leido = documento.readlines()
			documento.close()
		#Nombre:nivel_de_juego
		#Entradas: recibe la palabra event, que es el evento cuando el usuario seleccionó un nivel de juego
		#Salidas: alamcena el nivel de juego seleccionado por el usuario para ser tomado en cuenta en la
		#creación de la cuadrícula de la soa de letras
		#Restricciones: no hay
		def nivel_de_juego(event):#Método para seleccionar el nivel de juego 
			self.boton_de_accion = str(event.widget)
			if self.boton_de_accion == ".!button7":
				modo_principiante(self)
			if self.boton_de_accion == ".!button8":
				self.jugador = 1
				modo_intermedio(self)
			if self.boton_de_accion == ".!button9":
				self.jugador = 2
				modo_avanzado(self)
		#Nombre: modo_principiante
		#Entradas: no recibe una entrada directamente
		#Salidas: crea una Listbox con las letras que están en la hoja de cálculo de Excel llamada PRINCIPIANTE
		# y las palabras que están en el archivo "Diccionario.txt"
		#Restricciones: La cuadrícula tendrá dimensiones de 12 filas y 12 columnas.
		#Adicionalmente, la cantidad de palabras a encontrar serán 6 

		def modo_principiante(self):
			self.lista_palabras = Listbox(self.fondo_interfaz_principal)
			self.lista_palabras.config(font = ("Calibri", 11, "bold"), relief = "raised", width = 25, height = 20)
			self.lista_palabras.place(x = 0, y = 100)
			self.matriz = "./CUADRICULAS/PRINCIPIANTE.csv"
			self.interfaz_principal.geometry("520x320")
			#Creando un generador de palabras aleatorias
			self.palabras_aleatorias = random.sample([self.documento_leido[x].upper() for x in range(1,len(self.documento_leido))],6)
			self.lista_palabras.config(font = ('Calibri',8,"bold"), width = 15, height = 15)
			destruir_interfaz_principal(self)
		#Nombre: modo_intermedio
		#Entradas: no recibe una entrada directamente
		#Salidas:crea una Listbox con las letras que están en la hoja de cálculo de Excel llamada INTERMEDIO
		# y las palabras que están en el archivo "Diccionario.txt"
		#Restricciones:  La cuadrícula tendrá dimensiones de 20 filas y 20 columnas. Por otra parte, 
                #la cantidad de palabras a encontrar serán 10 palabras 
		def modo_intermedio(self):
			self.lista_palabras = Listbox(self.fondo_interfaz_principal)
			self.lista_palabras.config(font = ("Calibri", 11, "bold"), relief = "raised", width = 20, height = 20)
			self.lista_palabras.place(x = 0, y = 100)
			self.matriz = "./CUADRICULAS/INTERMEDIO.csv"
			self.interfaz_principal.geometry("700x530")
			#Creando un generador de palabras aleatorias
			self.palabras_aleatorias = random.sample([self.documento_leido[x].upper() for x in range(1,len(self.documento_leido))],10)
			self.lista_palabras.config(font = ('Calibri',8,"bold"), width = 15, height = 25)
			destruir_interfaz_principal(self)
		#Nombre: modo_avanzado
		#Entradas: no recibe una entrada directamente
		#Salidas:crea una Listbox con las letras que están en la hoja de cálculo de Excel llamada AVANZADO
		# y las palabras que están en el archivo "Diccionario.txt"
		#Restricciones: : La cuadrícula tendrá dimensiones de 28 filas y 28 columnas. Además, la 
                #cantidad de palabras a encontrar serán 14. 
		def modo_avanzado(self):
			self.lista_palabras = Listbox(self.fondo_interfaz_principal)
			self.lista_palabras.config(font = ("Calibri", 11, "bold"), relief = "raised", width = 20, height = 20)
			self.lista_palabras.place(x = 0, y = 100)
			self.matriz = "./CUADRICULAS/AVANZADO.csv"
			self.interfaz_principal.geometry("900x750")
			#Creando un generador de palabras aleatorias
			self.palabras_aleatorias = random.sample([self.documento_leido[x].upper() for x in range(1,len(self.documento_leido))],14)
			destruir_interfaz_principal(self)
		#Nombre: destruir_interfaz_principal
		#Entradas: no recibe una entrada directamente
		#Salidas: destruye todo lo que estaba en la interfaz de nivel de juego
		#Restricciones: no existen
		def destruir_interfaz_principal(self):
			InterfazSecundaria.cuadricula(self)
			self.tipo_de_jugador.destroy()
			self.jugador_principiante.destroy()
			self.jugador_intermedio.destroy()
			self.jugador_avanzado.destroy()
			self.hora.destroy()
			self.salir.destroy()
			#CREANDO INTERFAZ DE JUEGO


		#Botones de idioma
		#Muestra las imágenes de las banderas en la ventana principal
		self.boton_es = Button(image = icono_en, width = 111, activebackground = "blue", highlightcolor = "green", relief="raised")
		self.boton_es.place(x = 160, y = 95)
		self.boton_es.bind("<Button-1>", lenguaje)
		self.boton_en = Button(image = icono_es, width = 111, activebackground = "blue", activeforeground = "green", relief="raised")
		self.boton_en.place(x = 310, y = 95)
		self.boton_en.bind("<Button-1>", lenguaje)

		
#CREANDO INTERFAZ
interfaz_principal = Tk()
#CARGANDO IMÁGENES EN INTERFAZ
icono_es = ImageTk.PhotoImage(Image.open("./IMAGENES/ICONO-ES.png"))
icono_en = ImageTk.PhotoImage(Image.open("./IMAGENES/ICONO-EN.png"))
fondo = ImageTk.PhotoImage(Image.open("./IMAGENES/fondo8.png"))
fondo_2 = ImageTk.PhotoImage(Image.open("./IMAGENES/2.png"))
basico = ImageTk.PhotoImage(Image.open("./IMAGENES/basico1.png"))
reloj = ImageTk.PhotoImage(Image.open("./IMAGENES/tiempo.png"))
contra_reloj = ImageTk.PhotoImage(Image.open("./IMAGENES/contraReloj.png"))
principiante = ImageTk.PhotoImage(Image.open("./IMAGENES/principiante1.png"))
intermedio = ImageTk.PhotoImage(Image.open("./IMAGENES/intermedio1.png"))
avanzado = ImageTk.PhotoImage(Image.open("./IMAGENES/avanzado1.png"))
mi_menu = Menu(interfaz_principal)
interfaz_principal.config(menu = mi_menu)
mi_menu.add_cascade(label="Ayuda")
mi_menu.add_command(label="Salir",command = quit)
#MANTENIENDO INTERFAZ
interfaz = InterfazPrincipal(interfaz_principal)





"""
Nombre de la clase: InterfazSecundaria

Entrada: recibe la InterfazPrincipal, es decir hereda la clase principal

Salidas: retorna a los diferentes métodos, según el evento que sea escogido

Métodos:
1.cuadricula
2.actualizacion_cronometro
3.matriz
4.acomodar
5.callback
6.buscador_de_palabras
7.modificar_lista_palabras
8.anticipar_direccion

Restricciones: no hay
"""
class InterfazSecundaria(InterfazPrincipal):#Clase heredada, donde se formará la interfaz secundaria
        #Nombre: cuadricula
	#Entradas: no recibe una entrada directamente
	#Salidas: monta las palabras en la listbox de manera aleatoria
	#Restricciones: no hay
	def cuadricula(self):#Método para formar la cuadrícula de botones
		if self.jugador==1:
			self.cronometro=Label(borderwidth=2,bg = "green", relief="sunken",width=20,height=3,text="Tiempo transcurrido: \n"+time.strftime('%M:%S'),font=('Arial',8,"bold"))
			self.cronometro.place(x=2,y=4)
		if self.jugador==2:
			self.cronometro=Label(borderwidth=2,bg = "green", relief="sunken",width=20,height=3,text="Tiempo restante: \n"+time.strftime('%M:%S'),font=('Arial',8,"bold"))
			self.cronometro.place(x=2,y=2)
		self.fondo_interfaz_principal.config(image = fondo_2, bg = "black")
		self.fondo_interfaz_principal.pack(fill = "both")
		self.label_de_cuadricula = Label(self.interfaz_principal)
		self.label_de_cuadricula.place(x = 200, y = 0)
		self.lista_palabras.place(x = 0,y = 80)
		#ARMANDO LISTA CON LAS PALABRAS A BUSCAR
		palabra = []
		for x in self.palabras_aleatorias:
			#MONTANDO LAS PALABRAS EN LA LISTBOX
			self.lista_palabras.insert(0,self.palabras_aleatorias[0][:-1])
			palabra.append(self.palabras_aleatorias[0][:-1])
			self.palabras_aleatorias = self.palabras_aleatorias[1:]
		return InterfazSecundaria.matriz(self,palabra)
	#Nombre: actualizacion_cronometro
	#Entradas: no recibe una entrada directamente
	#Salidas: crea el cronómetro autilizar
	#Restricciones: no hay
	def actualizacion_cronometro():#Método para crear el cronometro
	    #Contador de tiempo en la interfaz principal
		try:
			self.contador_tiempo = time.strftime('%M:%S')
			while self.cronometro['text']!="5:00":
				self.cronometro['text'] = self.contador_tiempo
			self.fond.after(1000, actualizacion_cronometro)
		except:
			pass
	actualizacion_cronometro()
	#Nombre: matriz
	#Entradas: recibe la lista llamada palabra
	#Salidas: crea la matriz según el nivel de juego escogido
	#Restricciones: según el nivel de juego escogido
	def matriz(self,palabra):#Método para medir la matriz y formar una base para montar las palabras
		ancho_matriz = 0 #ANCHO MATRIZ
		largo_matriz = 0 #LARGO MATRIZ
		archivo = open(self.matriz)
		datos_matriz = csv.reader(archivo, delimiter=";")
		for lineas in datos_matriz:
			largo_matriz+=1
			for columnas in lineas:
				pass
			ancho_matriz+=1
		return InterfazSecundaria.acomodar(self,ancho_matriz,largo_matriz,palabra)
	#Nombre: acomodar
	#Entradas: recibe los parámetros ancho_matriz, largo_matriz, palabra
	#Salidas: acomoda correcatmente las palabras dentro de la matriz creada, lo hace de manera aleatoria
	#Las palabras pueden ubicarse de forma horizontal (de izquierda a derecha o de derecha a izquierda),
	#vertical (de arriba hacia abajo o de abajo hacia arriba) y en diagonal.
	#Restricciones: segúm las dimesiones de la matriz, no podrá acomodrase palabras de forma que no se
	#puedan posicionar dentro de la matriz
	def acomodar(self,ancho_matriz,largo_matriz,palabra): #Método para formar la matriz con letras aleatorias siempre
		global palabras_aleatorias
		palabras_aleatorias=palabra
		self.palabras_aleatorias=palabras_aleatorias #Estas van a ser las palabras aleatorias que se colocarán en la matriz
		matriz_csv = [] #ESTA VA A SER LA MATRIZ QUE VAMOS A MODIFICAR
		elementos_matriz = [] #ESTOS SON LO ELEMENTOS MODIFICADOS QUE VAMOS A METER EN LA MATRIZ
		alfabeto = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		e=25 #ESTE ES EL CONTADOR DE LAS PALABRAS ALEATORIAS
		contador_largo_filas = 0 
		self.posicion_palabras = posicion_palabras
		archivo = open(self.matriz)
		datos_matriz = csv.reader(archivo, delimiter=";")
		for i in datos_matriz:
			for m in i:
				while e > 0:
					e -= 1
					aleatorio = random.randint(0,25)#AQUI SACAMOS UN NÚMERO ALEATORIO
					letras_aleatorias = alfabeto[aleatorio] #AQUÍ SACAMOS LA PALABRAS ALEATORIAS
				e=25
				contador_largo_filas += 1
				elementos_matriz.append(letras_aleatorias)
			if contador_largo_filas == ancho_matriz:
				matriz_csv.append(elementos_matriz)
				elementos_matriz = []
				contador_largo_filas = 0
		try:
			#Mientras la lista de palabras a colocar en la matriz no se encuentre vacía, no se detendra el ciclo
			while palabra != []:
				for recorrer in range(1):
					largo_de_palabra = len(palabra[0])
					#ESTO ES PARA MONTAR LAS PALABRAS EN LA MATRIZ
					#Definiendo las filas y columnas a modificar
					columna_aleatoria = random.randint(0,ancho_matriz-largo_de_palabra)
					fila_aleatoria = random.randint(0,largo_matriz-largo_de_palabra)
					#Recorrer la palabra letra por letra
					modos_de_acomodar = random.randint(1,8)
					if (modos_de_acomodar==1): #manera 1 HORIZONTAL DERECHA
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								columna_aleatoria+=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==2):   #MANERA DE ACOMODAR 2 HORIZONTAL IZQUIERDA
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								columna_aleatoria-=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==3):   #MANERA DE ACOMODAR 3 VERTICAL ARRIBA
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria-=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==4):   #MANERA DE ACOMODAR 4 VERTICAL ABAJO
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria+=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==5):   #MANERA DE ACOMODAR 5 DIAGONAL IZQUIERDA ABAJO
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria-=1
								columna_aleatoria-=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==6):   #MANERA DE ACOMODAR 6 DIAGONAL IZQUIERDA ARRIBA
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria+=1
								columna_aleatoria-=1						
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue					
					if (modos_de_acomodar==7):   #MANERA DE ACOMODAR 6 DIAGONAL DERECHA ARRIBA
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria-=1
								columna_aleatoria+=1						
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
					if (modos_de_acomodar==8):   #MANERA DE ACOMODAR 8 DIAGONAL DERECHA ABAJO
						#ESTO ES PARA MODIFICAR LA MATRIZ Y VALIDACIONES
						if InterfazSecundaria.anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz)==False:
							for recorrido_letra in range(largo_de_palabra):
								fila_aleatoria+=1
								columna_aleatoria+=1
								matriz_csv[fila_aleatoria][columna_aleatoria]=palabra[0][recorrido_letra]
								posicion_palabras.append([fila_aleatoria,columna_aleatoria])
							palabra=palabra[1:]
							continue
						else:
							modos_de_acomodar = random.randint(1,8)
							continue
				#Escribiendo los datos en el csv despues de modificarlos
				archivo = open(self.matriz,"w",newline = '\n')
				writer = csv.writer(archivo,delimiter = ";")
				writer.writerows(matriz_csv)
				archivo.close()
		except Exception as e:
			print("No se pudo crear la matriz",e)
		#Procedo a crear la matriz de botones
		contador_lineas = 0
		contador_columnas = 0
		# Leyendo la matriz
		Matriz = open(self.matriz)
		# Delimitando por ";" el contenido de dicha matriz
		contenido = csv.reader(Matriz, delimiter=";")
		# Realizando los recorridos por las filas y columnas
		for lineas in contenido:
			for columnas in lineas:
			# Utilizando iteración para cargar imágenes de manera aleatoria en el mapa
				if columnas != "":  # Cuadras
					self.botones=Button(self.label_de_cuadricula, text = columnas, command=lambda:InterfazSecundaria.modificar_lista_palabras(self))
					self.botones.config(width=2, height=0, bg="white", relief = "flat")
					self.botones.grid(row=contador_lineas, column=contador_columnas)
					self.botones.bind("<ButtonRelease>", InterfazSecundaria.callback)
				contador_columnas += 1
			contador_lineas += 1
			contador_columnas = 0
	#Nombre: callback
	#Entradas: recibe la palabra event, que es el evento sobre los botones según los clicks 
	#Salidas: captura los clicks de los botones para ir formando la palabra encontrada en la matriz
	#Restricciones: la palabra que se forme con los clicks de los botones deberá estar en la listbox
	#de palabras a buscar
	def callback(event):#Método para capturar los click sobre los botones de la cuadrícula
		global palabra_a_buscar
		global lista_de_eventos
		lista_de_eventos+=[event.widget]
		texto_boton = event.widget.cget("text")
		event.widget.config(bg = "red")
		# x =event.x_root - self.interfaz_principal.winfo_rootx()
		# y =event.y_root - self.interfaz_principal.winfo_rooty()
		# print(event.x,event.y,"----",event.widget.grid_location(x,y),"---",event.widget.grid_size())
		# print(posicion_palabras)
		palabra_a_buscar+=texto_boton
		palabra=InterfazSecundaria.buscador_de_palabras()
		if(palabra in palabras_aleatorias):
			for x in lista_de_eventos[:len(InterfazSecundaria.buscador_de_palabras())]:
				x.config(bg="green")
				lista_de_eventos=[]
	#Nombre: buscador_de_palabras
	#Entradas: busca las palabras en el juego
	#Salidas: retorna la palabra a buscar si se logró encontrar en la matriz
	#Restricciones: si se hacen más clicks de lo que posee el largo de la palabra con más letras,
        #entonces dará un mensje de error y volverá a poner los botones en blanco nuevamente
	def buscador_de_palabras():#Método para buscar las palabras en el juego
		global palabra_a_buscar
		global lista_de_eventos
		palabra_mas_larga=0
		for x in palabras_aleatorias:
			if len(x)>palabra_mas_larga:
				palabra_mas_larga=len(x)
		if len(palabra_a_buscar)>palabra_mas_larga:
			palabra_a_buscar=""
			messagebox.showerror(message= "Excedió el límite de carácteres que posee la palabra más larga de la lista", title="Límite de carácteres")
			for x in lista_de_eventos:
				x.config(bg="white")
				lista_de_eventos=[]
		if str(palabra_a_buscar) in palabras_aleatorias:
			return palabra_a_buscar
		else:
			return palabra_a_buscar
	#Nombre: modificar_lista_palabras
	#Entradas: no recibe una entrada directamente
	#Salidas: retorna un mensaje cuando el jugador haya encontrado todas las palbras
	#Restricciones:
	def modificar_lista_palabras(self):#Método para modificar la lista de las palabras encontradas en la matriz
		global palabra_a_buscar
		palabra=InterfazSecundaria.buscador_de_palabras()
		for x in range(len(list(self.lista_palabras.get(0,END)))):
			if self.contador_de_palabras_encontradas == len(list(self.lista_palabras.get(0,END))):
				messagebox.showinfo(message="GANÓ EL JUEGO EN: "+time.strftime('%M:%S'),title = "FELICITACIONES", )
			if str(self.lista_palabras.get(x)) == palabra:
				self.contador_de_palabras_encontradas+=1
				messagebox.showinfo(message= "Palabra encontrada con éxito", title="Palabra encontrada")
				palabra_a_buscar=""
				self.lista_palabras.itemconfigure(x,bg="red")
				return True
    
	#FUNCIÓN PARA PREDECIR DÓNDE SERÁ COLOCADA UNA PALABRA Y SABER SI SE ESTÁ COLOCANDO SOBRE OTRA
	#Nombre: anticipar_direccion
	#Entradas: modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz
	#Salidas: permite predecir dónde será colocada una palabra para saber si se está colocando sobre otra, retorna True si
	#las posiciones están correctas o False si no es así
	#Restricciones: las palbras a acomodar en la matriz no pueden caer sobre otras
	def anticipar_direccion(self,modos_de_acomodar,largo_de_palabra,posicion_palabras,fila_aleatoria,columna_aleatoria,largo_matriz,ancho_matriz):
		#Método para montar las palabras en la matriz, verificando que no quede fuera ninguna
		if (modos_de_acomodar==1):
			for x in range(largo_de_palabra):
				columna_aleatoria+=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==2):
			for x in range(largo_de_palabra):
				columna_aleatoria-=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==3):
			for x in range(largo_de_palabra):
				fila_aleatoria-=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==4):
			for x in range(largo_de_palabra):
				fila_aleatoria+=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==5):
			for x in range(largo_de_palabra):
				fila_aleatoria-=1
				columna_aleatoria-=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==6):
			for x in range(largo_de_palabra):
				fila_aleatoria+=1
				columna_aleatoria-=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==7):
			for x in range(largo_de_palabra):
				fila_aleatoria-=1
				columna_aleatoria+=1
				if[fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		if (modos_de_acomodar==8):
			for x in range(largo_de_palabra):
				fila_aleatoria+=1
				columna_aleatoria+=1
				if [fila_aleatoria,columna_aleatoria] in posicion_palabras:
					return True
				if(fila_aleatoria<0 or columna_aleatoria<0):
					return True
				if(fila_aleatoria>=largo_matriz or fila_aleatoria>=ancho_matriz):
					return True
				if(columna_aleatoria>=largo_matriz or columna_aleatoria>=ancho_matriz):
					return True
		return False
	    
interfaz_principal.mainloop()
