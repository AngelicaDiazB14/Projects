
% ...........................................................................................
% Tecnológico de Costa Rica
% Arquitectura de Computadores, GR 40
% Tarea Programada 2: El juego de mente maestra
% Realizado por: Angélica Díaz Barrios
%
% Este programa permite recibir el nombre del jugador al iniciar el juego, luego podrá escoger
% 2 Opciones de modo de juego, la computadora vs usted (la computadora le da una secuencia y
% usted adivina) y usted vs la computadora (usted le da una secuencia a la computadora y ella
% adivina) para ambos casos existe un límite de 10 intentos.
%
% El juego consiste en "batear" una lista de secuencia con 4 números, cuyos valores pueden
% ser úncamente del 1 al 6, en la secuencia los números pueden estar repetidos.
%.............................................................................................


% =====================================================================================
%                                     inicio
% =====================================================================================

inicio :-
    solicitarNombre,                              % Llama al predicado para solicitar el nombre del usuario
    menu.                                         % Llama al predicado para mostrar el menú del juego

% =====================================================================================
%                                 solicitarNombre
% =====================================================================================

solicitarNombre :-
    write(''), nl,
    write('.............................................................................'), nl,
    write('.                     BIENVENIDO AL JUEGO DE MENTE MAESTRA                  .'), nl,
    write('.                                                                           .'), nl,
    write('.............................................................................'), nl,
    write(''), nl,
    write('Ingrese su nombre, por favor: '),        % Solicita al usuario que ingrese su nombre
    read_line_to_string(user_input, Nombre), nl,    % Lee el nombre ingresado por el usuario
    format('¡Hola, ~w!~n', [Nombre]),               % Imprime un mensaje de saludo personalizado
    write(''), nl,
    assertz(nombre_usuario(Nombre)),!.              % Agrega el nombre del usuario a la base

:- dynamic nombre_usuario/1.                        % Depliega mensajes de saludo


% =====================================================================================
%                                        MENU
% =====================================================================================


menu :-
    write(''), nl,
    write('.............................................................................'), nl,
    write('.                                                                           .'), nl,
    write('.                                  MENU                                     .'), nl,
    write('.                                                                           .'), nl,
    write('.1. Jugar: la maquina escoge una configuracion aleatoria, usted adivina     .'), nl,
    write('.2. Jugar: usted escoge una configuracion aleatoria y la maquina adivina    .'), nl,
    write('.3. Ver tabla de mejores puntajes                                           .'), nl,
    write('.4. Iniciar juego con otro usuario                                          .'), nl,
    write('.5. Salir                                                                   .'), nl,
    write('.............................................................................'), nl,
    write(''), nl,
    write('Ingrese el numero de la opcion que desea realizar:                          '), nl,
    write(''), nl,
    write('Opcion: '),
    write(''), nl,

    read_line_to_string(user_input, OpcionStr),          % Lee la opción ingresada por el usuario
    (
    OpcionStr = "3" ->                                   % Verifica si la opción es "3"
        realizarOperacion(3)                             % Si la opción es "3", llama a realizarOperacion con el argumento 3
    ;
    (atom_number(OpcionStr, Opcion), integer(Opcion)) -> % Verifica si la opción es un número entero
        realizarOperacion(Opcion)                        % Si la opción es un número entero, llama a realizarOperacion con el argumento OpcionStr
    ;
        write(''), nl,
        write('Error: Opcion invalida.'), nl,            % Si la opción no es un número entero, muestra un mensaje de error
        menu                                             % Y regresa al menú
    ).


% =====================================================================================
%                                 realizarOperacion (1)
% =====================================================================================


realizarOperacion(1) :-                                  % Opción usuario adivina la secuencia generada por la máquina
    crearSecuenciaAleatoria(SecuenciaMaquina),           % Invoca a crear la secuencia aleatoria
    jugarUContraMaquina(SecuenciaMaquina,0),             % Invoca al predicado con la lógica del juego
    regresarMenu.                                        % Regresa al menú

% =====================================================================================
%                                 realizarOperacion (2)
% =====================================================================================

