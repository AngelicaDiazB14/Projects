#ifndef QUEUE_H
#define QUEUE_H

/*
 Clase: Queue

 Autor: prof.Mauricio Avilés

*/
template <typename E>
class Queue {
private:
    void operator =(const Queue<E> &other) {}
    Queue(const Queue<E> &other) {}

public:
    Queue() {}
    virtual ~Queue() {}
    virtual void enqueue(E element) =0;
    virtual E dequeue() =0;
    virtual E frontValue() =0;
    virtual void clear() =0;
    virtual bool isEmpty() =0;
    virtual int getSize() =0;
    virtual void enqueueFront(E element) =0;
    virtual E dequeueRear()= 0;
    virtual E rearValue() = 0;
    virtual void print() =0;
};

#endif // QUEUE_H
