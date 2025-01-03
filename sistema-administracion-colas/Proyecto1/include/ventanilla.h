#ifndef VENTANILLA_H
#define VENTANILLA_H
#include <string>

using namespace std;
using std::string;

/*
 Clase: ventanilla
 Funcionalidad:
 -Permite manejar la funcionalidades de los métodos que corresponden
  solo a la clase ventanilla, tales como: el estado (ocupado, en atención),
  eliminar una ventanilla, imprimir los atributos de la ventanilla (toStringVentanilla())
  y atender una ventanilla
 Autora: Dina Monge
*/

class ventanilla {
private:
    string codigo="";
    bool estado;
    string codigo_tiquete_atencion;
    int count_ventanilla = 0;	// Cantidad de atendidos por ventanilla

public:
    // Constructor
    ventanilla(string codigo, bool estado){
        this->codigo = codigo;
        this->estado = estado;
    }
    // Atiende un tiquete en la ventanilla, lo posiciona ahí,
    // marca la ventanilla como ocupada y aumenta el contador (count_ventanilla)
    // el cual representa los tiquetes que se atienden en la ventanilla.
    void atender(string codigo_tiquete){
        eliminar(); // Llamada al método eliminar para sacarlo de la ventanilla.
        estado=true;
        codigo_tiquete_atencion = codigo_tiquete;
        count_ventanilla ++;
        cout << "Atendiendo a tiquete " << codigo_tiquete_atencion << endl;
    }
    // Elimina la ventanilla
    void eliminar(){
        estado=false;
        codigo_tiquete_atencion="";
    }
    // Obtiene la cantidad de tiquetes atendidos por venanilla.
    int getContadorVentanilla(){
        return count_ventanilla;
    }
    // Obtiene el código de la ventanilla
    string getCodigo(){
        return codigo;
    }
    // Obtiene el código del tiquete que está siendo atendido.
    string tiquete_en_Ventanilla(){
        return codigo_tiquete_atencion;
    }
    // Retorna si la ventanilla está en atención o desocupada.
    string estadoVentanilla(){
        if(estado){
            return "En atención";
        }
        return "Desocupada";
    }
    //  Imprime los atributos de la ventanilla.
    void toStringVentanilla(){
        cout<<codigo << "\t\t\t    "<< estadoVentanilla()<< "\t\t"<<codigo_tiquete_atencion<<"~"<<endl;
        cout<<"______________________________________________________________________"<<endl;

    }

};

#endif // VENTANILLA_H
