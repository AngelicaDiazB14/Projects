#ifndef AREA_H
#define AREA_H

#include "LinkedList.h"
#include "LinkedQueue.h"
#include "ventanilla.h"
#include "tiquete.h"
#include "lista_Servicios.h"
#include <iostream>
#include <string>
#include <ctime>
#include <time.h>
#include <stdexcept>

using std::cout;
using std::endl;
/*
 Clase: Area
 Funcionalidad:
 - Crear un área que es la base de todo,
   esta contiene ventanillas, lista de servicios, cola de tiquetes
   preferenciales y normales.
 - Permite:
   *crear ventanillas
   *Insertar en la cola de tiquetes preferenciales
   *Insertar en la cola de tiquetes normales
   *Insertar en la lista de servicios
   *Atender las filas (los tiquetes que están en la cola)
   *Eliminar áre y todo lo relacionado a ella
   *Se llama a métodos creados en la clase lista_Areas, lista_Servicios y ventanilla,
    métodos que son parte de las estadísticas relacionadas con los tiquetes y el tiempo
   (promedioTimepo(), totalTiquetesArea(), totalAtendidosVentanillas(), getTotalTiquetesPreferenciales(),
    cantidadTiquetesPorVentanilla()).

 Autor: David Centeno
*/
class Area{
    private:
        string descripcion;
        string codigo_area;
        List<ventanilla*> *base;
        Queue<tiquete*> *fnormal;
        Queue<tiquete*> *fprioridad;
        lista_Servicios *lista_servicios;
        int tiquete_count=0;
        int contadorTiquete=0;						// int
		int tiquetes_atendidos_Area=0;
		int tiquete_count_prioridad=0;
		int cantidad_ventanillas = 0;
		double tiempo_espera_general=0;
		time_t tiempo_actual;


    public:
        // Constructor
        Area(string descripcion, string codigo_area, int cantidad_ventanillas) {
            this->descripcion = descripcion;
            this->codigo_area = codigo_area;
            this->cantidad_ventanillas=cantidad_ventanillas;

            base = new LinkedList<ventanilla*>();
            fnormal = new LinkedQueue<tiquete*>();
            fprioridad = new LinkedQueue<tiquete*>();
            lista_servicios = new lista_Servicios();
            crearVentanillas(cantidad_ventanillas);

        }
        // Destructor
        ~Area() {
        }
        void crearVentanillas(int cantidad){
			for(int i=0; i < cantidad; i++){
				base->append(new ventanilla(codigo_area + std::to_string(i) ,false));
			}
			cantidad_ventanillas++;
		}
		//Entrada en fila prioridad
        void insertarPrioridad(int pos){
			time_t tiempo_inicial = time(&tiempo_inicial);
			fprioridad->enqueue(new tiquete(codigo_area+ std::to_string(tiquete_count),tiempo_inicial));
			tiquete_count_prioridad++;
			tiquete_count++;
			contadorTiquete++;
			lista_servicios->aumentarContadorTiqueteL(pos);//nuevo
		}
		//Entrada en fila normal
        void insertarNormal(int pos){
			time_t tiempo_inicial = time(&tiempo_inicial);
			fnormal->enqueue(new tiquete(codigo_area+std::to_string(tiquete_count),tiempo_inicial));
			tiquete_count++;
			contadorTiquete++;
			lista_servicios->aumentarContadorTiqueteL(pos);//nuevo
		}
		//Atención de filas
		bool atenderFilas(int pos){
		    tiquetes_atendidos_Area++;
			time(&tiempo_actual);
			if(!fprioridad->isEmpty()){
				tiquete *dato = fprioridad->dequeue();
				tiempo_espera_general = tiempo_espera_general + difftime(tiempo_actual,dato->getTimepo());//Cálculo de diferencia del tiempo
				string cod = dato->getCodigo();
				delete dato;
				insertarEnVentanilla(cod,pos);
				contadorTiquete--;
				return true;
			}else{
				if(!fnormal->isEmpty()){
					tiquete *dato = fnormal->dequeue();
					tiempo_espera_general = tiempo_espera_general + difftime(tiempo_actual,dato->getTimepo());//Cálculo de diferencia del tiempo
					string cod = dato->getCodigo();
					delete dato;
					insertarEnVentanilla(cod,pos);
					contadorTiquete--;
					return true;
				}else{
					return false;
				}
			}
		}
		//Insertar tiquetes en ventanilla
		void insertarEnVentanilla(string codigo_tiquete,int pos){
			base->goToPos(pos);
			ventanilla *vent = base->getElement();
			vent->atender(codigo_tiquete);
		}
		//Insertar servicio en la lista de servicios.
		void insertarEnListaServicios(string descripcion){
            lista_servicios->agregarServicio(descripcion,this->codigo_area);
		}

