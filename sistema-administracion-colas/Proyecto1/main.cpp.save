#include <iostream>
#include "Area.h"
#include <ctime>
#include <time.h>
#include "lista_Areas.h"
#include "lista_Servicios.h"
// Permite utilizar exit para salir del programa
#include <stdio.h>
#include <stdlib.h>

using std::cout;
using std::cin;
using std::endl;
using std::string;
using std::stoi;// stoi pasar de string a entero entero


/*
 Clase: main
 Funcionalidad:
 -Permite la ejecución del programa por medio de
  diferentes menús, se realiza el llamado de los diferentes métodos
  creados en todo el programa y prueba las funcionalidades
  de los mismos.
 -Permite la interacción del usuario.
 Autora: Angélica Díaz
*/

// =======================================================================================================================

// Se declaran los siguientes métodos para su posterior utilización.
void menuTiquete();
void menuAdmi();
void menuEstadisticas();
void menuAreas();
void menuServicios();
bool isNumber3(const string& str);
bool numeroValido(string numero);
lista_Servicios *servicios = new lista_Servicios();
lista_Areas *areas  = new lista_Areas();

/*
 Nombre: isNumber
 Método que permite saber si un string es un número entero.
 Se utiliza las funciones find_first_not_of y string::npos
 que están incorparadas en std::string.

 Autor: Este método fue tomado de DelftStack abajo podrá encontrar el link.
*/
bool isNumber(const string& str){
    return str.find_first_not_of( "0123456789" ) == string::npos;
}

/*
 Método: numeroValido
 Valida que se haya ingresado un dato, que el dato sea un número,
 convierte el dato a número y valida que sea entero positivo.
 Autora: Angélica Díaz
*/
bool numeroValido(string numero){
    //.empty() es una función que permite saber si una cadena está vacía.
    if (!numero.empty()){
        if (isNumber(numero)){
            // stoi(dato) permite convertir un string a int.
            int num = stoi(numero);
            if (num >= 0){
                return true;
            }
            else{
                cout<<"\nERROR: debe ingresar un número entero positivo\n"<<endl;
                return false;
            }
        }
        else{
            cout<<"\nERROR: debe ingresar un número entero positivo\n"<<endl;
            return false;
        }
    }
    else{
        cout<<"\nERROR: espacio vacío\n"<<endl;
        return false;
    }
  }
// ============================================= MENÚ PRINCIPAL =================================================
/*
 Nombre: menuPrincipal
 Método que se le mostrará al usuario al iniciar con el programa.
 Este contiene 6 opciones a escoger y según la opción ingresada por
 el usuario este devolverá su respectivo método.
 Autora: Angélica Díaz
*/
void menuPrincipal(){
    string option;
    string numero1;
    string numero2;
    bool repetir = true;
    do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                  BIENVENID@ AL MENÚ PRINCIPAL                      ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Ver estados de la cola                                          ." << endl;
        cout << ". 2. Solicitar tiquete                                               ." << endl;
        cout << ". 3. Atender                                                         ." << endl;
        cout << ". 4. Administración                                                  ." << endl;
        cout << ". 5. Estadísticas del sistema                                        ." << endl;
        cout << ". 6. Salir                                                           ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                     if (areas->getCantidadAreas() != 0){
                         areas->printAreasVentaniTique();
                         return menuPrincipal();
                     }
                     else{
                        cout<<"\nERROR: no existen áreas disponibles por mostrar\n"<<endl;
                        return menuPrincipal();
                     }
                }
                case 2:{
                    menuTiquete();
                    break;
               }
               case 3:{
                   if (areas->getCantidadAreas() != 0 ){
                         areas->printAreas();
                         cout<<"\nIngrese el número del área: ";
                         getline(cin, numero1);
                         cout<<"\n"<<endl;
                         if (numeroValido(numero1)){
                         int num1 = stoi(numero1);
                             if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                area->printVentanillas();
                                cout<<"\nIngrese el número de la ventanilla: ";
                                getline(cin, numero2);
                                cout<<"\n"<<endl;
                                if (numeroValido(numero2)){
                                    int num2 = stoi(numero2);
                                    if (num2 < area->getCantidadVentanillas()){
                                        if (area->contTiquetesArea() != 0){
                                            area->atenderFilas(num2);
                                            cout<<"\n**********************************************************************"<<endl;
                                            cout<<"                 ¡El tiquete fue atendido exitosamente!"<<endl;
                                            cout<<"**********************************************************************"<<endl;
                                            cout<<"\n____________________________-TIQUETES-________________________________"<<endl;
                                            area->prirntTiqutesFilaN();
                                            cout<<"______________________________________________________________________"<<endl;
                                            area->prirntTiqutesFilaP();
                                            cout<<"______________________________________________________________________"<<endl;
                                            return menuPrincipal();
                                        }
                                        else{
                                            cout<<"\nERROR: no existen clientes en la cola.\n"<<endl;
                                            return menuPrincipal();
                                        }
                                    }
                                    else{
                                        cout<<"\nERROR: ventanilla no válida\n"<<endl;
                                        return menuPrincipal();
                                    }
                                }
                                 else{
                                    return menuPrincipal();
                                }
                            }
                            else{
                                cout<<"\nERROR: área no válida.\n"<<endl;
                                return menuPrincipal();
                            }
                        }
                        else{
                            return menuPrincipal();
                        }
                    }
                    else{
                        cout<<"\nERROR: aún no existen áreas creadas, ni servicios. \n"<<endl;
                        return menuPrincipal();
                    }
                }
                case 4:{
                    menuAdmi();
                    break;
                }
                case 5:{
                    menuEstadisticas();
                    break;
                }
                case 6:
                    if(areas->getCantidadAreas()!= 0){
                        areas->borrarListaAreas();
                    }
                    delete areas;
                    repetir = false;
                    cout <<"\n\n\n               ¡Gracias por utilizar nuestros servicios!"<<endl;
                    cout <<"\n                            ¡Vuelva pronto!\n\n"<<endl;
                    exit(-1);
                default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
                //return menuPrincipal();
            }
       }
       else{
           return menuPrincipal();
       }
    } while (repetir);
}

