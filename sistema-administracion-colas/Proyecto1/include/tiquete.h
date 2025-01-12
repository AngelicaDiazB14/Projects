#ifndef TIQUETE_H
#define TIQUETE_H
#include <iostream>
#include <string>
#include <ctime>
#include <time.h>

using std::string;
using std::ostream;

/*
 Clase: tiquete
 Funcionalidad:
 -Permite crear un tiquete con un c�digo y el tiempo actual
  del sistema y permite la impresi�n del tiquete
 Autora: Dina Monge
*/
class tiquete {
private:
    string codigo;//Codigo de tiquete
    time_t tiempo_entrada;//Tiempo de entrada de tiquete

public:
    // Constructor
    tiquete(string codigo,time_t tiempo_entrada){
        this->codigo = codigo;
        this->tiempo_entrada = tiempo_entrada;
    }
    // Obtiene el atributo tiempo_entrada del tiquete.
    time_t getTimepo(){
        return tiempo_entrada;
    }
    // Obtiene el c�digo del tiquete.
    string getCodigo() const{
        return codigo;
    }

};

// Imprime el c�digo del tiquete.
ostream& operator<<(ostream& os, const tiquete& t) {
    os << t.getCodigo() << " ";
    return os;
}

#endif // TIQUETE_H
