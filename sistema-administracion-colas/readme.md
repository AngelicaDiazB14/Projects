# Sistema de Administración de Colas

## **Realizado por:**
- **David Josué Centeno Araya**
- **Dina Isabel Monge Sandoval**
- **Angélica María Díaz Barrios**

---

## **Descripción General**
Este proyecto surge de la necesidad de mejorar la organización y gestión de colas en establecimientos que ofrecen servicios presenciales. El objetivo es desarrollar un sistema virtual en consola (sin interfaz gráfica) que permita:

- Mantener el orden en las filas.
- Priorizar la atención de personas con condiciones especiales (adultos mayores, mujeres embarazadas, personas con discapacidades, etc.).
- Administrar diferentes áreas y servicios.
- Generar estadísticas relacionadas con los tiempos y atenciones.

El sistema está diseñado para ser lo suficientemente flexible y configurable, adaptándose a distintas situaciones o tipos de locales.

El proyecto se desarrolla en **C++**, utilizando estructuras de datos para implementar la lógica del sistema, como colas para manejar la atención de clientes.

---

## **Funcionalidades Principales**

### 1. **Gestor de Áreas y Ventanillas**
- Creación de áreas dentro del sistema.
- Cada área contiene una cantidad configurable de ventanillas para la atención.
- Prioridad en la atención de clientes preferenciales.

### 2. **Manejo de Tiquetes**
- Generación de tiquetes para los clientes.
- Identificación de clientes regulares y preferenciales.
- Orden de atención basado en la prioridad y el tiempo de llegada.

### 3. **Estadísticas**
- Registro de datos relacionados con los tiquetes y tiempos de atención.
- Generación de informes sobre el rendimiento de las ventanillas y las áreas.

---

## **Estructura del Proyecto**
El desarrollo del proyecto se divide en las siguientes etapas:

1. **Documentación**
   - Introducción.
   - Análisis del problema.
   - Metodología.
   - Análisis crítico.
   - Conclusiones y recomendaciones.

2. **Programación**
   - Implementación de estructuras de datos para manejar las colas.
   - Desarrollo de funciones para gestionar áreas, ventanillas y clientes.
   - Generación y administración de tiquetes.
   - Desarrollo de un sistema de prioridades.
   - Generación de informes estadísticos.

---

## **Requisitos**
- **Lenguaje de programación**: C++
- **Entorno de desarrollo**: Cualquier IDE compatible con C++ (Code::Blocks, Visual Studio, etc.)

---

## **Ejemplo de Uso**
### **Simulación de una Cola de Atención**
1. **Inicio del Sistema:**
   - Crear áreas y asignar ventanillas.
2. **Registro de Clientes:**
   - Generación de tiquetes según tipo de cliente (regular o preferencial).
3. **Atención:**
   - Los clientes preferenciales son atendidos antes de los regulares, respetando el orden de llegada.
4. **Generación de Estadísticas:**
   - Tiempo promedio de atención.
   - Número de clientes atendidos por ventanilla.

---

## **Notas Importantes**
- El sistema está diseñado para ser escalable y adaptable.
- Los clientes que requieren atención especial son gestionados de manera prioritaria para garantizar una mejor experiencia.

---

## **Conclusión**
Este sistema ofrece una solución efectiva para gestionar filas de espera, optimizando la atención al cliente y reduciendo los problemas de desorganización. El uso de **C++** permite implementar una solución robusta y eficiente basada en estructuras de datos.
