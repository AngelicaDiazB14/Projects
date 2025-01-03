#ifndef LISTA_AREAS_H
#define LISTA_AREAS_H
#include "Area.h"
#include "LinkedList.h"


class lista_Areas{
private:
    List<Area*> *lista;
    int cantidad_areas = 0;

/*
 Clase: lista_Areas
 Funcionalidades:
  - agregar �rea a la lista.
  - eliminar �rea de la lista.
  - buscar un �rea en la lista.
  - borrar lista de �reas.
  - imprimir tiempo de espera promedio del �rea.
  - imprimir cantidad de tiquetes por �rea.
  - imprimir cantidad de tiquetes preferenciales emitidos.
  - imprimir cantidad de tiquetes emitidos por servico.
  - impimir las �reas de la lista.
  - imprimir las �reas y sus ventanillas
  - impirmir las �reas, ventanillas y tiquetes regulares y preferenciales
  - imprimir �reas con servicios.

 Autor: David Centeno
 En los m�todos de impresi�n los cout fueron modificados por Ang�lica D�az.
*/

public:
    //Constructor
    lista_Areas(){
        lista = new LinkedList<Area*>();
    }
    // agrega un �rea a la lsita de �reas
    void agregarArea(string descripcion, string codigo,int ventanillas){
        lista->append(new Area(descripcion , codigo , ventanillas));;
        cantidad_areas++;
    }
    // elimina un �rea de la lista de �reas
    void eliminarArea(int pos){
        lista->goToPos(pos);
        Area *area = lista->remove();
        area->eliminarArea();
        delete area;
        cantidad_areas--;

    }
    //Busca un �rea en la lista de �reas
    Area* buscarArea(int pos){
        lista->goToPos(pos);
        return lista->getElement();
    }
   //Imprime el tiempo promedio de atenci�n de un �rea
    void printTimepoEsperaPromedioArea(int pos){
        lista->goToPos(pos);
        Area *area = lista->getElement();
        cout << "Tiempo de espera promedio �rea " << area->getDescripcion() << ": " << area->promedioTimepo() <<endl;
    }
    //Imprime la cantidad de tiquetes que hay en un �rea.
    void printCantidadTiquetesPorArea(){
         int i = 0;
        cout << "\n------------- Cantidad de tiquetes dispensados por �rea --------------\n" <<endl;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<< "#."<< std::to_string(i) << " �rea: "<< area->getDescripcion()<<"\n\nCantidad tiquetes: "<<area->totalTiquetesArea() <<" "<<endl;
            cout<<"______________________________________________________________________\n"<<endl;
            i++;
        }
    }
    //Borra la lista de �reas y todo su contenido.
    void borrarListaAreas(){
        lista->goToStart();
        while(!lista->isEmpty()){
            Area *area = lista->remove();
            area->eliminarArea();
            delete area;
        }
        cantidad_areas=0;
    }
    //Imprime la cantidad de tiquetes atendidos por ventanilla
    void printCantidadAtendidosVentanilla(int pos){
        lista->goToPos(pos);
        Area *area = lista->getElement();
        area->cantidadTiquetesPorVentanilla();
    }
    //Imprime la cantidad de tiquetes preferenciales emitidos
    void printCantidadTiquetesPreferencialesEmitidos(){
        int cantidad_tiquetes_preferenciales = 0;
        int i = 0;
        cout <<"\n--------------------- Tiquetes preferenciales ------------------------\n" <<endl;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<<"#."<< std::to_string(i) << " �rea: " << area->getDescripcion()<< "\n\nCantidad tiquetes: " << area->getTotalTiquetesPreferenciales() << endl;
            i++;
            cout<<"______________________________________________________________________\n"<<endl;
            cantidad_tiquetes_preferenciales+=area->getTotalTiquetesPreferenciales();
        }
        cout << "\nTotal de tiquetes preferenciales emitidos: " << cantidad_tiquetes_preferenciales<<"\n" << endl;
    }
    //Imprime la cantidad de tiquetes emitidos por servicio
    void printCantidadTiquetesEmitidosServicio(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout <<"N�MERO: "<< std::to_string(i) << "\t" << " �REA: " << area->getDescripcion()<<endl;
            area->totalTiquetesEmitidosPorServicio();
        }
    }
    //Imprime las �reas que hay en la lista de �reas.
    void printAreas(){
        int i = 0;
        cout << "\n�REAS DISPONIBLES" <<endl;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<<"______________________________________________________________________"<<endl;
            cout<<"N�MERO: "<<std::to_string(i) << "\t\t    " <<"�REA: " << area->getDescripcion() <<endl;
            cout<<"______________________________________________________________________\n"<<endl;
            i++;
        }

    }
    //Imprime las �reas de la lista y sus ventanillas
    void printAreasVentanilla(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            cout<<"\n---------------------------------"<<endl;
            Area *area = lista->getElement();
            cout<< std::to_string(i) << "." <<" �REA: " << area->getDescripcion() <<endl;
            cout<<"---------------------------------\n"<<endl;
            cout << "\nC�digo de ventanilla "<< "\t"<< "Estado de ventanilla"<<"\t"<<"Tiquete en atenci�n\n"<<endl;
            area->printVentanillas();
            cout<<endl;
            i++;
        }
    }
     //Imprime las �reas de la lista, sus ventanillas y colas de tiquetes.
     void printAreasVentaniTique(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            cout<<"\n---------------------------------"<<endl;
            Area *area = lista->getElement();
            cout<< std::to_string(i) << "." <<" �REA: " << area->getDescripcion() <<endl;
            cout<<"---------------------------------\n"<<endl;
            cout << "\nC�digo de ventanilla "<< "\t"<< "Estado de ventanilla"<<"\t"<<"Tiquete en ventanilla\n"<<endl;
            area->printVentanillas();
            cout<<"\n____________________________-TIQUETES-________________________________"<<endl;
            area->prirntTiqutesFilaP();
            cout<<"______________________________________________________________________"<<endl;
            area->prirntTiqutesFilaN();
            cout<<"______________________________________________________________________"<<endl;
            cout<<endl;
            i++;
        }
     }

    //Imprime las �reas de la lista y sus servicios
    void printAreasConServicios(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<<"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;
            cout<<std::to_string(i) << ". " <<"�REA: " << area->getDescripcion() <<endl;
            area->printListaServicios();
            cout<<"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"<<endl;
            i++;
        }
    }

     //Obtiene la cantidad de �reas de una lista.
    // Autora: Ang�lica D�az
    int getCantidadAreas(){
        return cantidad_areas;
    }

};

#endif // LISTA_AREAS_H
