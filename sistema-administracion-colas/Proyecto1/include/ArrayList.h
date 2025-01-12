#ifndef ARRAYLIST_H
#define ARRAYLIST_H
#define DEFAULT_MAX_SIZE 1024

#include "List.h"
#include <stdexcept>

using std::runtime_error;
using std::cout;
using std::endl;

/*
 Clase: ArrayList

 Autor: prof.Mauricio Avil�s

*/
template <typename E>
class ArrayList : public List<E> {
protected:
    E *elements;
    int max;
    int size;
    int pos;

    void checkFullList() {
        if (size == max)
            throw runtime_error("List is full.");
    }
    //Nuevos metodo
private:
    void expand(){
        E *temp = new E[max*2];
        for(int i=0; i < size; i++){
            temp[i]=elements[i];
        }
        delete [] elements;
        elements = temp;
        max=max*2;
    }

public:
    ArrayList(int max = DEFAULT_MAX_SIZE) {
        if (max < 1)
            throw runtime_error("Invalid max size.");
        elements = new E[max];
        this->max = max;
        size = 0;
        pos = 0;
    }
    ~ArrayList() {
        delete [] elements;
    }
    void insert(E element) {
        if(size==max){
            expand();
        }
        //checkFullList();
        for (int i = size; i > pos; i--)
            elements[i] = elements[i - 1];
        elements[pos] = element;
        size++;
    }
    void append(E element) {
        if (size==max){
            expand();
        }
        //checkFullList();
        elements[size] = element;
        size++;
    }
    E remove() {
        if (size == 0)
            throw runtime_error("List is empty.");
        if (pos == size)
            throw runtime_error("No current element.");
        E result = elements[pos];
        for (int i = pos; i < size - 1; i++)
            elements[i] = elements[i + 1];
        size--;
        return result;
    }
    void clear() {
        size = pos = 0;
        //delete [] elements;
        //elements = new E[max];
    }
    E getElement() {
        if (size == 0)
            throw runtime_error("List is empty.");
        if (pos == size)
            throw runtime_error("No current element.");
        return elements[pos];
    }
    void goToStart() {
        pos = 0;
    }
    void goToEnd() {
        pos = size;
    }
    void goToPos(int pos) {
        if (pos < 0 || pos > size)
            throw runtime_error("Invalid index.");
        this->pos = pos;
    }
    void next() {
        if (pos < size)
            pos++;
    }
    void previous() {
        if (pos > 0)
            pos--;
    }
    bool atStart() {
        return pos == 0;
    }
    bool atEnd() {
        return pos == size;
    }
    int getPos() {
        return pos;
    }
    int getSize() {
        return size;
    }
    void print() {
        int pos_actual=getPos();//guardar la posicion actual
        cout << "[ ";
        for (goToStart(); !atEnd(); next())
            cout << getElement() << " ";
        cout << "]" << endl;
        goToPos(pos_actual);//regresar a la posicion que se encontraba

    }






};

#endif // ARRAYLIST_H