realizarOperacion(2) :-                                  % Opción la máquina adivina la secuencia dada por el usuario
    write('Ingrese una lista de numeros : '),nl,
    read(SecuenciaUsuario),nl,                           % Lee la entrada ingresada por el usuario
    jugarMContraUsuario(SecuenciaUsuario),               % Invoca al predicado con la lógica del juego
    regresarMenu.                                        % Regresa al menú

% =====================================================================================
%                                 realizarOperacion (3)
% =====================================================================================

realizarOperacion(3) :-                                  % Opción de ver la tabla de mejores Puntaje
    guardarPuntajes,                                     % Invoca a cargar la tabla de mejores Puntaje
    mostrarMejoresPuntajes,                               % Muestra los mejores puntajes
    regresarMenu.                                        % Regresa al menú

% =====================================================================================
%                                 realizarOperacion (4)
% =====================================================================================
realizarOperacion(4) :-                                  % Opción de iniciar el juego con un nuevo usuario.
    retract(nombre_usuario(_)),                          % Quita de la base de Prolog el nombre de usuario anterior
    inicio.                                              % Vuelve a comenzar el programa 


% =====================================================================================
%                                 realizarOperacion (5)
% =====================================================================================

realizarOperacion(5) :-                                  % Termina el juego
     halt.                                               % Detiene la ejecución del programa


% =====================================================================================
realizarOperacion(_) :-                                  % Cuando no se ingresa una opción válida                     
    write(''), nl,
    write('Por favor, ingrese un numero valido'), nl,    % Imprime un mensaje cuando la opción es inválida
    menu.                                                % Se regresa al menú principal

% =====================================================================================
%                                    regresarMenu
% =====================================================================================
regresarMenu :-
    write('Presione Enter para volver al menu principal.'),
    read_line_to_codes(user_input, _Codes),              % Lee la entrada del usuario (en este caso, simplemente presionar Enter)
    nl,  
    menu.                                                % Se regresa al menú principal







% #####################################################################################

%                     PREDICADOS PARA LAS IMPLEMENTACIONES DEL JUEGO

% #####################################################################################




% =====================================================================================
%                                    contar_pos
% =====================================================================================
% Predicado para contar las posiciones en las que dos listas tienen el mismo elemento


contar_pos([], [], 0).                                    % Caso base: ambas listas están vacías, no hay coincidencias

contar_pos([X|Xs], [X|Ys], Coincidencias) :-              % Caso donde el primer elemento de ambas listas es igual
    contar_pos(Xs, Ys, CoincidenciasRestantes),           % Llamada recursiva con las colas de ambas listas
    Coincidencias is CoincidenciasRestantes + 1.          % Incrementa el contador de coincidencias en 1

                                                          
contar_pos([_|Xs], [_|Ys], Coincidencias) :-              % Caso donde el primer elemento de ambas listas es diferente
    contar_pos(Xs, Ys, Coincidencias).                    % Llamada recursiva sin incrementar el contador de coincidencias


% =====================================================================================
%                                  contarValoresCorrectos
% =====================================================================================
% Predicado para contar valores correctos en una lista

contarValoresCorrectos([], _, 0).                                     % Caso base: lista vacía, no hay valores correctos


contarValoresCorrectos([H|T], SecuenciaMaquina, ValoresCorrectos) :-  % Caso donde el primer elemento está en la secuencia objetivo
    member(H, SecuenciaMaquina),                                      % Verifica si H está en SecuenciaMaquina
    eliminarOcurrencias(H, SecuenciaMaquina, NuevaSecuenciaMaquina),  % Elimina ocurrencias de H en SecuenciaMaquina
    contarValoresCorrectos(T, NuevaSecuenciaMaquina, ValoresCorrectosRestantes),
    ValoresCorrectos is ValoresCorrectosRestantes + 1.


contarValoresCorrectos([_|T], SecuenciaMaquina, ValoresCorrectos) :-  % Caso donde el primer elemento no está en la secuencia objetivo
    contarValoresCorrectos(T, SecuenciaMaquina, ValoresCorrectos).