//============================================= MENÚ TIQUETE =================================================
/*
 Nombre: menuTiquete
 Contiene 2 opciones relacionadas con la creación de tiquetes
 y según la opción ingresada por el usuario este creará un
 tiquete preferencial o regular.
 Autora: Angélica Díaz
*/
void menuTiquete(){
     string option;
     string numero1;
     string numero2;
     bool repetir = true;
     do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                        SOLICITAR TIQUETE                           ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Seleccionar servicio                                            ." << endl;
        cout << ". 2. Cliente preferencial                                            ." << endl;
        cout << ". 3. Regresar                                                        ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                     if (areas->getCantidadAreas() != 0 ){
                         areas->printAreasConServicios();
                         cout<<"\nIngrese el número del área asociada con el servicio: ";
                         getline(cin, numero1);
                         if (numeroValido(numero1)){
                         int num1 = stoi(numero1);
                             if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                if (area->cantidadServicios() != 0){
                                    area->printListaServicios();
                                    cout<<"\nIngrese el número del servicio a consultar: ";
                                    getline(cin, numero2);
                                    if (numeroValido(numero2)){
                                        int num2 = stoi(numero2);
                                        if (num2 < area->cantidadServicios()){
                                            if(area->contTiquetesArea() <= 99){
                                                area->insertarNormal(num2);
                                                cout<<"\n**********************************************************************"<<endl;
                                                cout<<"                    ¡El tiquete fue creado exitosamente!"<<endl;
                                                cout<<"**********************************************************************"<<endl;
                                                cout<<"\n____________________________-TIQUETES-________________________________"<<endl;
                                                area->prirntTiqutesFilaN();
                                                cout<<"______________________________________________________________________"<<endl;
                                                return menuTiquete();
                                            }
                                            else{
                                                cout<<"\nERROR: máximo excedido, solo se permite generar de 0 a 99 tiquetes.\n"<<endl;
                                                return menuTiquete();
                                            }
                                        }
                                        else{
                                            cout<<"\nERROR: servicio no válido\n"<<endl;
                                            return menuTiquete();
                                        }
                                    }
                                    else{
                                        return menuTiquete();
                                    }
                                }
                                else{
                                    cout<<"\nERROR: no existen servicios creados en esta área\n"<<endl;
                                    return menuTiquete();
                                }
                            }
                            else{
                                cout<<"\nERROR: el área no existe.\n"<<endl;
                                return menuTiquete();
                            }
                        }
                        else{
                            return menuTiquete();
                        }
                    }
                    else{
                        cout<<"\nERROR: aún no existen áreas creadas, ni servcios. \n"<<endl;
                        return menuTiquete();
                    }
                }

                case 2:{
                    if (areas->getCantidadAreas() != 0 ){
                         areas->printAreasConServicios();
                         cout<<"\nIngrese el número del área asociada con el servicio: ";
                         getline(cin, numero1);
                         if (numeroValido(numero1)){
                         int num1 = stoi(numero1);
                             if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                if (area->cantidadServicios() != 0){
                                    area->printListaServicios();
                                    cout<<"\nIngrese el número del servicio a consultar: ";
                                    getline(cin, numero2);
                                    if (numeroValido(numero2)){
                                        int num2 = stoi(numero2);
                                        if (num2 < area->cantidadServicios()){
                                            area->insertarPrioridad(num2);
                                            cout<<"\n**********************************************************************"<<endl;
                                            cout<<"                    ¡El tiquete fue creado exitosamente!"<<endl;
                                            cout<<"**********************************************************************"<<endl;
                                            cout<<"\n____________________________-TIQUETES-________________________________"<<endl;
                                            area->prirntTiqutesFilaP();
                                            cout<<"______________________________________________________________________"<<endl;
                                            return menuTiquete();
                                        }
                                        else{
                                            cout<<"\nERROR: servicio no válido\n"<<endl;
                                            return menuTiquete();
                                        }
                                    }
                                    else{
                                        return menuTiquete();
                                    }
                                }
                                else{
                                    cout<<"\nERROR: no existen servicios creados en esta área.\n"<<endl;
                                    return menuTiquete();
                                }
                            }
                            else{
                                cout<<"\nERROR: el área no existe.\n"<<endl;
                                return menuTiquete();
                            }
                        }
                        else{
                            return menuTiquete();
                        }
                    }
                    else{
                        cout<<"\nERROR: aún no existen áreas creadas, ni servicios. \n"<<endl;
                        return menuTiquete();
                    }
               }
                case 3:
                    repetir = false;
                    menuPrincipal();
                    break;
                default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
                menuTiquete();
            }
        }
        else{
            return menuTiquete();
        }

    } while (repetir);
}


