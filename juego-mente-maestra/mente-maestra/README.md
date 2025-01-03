                                                       
# Tarea Programada 2: El Juego de Mente Maestra

## **Realizado por:**
**Angélica Díaz Barrios**   
                                                  
## **Descripción General**
Este programa implementa el clásico juego de **Mente Maestra** en **Prolog**, como parte del curso de **Lenguajes de Programación**. Permite al jugador interactuar con dos modos de juego:

1. **La computadora vs. usted**: La computadora genera una secuencia aleatoria y el jugador intenta adivinarla.
2. **Usted vs. la computadora**: El jugador define una secuencia y la computadora intenta adivinarla.

En ambos casos, el objetivo es adivinar la secuencia en un máximo de **10 intentos**.

El juego utiliza secuencias de 4 números, donde:
- Los valores pueden variar entre **1 y 6**.
- Los números pueden repetirse dentro de la secuencia.


INSTRUCCIONES:

1. Para comenzar el juego deberá abrir SWI-Prolog.

2. Dirigirse a la barra superior del menú y escoger la opción "File" ->
   Consult, esto le abrirá el directorio para que seleccione el archivo 
   que contiene el código fuente en este caso se llama "tareaProlog".

3. Una vez seleccionado y cargado el archivo, en la ventana de ejecución,
   deberá escribir "inicio." y dar clic en enter.

4. Se le solicitará que ingrese su nombre, podrá escribirlo sin caracteres
   especiales preferiblemente, no es necesario que coloque un punto al finalizar
   el nombre. Nuevamente hace clic en enter para guardar su nombre.

5. Se le desplegará un menú con 5 opciones:

    1. Jugar: la maquina escoge una configuracion aleatoria, usted adivina     
    2. Jugar: usted escoge una configuracion aleatoria y la maquina adivina    
    3. Ver tabla de mejores puntajes                                          
    4. Iniciar juego con otro usuario                                          
    5. Salir                                                                   


   Deberá ingresar el número de la opción que desea realizar, NO es necesario
   que ingrese un punto al final del número solo haga clic en enter.

6. Si seleccionó la opción 1, la máquina escogerá una secuencia aleatoria y usted 
   tendrá que ir adivinando la posible secencia, para ello deberá escribir una lista
   con 4 valores con números del 1 al 6, por ejemplo: "[1,2,4,5].", de esa forma se     
   ingresa la lista al juego, los números deberán estar entre corchetes cuadrador y 
   separados por comas sin espacios adicionales y con punto al final del corchete 
   de cierre (sin comillas). Deberá hacer clic en enter y el sistema le mostrará 
   el número de intentos que lleva, los números que son correctos y la cantidad de
   posiciones que son correctas. Continúa ingresando listas hasta que logre adivinar
   la secuencia cuando los valores correctos y las posiciones correctas sean 4.

7. Solo dispone de 10 intentos.

8. Se guardarán los nombres y el puntaje de los jugadores que adivinen en menos intentos.

9. Con la opción 3 podrá ver dicha tabla de puntajes.

10.Con la opción 2, usted escoge una secuencia para que la máquina adivide, la lista 
   deberá ser ingresada como se muestra en el paso 6, entre corchetes con 4 valores
   separados por comas y con un punto al final. Hacer clic en enter y la máquina 
   procederá a adivinar.

   La máquina le hará una serie de preguntas y usted deberá responder con: s. (para Sí) o n.
   (para No).

   En este caso la respuesta es en minúscula y debe llevar un punto al final, luego deberá hacer Enter.
   
   Ejemplo:

  Opcion: 
|: 2
Ingrese una lista de numeros : 
|: [2,3,4,5].

Â¿Es [2,6,5,2] (Si/No)? |: n.

Â¿Cuantos estan correctos en valor y posicion? |: 1.

Â¿Cuantos estan correctos solo en valor? |: 2.

Â¿Es [3,6,3,2] (Si/No)? |: n.

Â¿Cuantos estan correctos en valor y posicion? |: 0.

Â¿Cuantos estan correctos solo en valor? |: 2.

Â¿Es [2,6,3,6] (Si/No)? |: n.

   
   Usted responde según lo que aparezca en la secuencia que usted ingresó.
   

11.Con la opción 4 del menú usted podrá jugar con otro usuario, es decir ingresa el 
   nuevo nombre de usuario.

12. Y la opción 5 del menú, cerrará por completo el juego y la ventana de ejecución.


NOTA: CUANDO SE ABRE DIRECTAMENTE EL ARCHIVO DE MEJORES PUNTAJES.TXT SE VE VACÍO,
      PERO LOS PUNTAJES SÍ SE GUARDAN EN DISCO Y SI EL JUEGO SE CIERRA, PERSISTEN
      LOS DATOS, PUEDE COMPROBARLO JUGANDO Y TRATAR DE OBTENER UN BUEN PUNTAJE
      LUEGO EN EL MENÚ SELECCIONA LA OPCIÓN 3 Y VERÁ EL NOMBRE DEL USUARIO
      CON SU PUNTAJE, SI CIERRA EL PROGRAMA Y LO VUELVE A EJECUTAR Y SELECCIONA
      INICIALMENTE LA OPCIÓN 3, NOTARÁ QUE SE MUESTRAN LOS O EL USUARIO CON SU
      MEJOR PUNTUACIÓN.