% =====================================================================================
%                                  eliminarOcurrencias
% =====================================================================================
% Predicado para eliminar ocurrencias de un elemento en una lista

eliminarOcurrencias(_, [], []).                                       % Caso base: lista vacía
eliminarOcurrencias(Elem, [Elem|T], NuevaLista) :-
    eliminarOcurrencias(Elem, T, NuevaLista).                         % Llamada recursiva sin agregar el primer elemento

eliminarOcurrencias(Elem, [H|T], [H|NuevaLista]) :-
    Elem \= H,  % Verifica si Elem es diferente de H
    eliminarOcurrencias(Elem, T, NuevaLista).                         % Llamada recursiva agregando el primer elemento

contarValoresLista(Lista, SecuenciaMaquina, Resultado) :-             % Predicado para contar valores correctos en una lista
    contarValoresCorrectos(Lista, SecuenciaMaquina, Resultado).       % Llama al predicado principal



% =====================================================================================
%                                     contarAciertos
% =====================================================================================
% Predicado para contar los aciertos (valores y posiciones correctas) entre dos secuencias

contarAciertos(SecuenciaUsuario, SecuenciaMaquina, ValoresCorrectos, PosicionesCorrectas) :-
    contarValoresCorrectos(SecuenciaUsuario, SecuenciaMaquina, ValoresCorrectos),  % Cuenta los valores correctos entre las secuencias
    contar_pos(SecuenciaUsuario, SecuenciaMaquina, PosicionesCorrectas).           % Cuenta las posiciones correctas entre las secuencias



% =====================================================================================
%                                 crearSecuenciaAleatoria
% =====================================================================================
% Predicado para cargar el módulo 'random' necesario para generar números aleatorios

:- use_module(library(random)).
crearSecuenciaAleatoria(Lista) :-                      % Predicado para crear una secuencia aleatoria de longitud 4
    length(Lista, 4),                                  % La longitud de la lista debe ser 4
    maplist(generarNumero, Lista).                     % Se aplica el predicado generarNumero a cada elemento de la lista

% =====================================================================================
%                                      generarNumero
% =====================================================================================
% Predicado para generar un número aleatorio entre 1 y 6

generarNumero(Numero) :-
    random_between(1, 6, Numero).                       % Genera un número aleatorio entre 1 y 6 


% =====================================================================================
%                                    generarSequencias
% =====================================================================================
% Predicado para generar todas las posibles secuencias de longitud 4 con elementos del 1 al 6

generarSequencias(Result) :-
    findall(PossibleLists, generate(4, [1, 2, 3, 4, 5, 6], PossibleLists), Result).

% Predicado auxiliar para generar secuencias recursivamente
generate(0, _, []).                                    % Caso base: no se generan más elementos, la lista resultante es vacía
generate(N, List, [H|T]) :-
    N > 0,                                             % Se asegura de que N sea mayor que 0 para continuar la generación
    N1 is N - 1,                                       % Decrementa N en 1 para la próxima llamada recursiva
    member(H, List),                                   % H es un miembro de List
    generate(N1, List, T).                             % Llamada recursiva para generar el resto de la lista




% #####################################################################################

%                           PREDICADOS PARA LOS MODOS DE JUEGO

% #####################################################################################


% =====================================================================================
%                                   jugarUContraMaquina
% =====================================================================================
% Predicado para que un usuario juegue contra la máquina


jugarUContraMaquina(_, 10) :-  % Si el número de intentos alcanza 10
    write(''), nl,      
    write('.............................................................................'), nl,  
    write(''), nl,  
    write('¡Has agotado 10 intentos! ¡La computadora ha ganado!'), nl,  % Mensaje de que el usuario ha perdido
    write('.............................................................................'), nl,  
    write(''), nl. 