//============================================= MENÚ ADMINISTRACIÓN =================================================
/*
 Nombre: menuAdmi
 Contiene 2 opciones relacionadas con la creación de áreas
 y servicios y según la opción ingresada por el usuario este
 devolverá su respectivo método.
 Autora: Angélica Díaz
*/
void menuAdmi(){
    string option;
    bool repetir = true;
    do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                        ADMINISTRACIÓN                              ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Definir áreas                                                   ." << endl;
        cout << ". 2. Definir servicios disponibles                                   ." << endl;
        cout << ". 3. Regresar                                                        ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                    menuAreas();
                    break;
                }
                case 2:{
                    menuServicios();
                    break;
               }
                case 3:
                    repetir = false;
                    menuPrincipal();
                    break;
                default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
                menuAdmi();
            }
        }
        else{
            return menuAdmi();
        }

    } while (repetir);
}

//=============================================== MENÚ ÁREAS =================================================

/*
 Nombre: menuAreas
 Contiene las opciones de agregar área y eliminar áreas
 Autora: Angélica Díaz
*/
void menuAreas(){
    string option;
    string descripcion;
    string codigo;
    string cantVentan;
    string posicion;
    bool repetir = true;
    do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                           MENÚ ÁREAS                               ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Agregar área                                                    ." << endl;
        cout << ". 2. Eliminar área                                                   ." << endl;
        cout << ". 3. Eliminar todas las áreas                                        ." << endl;
        cout << ". 4. Regresar                                                        ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                    cout<<"\nPor favor ingrese los siguientes datos:\n"<<endl;
                    cout<<"Descripción del área: ";
                    getline(cin, descripcion);
                    if (!descripcion.empty()){
                        cout<<"Código del área: ";
                        getline(cin, codigo);
                        if (!codigo.empty()){
                            cout<<"Cantidad de ventanillas del área: ";
                            getline(cin, cantVentan);
                            if (numeroValido(cantVentan)){
                                int cantVentan1 = stoi(cantVentan); // stoi convierte un string a número.
                                if(cantVentan1 != 0){
                                    areas->agregarArea(descripcion, codigo,cantVentan1);
                                    cout<<"\n**********************************************************************"<<endl;
                                    cout<<"                 ¡El área ha sido creada exitosamente!"<<endl;
                                    cout<<"**********************************************************************"<<endl;
                                    areas->printAreasVentanilla();
                                    return menuAreas();
                                }
                                else{
                                    cout<<"\nERROR:\nEl área debe contener al menos una ventanilla.\n"<<endl;
                                    return menuAreas();
                                }
                            }
                            else{
                                return menuAreas();
                            }

                        }
                        else {
                            cout<<"\nERROR: debe ingresar el código del área\n"<<endl;
                            return menuAreas();
                        }
                    }
                    else {
                        cout<<"\nERROR: el área debe contener una descripción.\n"<<endl;
                        return menuAreas();
                    }
                }
                case 2:{
                    if (areas->getCantidadAreas() != 0){
                        areas->printAreas();
                        cout<<"\nPor favor ingrese los siguientes datos:\n"<<endl;
                        cout<<"Número del área a eliminar: ";
                        getline(cin, posicion);
                        if (numeroValido(posicion)){
                            int pos = stoi(posicion);
                            if (pos < areas->getCantidadAreas()){
                                areas->eliminarArea(pos);
                                cout<<"\n**********************************************************************"<<endl;
                                cout<<"                 ¡El área se ha eliminado exitosamente!"<<endl;
                                cout<<"**********************************************************************"<<endl;
                                areas->printAreas();
                                cout<<"\nCantidad de áreas: "<<areas->getCantidadAreas()<<"\n"<<endl;
                                return menuAreas();
                            }
                            else{
                                cout<<"\nERROR: el área no es válida\n"<<endl;
                                return menuAreas();
                            }
                        }
                        else{
                            return menuAreas();
                        }
                    }
                    else{
                        cout<<"\n                ¡¡¡ADVERTENCIA!!!\n\nAún no existen áreas creadas."<<endl;
                        cout<<"Por favor cree un área.\n"<<endl;
                        return menuAreas();
                    }

                }
                case 3:{
                    if (areas->getCantidadAreas() != 0){
                        if(areas->getCantidadAreas() > 1){
                            areas->printAreas();
                            areas->borrarListaAreas();
                            cout<<"\n**********************************************************************"<<endl;
                            cout<<"                 ¡Las áreas han sido eliminadas exitosamente!"<<endl;
                            cout<<"**********************************************************************"<<endl;
                            areas->printAreas();
                            cout<<"\nCantidad de áreas: "<<areas->getCantidadAreas()<<"\n"<<endl;
                            return menuAreas();
                        }
                        else{
                            areas->printAreas();
                            areas->borrarListaAreas();
                            cout<<"\n**********************************************************************"<<endl;
                            cout<<"                  ¡El área ha sido eliminada exitosamente!"<<endl;
                            cout<<"**********************************************************************"<<endl;
                            areas->printAreas();
                            cout<<"\nCantidad de áreas: "<<areas->getCantidadAreas()<<"\n"<<endl;
                            return menuAreas();
                        }
                    }
                    else{
                        cout<<"\n                ¡¡¡ADVERTENCIA!!!\n\nAún no existen áreas creadas."<<endl;
                        cout<<"Por favor cree un área.\n"<<endl;
                        return menuAreas();
                    }

                }
                case 4:
                    repetir = false;
                    menuAdmi();
                    break;
                default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
                menuAreas();
            }
       }
       else{
            return menuAreas();
       }
    } while (repetir);
}

