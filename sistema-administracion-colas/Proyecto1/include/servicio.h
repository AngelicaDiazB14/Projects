#ifndef SERVICIO_H
#define SERVICIO_H
#include <string>

using std::string;

/*
 Clase: Servicio
 Funcionalidad:
 -Permite crear un servicio con una descripci�n
  y el c�digo de un �rea.
 -Imprime el servicio.
 Autora: Dina Monge
*/
class Servicio {
private:
    string descripcion;
    string area;
    int contador_tiquetes;

public:
    // Constructor
    Servicio(string descripcion,string area){
        this->descripcion = descripcion;
        this->area = area;
    }
    // Aumenta el contador de tiquetes cada vez que se selecciona
    // un servicio a la hora de crear un tiquete (creado en la clase Area)
    void aumentarContadorTiquetes(){
        contador_tiquetes++;
    }
    // Permite obtener la descripci�n del servicio.
    string getDescripcion(){
        return descripcion;
    }
    // Permite obtener el �rea relacionada con el servicio.
    string getArea(){
        return area;
    }
    // Permite obtener el contador de tiquetes asociados al servicio.
    int getContador(){
        return contador_tiquetes;
    }
    // Permite imprimir la descripci�n del servicio.
    void printServicio(){
        cout << " Servicio: " << descripcion << " ";
    }
};

#endif // SERVICIO_H