jugarUContraMaquina(SecuenciaMaquina, Intentos) :-
    Intentos < 10,  % Verifica que el número de intentos sea menor que 10
    write(''), nl,      
    write('.............................................................................'), nl,  
    write(''), nl,  
    write('Ingrese una lista []. de cuatro valores del 1 al 6, separada por comas: '),nl,  % Solicita al usuario que ingrese una secuencia
    read(SecuenciaUsuario) ,nl,                               % Lee la secuencia ingresada por el usuario

    (   SecuenciaUsuario = SecuenciaMaquina ->                % Verifica si la secuencia ingresada coincide con la de la máquina
        write(''), nl,  % Salto de línea para dar espacio
        write('.............................................................................'), nl,  
        write('¡Felicidades, adivinaste la secuencia en '), write(Intentos), write(' intentos!'), nl,  
        write('.............................................................................'), nl,  
        write(''), nl,  
        nombre_usuario(Nombre),                               % Obtener el nombre del usuario
        guardarPuntaje(Nombre, Intentos)                      % Guardar el puntaje del usuario
        % Se interrumpe la ejecución porque el usuario ha adivinado la secuencia
    ;
        % Si la secuencia ingresada no coincide, se calculan los aciertos y se muestra la retroalimentación

        contarAciertos(SecuenciaUsuario, SecuenciaMaquina, ValoresCorrectos, PosicionesCorrectas),  % Calcula los aciertos
        write('Intento '), write(Intentos), write(': '),                                            % Muestra el número de intento
        write('Valores correctos: '), write(ValoresCorrectos), write(', '),                         % Muestra los valores correctos
        write('Posiciones correctas: '), write(PosicionesCorrectas), nl,                            % Muestra las posiciones correctas
        write(''), nl, 
        NuevoIntento is Intentos + 1,  % Incrementa el número de intentos
        jugarUContraMaquina(SecuenciaMaquina, NuevoIntento)   % Llama recursivamente al predicado para el siguiente intento
    ).


% =====================================================================================
%                                  jugarMContraUsuario
% =====================================================================================
% Predicado para que la máquina juegue contra el usuario


jugarMContraUsuario(SecuenciaUsuario) :-
    generarSequencias(ListaSequences),                            
    random_permutation(ListaSequences, SecuenciasDesordenadas),  
    adivinarMaquina(SecuenciaUsuario, SecuenciasDesordenadas, 1). % Inicia el proceso de adivinanza por parte de la máquina

adivinarMaquina(_, _, 11) :-                                     
    write('La computadora no pudo adivinar la secuencia en 10 intentos.'), nl.

adivinarMaquina(SecuenciaUsuario, [SecuenciaMaquina|RestoSecuencias], Intento) :-
    Intento < 11,                                                 
    write('¿Es '), write(SecuenciaMaquina), write(' (Si/No)? '),  
    read(Respuesta), nl,                                       
    downcase_atom(Respuesta, RespuestaLower),            
    (
        RespuestaLower = 's' ->                                        
            write('La computadora adivino la secuencia en '), write(Intento), write(' intentos.'), nl
        ;
        RespuestaLower = 'n' ->                                        
            write('¿Cuantos estan correctos en valor y posicion? '), read(CorrectosPosicion), nl,
            write('¿Cuantos estan correctos solo en valor? '), read(CorrectosColor), nl,
            filtrarSecuenciasRestantes(SecuenciaMaquina, CorrectosPosicion, CorrectosColor, RestoSecuencias, NuevasSecuencias),
            NuevoIntento is Intento + 1,
            length(NuevasSecuencias, Length), Length > 0,  % Verifica si quedan secuencias restantes
            adivinarMaquina(SecuenciaUsuario, NuevasSecuencias, NuevoIntento)
        ;
            write('La computadora no pudo adivinar la secuencia en 10 intentos.'), nl  % La máquina se rinde después de 10 intentos
    ).