//=============================================== MENÚ SERVICIOS =================================================

/*
 Nombre: menuServicios
 Contiene las opciones de agregar servicios, eliminar servicios y reordenar servicios.
 Autora: Angélica Díaz
*/

void menuServicios(){
    string option;
    string descripcion;
    string codigo;
    string numero1;
    string numero2;
    string pos_reubicar;
    string pos_destino;
    bool repetir = true;
    do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                        MENÚ SERVICIOS                              ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Agregar servicio                                                ." << endl;
        cout << ". 2. Eliminar servicio                                               ." << endl;
        cout << ". 3. Reordenar servicio                                              ." << endl;
        cout << ". 4. Regresar                                                        ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                    if(areas->getCantidadAreas() != 0){
                        areas->printAreas();
                        cout<<"\nPor favor ingrese los siguientes datos:\n"<<endl;
                        cout<<"Descripción del servicio: ";
                        getline(cin, descripcion);
                        if (!descripcion.empty()){
                                cout<<"Número del área a asignar: ";
                                getline(cin, codigo);
                                if (numeroValido(codigo)){
                                    int cod = stoi(codigo);
                                    if (cod < areas->getCantidadAreas()){
                                        Area *area = areas->buscarArea(cod);
                                        area->insertarEnListaServicios(descripcion);
                                        cout<<"\n**********************************************************************"<<endl;
                                        cout<<"                   ¡El servicio ha sido creado exitosamente!"<<endl;
                                        cout<<"**********************************************************************"<<endl;
                                        area->printListaServicios();
                                        return menuServicios();
                                        }
                                    else{
                                        cout<<"\nERROR: el área seleccionada no existe."<<endl;
                                        return menuServicios();
                                    }
                                }
                                else{
                                    return menuServicios();
                                }

                        }
                        else{
                            cout<<"\nERROR: el servicio debe contener una descripción.\n"<<endl;
                            return menuServicios();
                        }
                }
                else{
                    cout<<"\n                ¡¡¡ADVERTENCIA!!!\n\nAún no existen áreas creadas."<<endl;
                    cout<<"Por favor diríjase a crear un área.\n"<<endl;
                    return menuAreas();
                }

            }
            case 2:{
                if (areas->getCantidadAreas() != 0){
                    areas->printAreasConServicios();
                    cout<<"\nIngrese el número del área asociada con el servicio: ";
                    getline(cin, numero1);
                    if (numeroValido(numero1)){
                        int num1 = stoi(numero1);
                        if (num1 < areas->getCantidadAreas()){
                            Area *area = areas->buscarArea(num1);
                            if (area->cantidadServicios() != 0){
                                area->printListaServicios();
                                cout<<"\nIngrese el número del servicio a eliminar: ";
                                getline(cin, numero2);
                                if (numeroValido(numero2)){
                                    int num2 = stoi(numero2);
                                    if (num2 < area->cantidadServicios()){
                                        area->eliminarServicioL(num2);
                                        cout<<"\n**********************************************************************"<<endl;
                                        cout<<"                 ¡El servicio ha sido eliminado exitosamente!"<<endl;
                                        cout<<"**********************************************************************"<<endl;
                                        area->printListaServicios();
                                        return menuServicios();
                                    }
                                    else{
                                        cout<<"\nERROR: el servicio seleccionado no es válido\n"<<endl;
                                        return menuServicios();
                                    }
                                }
                                else{
                                    return menuServicios();
                                                    }
                            }
                            else{
                                cout<<"\nERROR: el área seleccionada aún no tiene servicios asociados\n"<<endl;
                                return menuServicios();
                            }
                        }
                        else{
                            cout<<"\nERROR: el área seleccionada no existe.\n"<<endl;
                            return menuServicios();
                        }
                  }
                  else{
                      return menuServicios();
                  }

              }
              else{
                  cout<<"\n                   ¡¡¡ADVERTENCIA!!!\n"<<endl;
                  cout<<"\n~Aún no existen áreas creadas, por lo tanto,\nno hay servicios disponibles a eliminar."<<endl;
                  cout<<"\n~Por favor diríjase a crear un área,\nposteriormente podrá crear servicios y eliminar.\n"<<endl;
                  return menuAreas();
              }
            }
            case 3:{
                 if (areas->getCantidadAreas() != 0){
                    areas->printAreasConServicios();
                    cout<<"\nIngrese el número del área asociada con el servicio: ";
                    getline(cin, numero1);
                    if (numeroValido(numero1)){
                        int num1 = stoi(numero1);
                        if (num1 < areas->getCantidadAreas()){
                            Area *area = areas->buscarArea(num1);
                            if (area->cantidadServicios() != 0){
                                area->printListaServicios();
                                cout<<"\nIngrese la posición del servicio que desea reordenar: ";
                                getline(cin, pos_reubicar);
                                if(numeroValido(pos_reubicar)){
                                    int posReubicar = stoi(pos_reubicar);
                                    if (posReubicar < area->cantidadServicios()){
                                        cout<<"\nIngrese la posición destino del servicio: ";
                                        getline(cin, pos_destino);
                                        if (numeroValido(pos_destino)){
                                            int posDestino = stoi(pos_destino);
                                            if (posDestino < area->cantidadServicios()){
                                                area->reordenarListaServicios(posReubicar, posDestino);
                                                cout<<"\n**********************************************************************"<<endl;
                                                cout<<"                  ¡El servicio ha sido reordenado exitosamente!"<<endl;
                                                cout<<"**********************************************************************"<<endl;
                                                area->printListaServicios();
                                                return menuServicios();
                                            }
                                            else{
                                                cout<<"\nERROR: posición no válida\n"<<endl;
                                                return menuServicios();
                                            }
                                        }
                                        else{
                                            return menuServicios();
                                        }
                                    }
                                    else{
                                       cout<<"\nERROR: posición no válida\n"<<endl;
                                       return menuServicios();
                                    }
                                }
                                else{
                                    return menuServicios();
                                }
                            }
                            else{
                                cout<<"\nERROR: el área seleccionada aún no tiene servicios asociados\n"<<endl;
                                return menuServicios();
                            }
                        }
                        else{
                            cout<<"\nERROR: el área seleccionada no existe.\n"<<endl;
                            return menuServicios();
                        }
                    }
                    else{
                        return menuServicios();
                    }
                 }
                 else{
                     cout<<"\n                   ¡¡¡ADVERTENCIA!!!\n"<<endl;
                     cout<<"\n~Aún no existen áreas creadas, por lo tanto,\nno hay servicios disponibles por reordenar."<<endl;
                     cout<<"\n~Por favor diríjase a crear un área,\nposteriormente podrá crear servicios y reordenarlos.\n"<<endl;
                     return menuAreas();
              }
            }
            case 4:
                repetir = false;
                menuAdmi();
                break;
            default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
            menuServicios();
       }
     }
     else{
            return menuServicios();
     }
    } while (repetir);
}