		//Promedio del tiempo de atención de tiquetes por área.
		double promedioTimepo(){
			return tiempo_espera_general/tiquetes_atendidos_Area;
		}
        //Obtener código del área.
		string getCodigo(){
            return codigo_area;
		}
        //Obtener descripción del área.
		string getDescripcion(){
            return descripcion;
		}
        //Obtener total contador de atendidos en el área.
		int totalTiquetesArea(){
            return tiquete_count;
		}
		//Total atendidos en área.
		int totalAtendidosVentanillas(){
            return tiquetes_atendidos_Area;
		}
		//Total tiquetes preferenciales
		int getTotalTiquetesPreferenciales(){
            return tiquete_count_prioridad;
		}
		//Muestra el total de tiquetes emitidos por servicio en un área específica.
		void totalTiquetesEmitidosPorServicio(){
            lista_servicios->printCantidadTiquetesServicios();
		}
        //Muestra la cantidad de tiquetes que se atendieron por ventanilla
		void cantidadTiquetesPorVentanilla(){
		    cout << "Cantidad tiquetes por ventanilla del área " << descripcion << ":"<<endl;
            for(base->goToStart();!base->atEnd();base->next()){
                ventanilla *vent = base->getElement();
                cout << "Ventanilla: " << vent->getCodigo() << " / " << "Cantidad: " << vent->getContadorVentanilla() << endl;
            }
            cout<<endl;
		}

        //Elimina un área
		void eliminarArea(){
		    base->goToStart();
            while(!base->isEmpty()){
                delete base->remove();
            }
            delete base;
            while(fnormal->getSize()!=0){
                delete fnormal->dequeue();
            }
            delete fnormal;
            while(fprioridad->getSize()!=0){
                delete fprioridad->dequeue();
            }
            delete fprioridad;
            //
            lista_servicios->borrarListaServicios();
            delete lista_servicios;
            contadorTiquete= 0;

		}
		// Reordena la lista de servicios
		void reordenarListaServicios(int pos_reubicar,int pos_destino){
            lista_servicios->reordenar(pos_reubicar,pos_destino);
		}
		void eliminarServicioL(int pos){
            lista_servicios->eliminarServicio(pos);
		}
		// Obtiene la cantidad de servicios que hay en la lista de servicios
		// Autora: Angélica Díaz
		int cantidadServicios(){
            return lista_servicios->getCantidadServicios();
		}
        // Imprime las ventanillas
        void printVentanillas() {
            for (base->goToStart() ;!base->atEnd(); base->next()){
                ventanilla *vent = base->getElement();
                vent->toStringVentanilla();
            }
        }
        // Imprime la lista de tiquetes regulares
        void prirntTiqutesFilaN(){
            cout<< "\nFila normal: " << endl;
            fnormal->print();
        }
        // Imprime la lista de tiquetes preferenciales.
        void prirntTiqutesFilaP(){
            cout<< "\nFila preferencial: " << endl;
            fprioridad->print();
        }
        // Imprime la lista de servicios
        void printListaServicios(){
            cout << "\nSERVICIOS:\n" << endl;
            if (cantidadServicios() != 0){
               lista_servicios->printServicios();
            }
            else{
                cout<<"Cantidad de servicios = 0"<<endl;
            }
        }
        //Obtiene la cantidad de ventanillas credas en el área.
       //Autora Angélica
       int getCantidadVentanillas(){
           return cantidad_ventanillas;
       }
       int contTiquetesArea(){
            return contadorTiquete;
		}


};

#endif // AREA_H
