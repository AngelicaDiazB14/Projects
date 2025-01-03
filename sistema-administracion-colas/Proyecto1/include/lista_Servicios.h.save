#ifndef LISTA_SERVICIOS_H
#define LISTA_SERVICIOS_H
#include "servicio.h"
#include "LinkedList.h"

/*
 Clase: lista_Servicios
 Funcionalidades:
  - agregar servicio a una  lista.
  - eliminar servicio de una lista.
  - reordenar los servicios de una lista
  - borrar la lista de servicios.
  - imprimir los servicios de una lista.
  - aumentar e imprimir la cantidad de tiquetes relacionados con el servicio.

 Autor: David Centeno
*/
class lista_Servicios{
private:
    List<Servicio*> *lista;
    int cantidad_servicios=0;

public:
    //Constructor
    lista_Servicios(){
        lista = new LinkedList<Servicio*>();
    }
    //Agrega un servicio a una lista
    void agregarServicio(string descripcion, string area){
        lista->append(new Servicio(descripcion,area));
        cantidad_servicios++;
    }
    // Elimina un servicio de una lista
    void eliminarServicio(int pos){
        lista->goToPos(pos);
        delete lista->remove();
        cantidad_servicios--;
    }
    // Permite reordenar los servicios de una lista
    void reordenar(int pos_reubicar,int pos_destino){
        lista->goToPos(pos_reubicar);
        Servicio *servicio = lista->remove();
        lista->goToPos(pos_destino);
        lista->insert(servicio);
    }
    //Borra toda la lista de servicios
    void borrarListaServicios(){
        lista->goToStart();
        while(!lista->isEmpty()){
            delete lista->remove();
        }
        cantidad_servicios=0;
    }
    //Imprime los ervicios que están en una lista
    void printServicios(){
        int i = 0;
        for(lista->goToStart(); !lista->atEnd();lista->next()){
            Servicio *servicio=lista->getElement();
            cout <<std::to_string(i) << ".";
            servicio->printServicio();
            cout<<"\n"<<endl;
            cout << endl;
            i++;
        }
    }



//===========================================================================
    //Aumenta el contador de los tiquetes relacionados a un servicio
    void aumentarContadorTiqueteL(int pos){
        lista->goToPos(pos);
        Servicio *servicio = lista->getElement();
        servicio->aumentarContadorTiquetes();
    }
    //Imprime la cantidad de tiquetes por servicios
    void printCantidadTiquetesServicios(){
        int i = 0;
        cout << "\n---------------------------- Servicios -------------------------------\n"<<endl;
        for(lista->goToStart(); !lista->atEnd();lista->next()){
            Servicio *servicio=lista->getElement();
            cout << std::to_string(i) << ". " << servicio->getDescripcion() << "\n" <<"\nCantidad tiquetes: " << std::to_string(servicio->getContador()) << endl;
            i++;
        }
    }
    //Obtiene la cantidad de servicios que hay en una lista.
    // Autora: Angélica Díaz.
    int getCantidadServicios(){
        return cantidad_servicios;
    }

};

#endif // LISTA_SERVICIOS_H