//============================================= MENÚ ESTADÍSTICAS =================================================
/*
 Nombre: menuEstadisticas
 Este método permite al usuario conocer las diferentes estadísticas
 relacionadas con los tiquetes y el tiempo.
 Autora: Angélica Díaz
*/
void menuEstadisticas(){
    string option;
    string numero1;
    bool repetir = true;
    do {
        //system("cls"); limpia la pantalla
        cout << "\n......................................................................" << endl;
        cout << ".                        ESTADÍSTICAS                                ." << endl;
        cout << ".                                                                    ." << endl;
        cout << ". 1. Tiempo promedio de espera por área                              ." << endl;
        cout << ". 2. Total de tiquetes dispensados por área                          ." << endl;
        cout << ". 3. Total de tiquetes atendidos por ventanilla                      ." << endl;
        cout << ". 4. Total de tiquetes emitidos por servicio                         ." << endl;
        cout << ". 5. Total de tiquetes preferenciales dispensados en todo el sistema ." << endl;
        cout << ". 6. Regresar                                                        ." << endl;
        cout << "......................................................................" << endl;
        cout << "\nIngrese una opción y presione ENTER para continuar: ";
        getline(cin, option);
        if (numeroValido(option)){
            int opcion = stoi(option);
            switch (opcion){
                case 1:{
                    if (areas->getCantidadAreas() != 0){
                        areas->printAreas();
                        cout << "\nIngrese el número del área a consultar: ";
                        getline(cin, numero1);
                        if (numeroValido(numero1)){
                            int num1 = stoi(numero1);
                            if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                if (area->totalAtendidosVentanillas() != 0){
                                     cout<<"\nTiempo promedio de espera en el área número "<<num1<<" : "<<area->promedioTimepo()<<" segundos\n"<<endl;
                                     return menuEstadisticas();
                                }
                                else{
                                    cout<<"\nERROR: aún no existen clientes registrados como atendidos.\n"<<endl;
                                    return menuEstadisticas();
                                }
                            }
                            else{
                                cout<<"nERROR: el área ingresada no existe.\n"<<endl;
                                return menuEstadisticas();
                            }
                        }
                        else{
                            cout<<"nERROR: debe ingresar un número entero positivo.\n"<<endl;
                            return menuEstadisticas();
                        }
                    }
                    else{
                        cout<<"nERROR: no existen áreas creadas.\n"<<endl;
                        return menuEstadisticas();
                        }
                }
                case 2:{
                    if (areas->getCantidadAreas() != 0){
                        areas->printCantidadTiquetesPorArea();
                        return menuEstadisticas();
                    }
                    else{
                        cout<<"nERROR: no existen áreas creadas.\n"<<endl;
                        return menuEstadisticas();
                    }
                }
               case 3:{
                   if (areas->getCantidadAreas() != 0){
                        areas->printAreas();
                        cout << "\nIngrese el número del área a consultar: ";
                        getline(cin, numero1);
                        if (numeroValido(numero1)){
                            int num1 = stoi(numero1);
                            if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                cout<<"\nTiquetes atendidos en las ventanillas del área # "<<num1<<": "<<area->totalAtendidosVentanillas()<<endl;
                                return menuEstadisticas();
                            }
                            else{
                                cout<<"nERROR: el área ingresada no existe.\n"<<endl;
                                return menuEstadisticas();
                            }
                        }
                        else{
                            cout<<"nERROR: debe ingresar un número entero positivo.\n"<<endl;
                            return menuEstadisticas();
                        }
                    }
                    else{
                        cout<<"nERROR: no existen áreas creadas.\n"<<endl;
                        return menuEstadisticas();
                    }
                }
                case 4:{
                    if (areas->getCantidadAreas() != 0){
                        areas->printAreas();
                        cout << "\nIngrese el número del área a consultar: ";
                        getline(cin, numero1);
                        if (numeroValido(numero1)){
                            int num1 = stoi(numero1);
                            if (num1 < areas->getCantidadAreas()){
                                Area *area = areas->buscarArea(num1);
                                if(area->cantidadServicios() != 0){
                                    //cout<<"\nCantidad de tiquetes emitidos por servicio en el área # "<<num1<<": "<<endl;
                                    area->totalTiquetesEmitidosPorServicio();
                                    return menuEstadisticas();
                                }
                                else{
                                    cout<<"\nERROR: en esta área no hay servicios asociados.\n"<<endl;
                                    return menuEstadisticas();
                                }
                            }
                            else{
                                cout<<"\nERROR: el área ingresada no existe.\n"<<endl;
                                return menuEstadisticas();
                            }
                        }
                        else{
                            cout<<"\nERROR: debe ingresar un número entero positivo.\n"<<endl;
                            return menuEstadisticas();
                        }
                    }
                    else{
                        cout<<"\nERROR: no existen áreas creadas.\n"<<endl;
                        return menuEstadisticas();
                    }
                }
                case 5:{
                    if (areas->getCantidadAreas() != 0){
                        areas->printCantidadTiquetesPreferencialesEmitidos();
                        return menuEstadisticas();
                    }
                    else{
                        cout<<"\nERROR: no existen áreas creadas.\n"<<endl;
                        return menuEstadisticas();
                        }
                }
                case 6:
                    repetir = false;
                    menuPrincipal();
                    break;
                default: cout <<"\n¡¡¡Opción incorrecta, por favor vuelva a intentarlo!!!"<<endl;
                menuEstadisticas();
            }
       }
       else{
            return menuEstadisticas();
       }
    } while (repetir);
}