% Filtra las secuencias restantes basadas en la información proporcionada por el usuario
filtrarSecuenciasRestantes(_, _, _, [], []).                                           % Caso base: no quedan secuencias por filtrar
filtrarSecuenciasRestantes(SecuenciaMaquina, CorrectosPosicion, CorrectosColor, [SecuenciaRestante|RestoSecuencias], [SecuenciaRestante|NuevasSecuencias]) :-
    contarAciertos(SecuenciaMaquina, SecuenciaRestante, PosicionesCorrectas, ValoresCorrectos), % Calcula los aciertos entre las secuencias
    PosicionesCorrectas = CorrectosPosicion,  % Verifica si el número de posiciones correctas coincide
    ValoresCorrectos = CorrectosColor,        % Verifica si el número de valores correctos coincide
    filtrarSecuenciasRestantes(SecuenciaMaquina, CorrectosPosicion, CorrectosColor, RestoSecuencias, NuevasSecuencias). % Llamada recursiva
filtrarSecuenciasRestantes(SecuenciaMaquina, CorrectosPosicion, CorrectosColor, [_|RestoSecuencias], NuevasSecuencias) :-
    filtrarSecuenciasRestantes(SecuenciaMaquina, CorrectosPosicion, CorrectosColor, RestoSecuencias, NuevasSecuencias). % Llamada recursiva para el resto de secuencias



% =====================================================================================
%                                   guardarPuntaje
% =====================================================================================


:- dynamic mejor_puntaje/2.                                    % Declaración dinámica ara permitir la modificación dinámica de hechos.

guardarPuntaje(Nombre, Intentos) :-
    retractall(mejor_puntaje(Nombre, _)),                      % Retracta todos los hechos de mejor_puntaje que coincidan con el nombre dado.
    assertz(mejor_puntaje(Nombre, Intentos)),                  % Agrega un nuevo hecho de mejor_puntaje con el nombre y los intentos dados.
    open('mejoresPuntajes.txt', append, Stream),               % Abre un archivo 'mejoresPuntajes.txt' en modo de escritura al final.
    write(Stream, 'mejor_puntaje(\''), write(Stream, Nombre), write(Stream, '\', '), write(Stream, Intentos), write(Stream, ').'), nl(Stream),  % Escribe el nuevo hecho en el archivo.
    close(Stream).                                             % Cierra el archivo.

guardarPuntajes :-
    retractall(mejor_puntaje(_, _)),                            % Retracta todos los hechos de mejor_puntaje.
    open('mejoresPuntajes.txt', read, Stream),                  % Abre el archivo 'mejoresPuntajes.txt' en modo de lectura.
    leerPuntaje(Stream),                                        % Lee los puntajes almacenados en el archivo.
    close(Stream).                                              % Cierra el archivo.

% =====================================================================================
%                                     leerPuntaje
% =====================================================================================

leerPuntaje(Stream) :-
    read(Stream, Term),                                         % Lee un término del archivo.
    (   Term == end_of_file ->                                  % Si se llega al final del archivo,
        true                                                    % Finaliza la lectura.
    ;   assertz(Term),                                          % Agrega el término leído como un nuevo hecho dinámico.
        leerPuntaje(Stream)                                     % Continúa leyendo el siguiente término.
    ).


% =====================================================================================
%                                mostrarMejoresPuntajes
% =====================================================================================

mostrarMejoresPuntajes :-
    write(''), nl,
    write('Mejores Puntajes:'), nl,                            % Imprime un encabezado para indicar que se mostrarán los mejores puntajes
    findall([Nombre, Intentos], mejor_puntaje(Nombre, Intentos), Puntaje),  % Encuentra todos los mejores puntajes y los almacena en la lista Puntaje
    sort(2, @=<, Puntaje, PuntajeSOrdenados),  % Ordena los puntajes según la cantidad de intentos
    mostrarPuntaje(PuntajeSOrdenados).                          % Llama al predicado mostrarPuntaje para mostrar los puntajes ordenados

mostrarPuntaje([]).  % Caso base: no hay más puntajes que mostrar
mostrarPuntaje([[Nombre, Intentos]|Resto]) :-                  % Caso recursivo: muestra un puntaje y luego llama recursivamente a mostrarPuntaje para el resto de los puntajes
    write('Nombre: '), write(Nombre), write('->'), write('Cantidad de intentos: '), write(Intentos), nl,      mostrarPuntaje(Resto). % Llama recursivamente a mostrarPuntaje 
