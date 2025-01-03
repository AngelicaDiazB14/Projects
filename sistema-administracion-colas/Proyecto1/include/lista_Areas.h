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
  - agregar área a la lista.
  - eliminar área de la lista.
  - buscar un área en la lista.
  - borrar lista de áreas.
  - imprimir tiempo de espera promedio del área.
  - imprimir cantidad de tiquetes por área.
  - imprimir cantidad de tiquetes preferenciales emitidos.
  - imprimir cantidad de tiquetes emitidos por servico.
  - impimir las áreas de la lista.
  - imprimir las áreas y sus ventanillas
  - impirmir las áreas, ventanillas y tiquetes regulares y preferenciales
  - imprimir áreas con servicios.

 Autor: David Centeno
 En los métodos de impresión los cout fueron modificados por Angélica Díaz.
*/

public:
    //Constructor
    lista_Areas(){
        lista = new LinkedList<Area*>();
    }
    // agrega un área a la lsita de áreas
    void agregarArea(string descripcion, string codigo,int ventanillas){
        lista->append(new Area(descripcion , codigo , ventanillas));;
        cantidad_areas++;
    }
    // elimina un área de la lista de áreas
    void eliminarArea(int pos){
        lista->goToPos(pos);
        Area *area = lista->remove();
        area->eliminarArea();
        delete area;
        cantidad_areas--;

    }
    //Busca un área en la lista de áreas
    Area* buscarArea(int pos){
        lista->goToPos(pos);
        return lista->getElement();
    }
   //Imprime el tiempo promedio de atención de un área
    void printTimepoEsperaPromedioArea(int pos){
        lista->goToPos(pos);
        Area *area = lista->getElement();
        cout << "Tiempo de espera promedio área " << area->getDescripcion() << ": " << area->promedioTimepo() <<endl;
    }
    //Imprime la cantidad de tiquetes que hay en un área.
    void printCantidadTiquetesPorArea(){
         int i = 0;
        cout << "\n------------- Cantidad de tiquetes dispensados por área --------------\n" <<endl;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<< "#."<< std::to_string(i) << " Área: "<< area->getDescripcion()<<"\n\nCantidad tiquetes: "<<area->totalTiquetesArea() <<" "<<endl;
            cout<<"______________________________________________________________________\n"<<endl;
            i++;
        }
    }
    //Borra la lista de áreas y todo su contenido.
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
            cout<<"#."<< std::to_string(i) << " Área: " << area->getDescripcion()<< "\n\nCantidad tiquetes: " << area->getTotalTiquetesPreferenciales() << endl;
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
            cout <<"NÚMERO: "<< std::to_string(i) << "\t" << " ÁREA: " << area->getDescripcion()<<endl;
            area->totalTiquetesEmitidosPorServicio();
        }
    }
    //Imprime las áreas que hay en la lista de áreas.
    void printAreas(){
        int i = 0;
        cout << "\nÁREAS DISPONIBLES" <<endl;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<<"______________________________________________________________________"<<endl;
            cout<<"NÚMERO: "<<std::to_string(i) << "\t\t    " <<"ÁREA: " << area->getDescripcion() <<endl;
            cout<<"______________________________________________________________________\n"<<endl;
            i++;
        }

    }
    //Imprime las áreas de la lista y sus ventanillas
    void printAreasVentanilla(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            cout<<"\n---------------------------------"<<endl;
            Area *area = lista->getElement();
            cout<< std::to_string(i) << "." <<" ÁREA: " << area->getDescripcion() <<endl;
            cout<<"---------------------------------\n"<<endl;
            cout << "\nCódigo de ventanilla "<< "\t"<< "Estado de ventanilla"<<"\t"<<"Tiquete en atención\n"<<endl;
            area->printVentanillas();
            cout<<endl;
            i++;
        }
    }
     //Imprime las áreas de la lista, sus ventanillas y colas de tiquetes.
     void printAreasVentaniTique(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            cout<<"\n---------------------------------"<<endl;
            Area *area = lista->getElement();
            cout<< std::to_string(i) << "." <<" ÁREA: " << area->getDescripcion() <<endl;
            cout<<"---------------------------------\n"<<endl;
            cout << "\nCódigo de ventanilla "<< "\t"<< "Estado de ventanilla"<<"\t"<<"Tiquete en ventanilla\n"<<endl;
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

    //Imprime las áreas de la lista y sus servicios
    void printAreasConServicios(){
        int i = 0;
        for(lista->goToStart();!lista->atEnd();lista->next()){
            Area *area = lista->getElement();
            cout<<"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;
            cout<<std::to_string(i) << ". " <<"ÁREA: " << area->getDescripcion() <<endl;
            area->printListaServicios();
            cout<<"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"<<endl;
            i++;
        }
    }

     //Obtiene la cantidad de áreas de una lista.
    // Autora: Angélica Díaz
    int getCantidadAreas(){
        return cantidad_areas;
    }

};

#endif // LISTA_AREAS_H