//================================================= MAIN =================================================
int main(){
    setlocale(LC_ALL, "spanish"); // Permite el uso de caracteres especiales
    menuPrincipal(); // Invoca al menú principal
    return 0;
}

//============================================= REFERENCIAS =================================================
/*
REFERENCIAS:
Comprobar que la entrada sea un entero:
https://www.delftstack.com/es/howto/cpp/check-if-input-is-integer-cpp/#:~:text=Number%20Not%20number-,Use%20la%20funci%C3%B3n%20std%3A%3Astring%3A%3Afind_first_not_of%20para%20verificar,el%20objeto%20std%3A%3Astring%20.

Convertir una cadena a entero:
https://www.delftstack.com/es/howto/cpp/how-to-convert-string-to-int-in-cpp/

Comprobar si la cadena está vacía:
https://www.delftstack.com/es/howto/cpp/cpp-check-if-string-is-empty/#:~:text=en%20C%2B%2B.-,Usar%20el%20m%C3%A9todo%20incorporado%20empty()%20para%20comprobar%20si%20la,el%20objeto%20no%20contiene%20caracteres.
Biblioteca <algorithm>:
https://learn.microsoft.com/es-es/cpp/standard-library/algorithm?view=msvc-170

Finalizar programa con exit:
https://learn.microsoft.com/es-es/cpp/cpp/program-termination?view=msvc-170
*/




