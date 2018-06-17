
# coding: utf-8

from data import ruta, orden, campos, carreras
from flask import Flask, jsonify, request, abort
from json import loads
import sys


# ## Definición de funciones.

# ### Funciones de gestión de la base de datos.
# 
# En este caso la base de datos no es otra cosa más que un archivo de texto que representa a un objeto de tipo *list* de Python. 
# 
# La base de datos puede ser consultada en [data/alumnos.txt](data/alumnos.txt). 

# ### Función de carga de datos.


def carga_base(ruta):
    with open(ruta, 'tr') as base:
        return eval(base.read())


# ### Función de escritura de datos.



def escribe_base(lista ,ruta):
    with open(ruta, 'wt') as base:
            base.write(str(lista))


# ### Función de búsqueda en la base de datos.
# * Busca dentro del campo *'Cuenta'* de cada elemento de *base* al número entero correspondiente al argumento de *cuenta*.
# * En caso de encontrar una coincidencia, regresa al elemento.
# * En caso de no encontrar coincidencia regresa *False*.


def busca_base(cuenta, base):
    for alumno in base:
        try:
            if alumno['Cuenta'] == int(cuenta):
                return alumno
        except:
            return False
    return False


# ## Funciones de validación de datos.

# ### Función que valida el tipo de dato.


def es_tipo(dato, tipo):
    tipo = eval(tipo)
    if tipo == str:
        return True
    else:
        try: 
            return tipo(dato) is dato
        except:
            return False


# ### Función que valida las reglas de los datos.
# * Los campos *'Nombre"* y *'Primer Apellido'* no deben de ser una cadena de caracteres vacía.
# * El campo 'Semestre' debe de ser un entero mayor a 1.
# * La cadena de caracteres del campo 'Carrera' debe de estar dentro de las cadenas listadas en *datos.carrera*.
# * El campo promedio debe de ser un número entre 0 y 10.


def reglas(dato, campo):
    if campo == "Carrera" and dato not in carreras:
        return False
    elif campo == "Semestre" and dato < 1:
        return False
    elif campo == "Promedio" and (dato < 0 or dato > 10):
        return False
    elif (campo in ("Nombre", "Primer Apellido") and (dato == "")):
        return False
    else:
        return True           


# ### Función de validación de tipos y reglas.


def valida(dato, campo):
    return es_tipo(dato, campos[campo][0]) and reglas(dato, campo)


# ### Función que valida que el mensaje contiene todos los campos obligatorios.


def recurso_completo(base, ruta, cuenta, peticion):
    try:
        candidato = {'Cuenta': int(cuenta)}
        registro = loads(peticion.decode(encoding="utf-8"))
        if (set(registro)).issubset(set(orden)):
            for campo in orden:
                if not campos[campo][1] and campo not in registro:
                    candidato[campo] = ''
                elif valida(registro[campo], campo):
                    candidato[campo] = registro[campo]      
                else:
                    abort(401)
        else:
            abort(402)
    except:
        abort(403)
            
    base.append(candidato)
    escribe_base(base, ruta)
    return jsonify(candidato)


# ## Código del servidor.
# 
# * El servidor correrá en [localhost:5000/api/](localhost:5000/api/). Si se accede a la raíz, se desplegará un listado de todos los alumnos en formato JSON.
# * El servidor soporta los métodos:
#     * **GET**: para obtener la información de un alumno por su número de cuenta.
#     * **POST**: para crear un registro nuevo.
#     * **PUT**: para sustituir por completo un registro existente.
#     * **PATCH**: para modificar ciertos datos de un registro existente.
#     * **DELETE**: para eliminar un registro existente.


app = Flask(__name__)


@app.route('/')
def index():
    print(campos)
    return str(campos)

@app.route('/api/', methods=['GET'])
def api_raiz():
    with open(ruta, 'tr') as base:    
        return jsonify(eval(base.read()))

    
@app.route('/api/<cuenta>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def api(cuenta):
    
    if request.method == 'GET':
        base = carga_base(ruta)
        alumno = busca_base(cuenta, base)
        if alumno:
            return jsonify(alumno)
        else:
            abort(404)
            
    if request.method == 'DELETE':               
        base = carga_base(ruta)
        alumno = busca_base(cuenta, base)
        if alumno:
            base.remove(alumno)
            escribe_base(base, ruta)
            return jsonify(alumno)
        else:
            abort(404)
        
    if request.method == 'POST':
        base = carga_base(ruta)
        alumno = busca_base(cuenta, base)
        if alumno:
            abort(409)
        else:
            return recurso_completo(base, ruta, cuenta, request.data)
            
    if request.method == 'PUT':
        base = carga_base(ruta)
        alumno = busca_base(cuenta, base)
        if not alumno:
            abort(404)
        else:
            base.remove(alumno)
            return recurso_completo(base, ruta, cuenta, request.data)

    if request.method == 'PATCH':               
        base = carga_base(ruta)
        alumno = busca_base(cuenta, base)
        if not alumno:
            abort(404)
        else:
            indice = base.index(alumno)
            try:
                peticion = loads(request.data.decode(encoding="utf-8"))
                if (set(peticion)).issubset(set(orden)):
                    for campo in peticion:
                        dato = peticion[campo]
                        if valida(dato, campo):
                            alumno[campo] = dato
                        else:
                            abort(401)
                else:
                    abort(402)
            except:
                abort(403)
            base[indice] = alumno
            escribe_base(base, ruta)
            return jsonify(alumno)


if __name__ == '__main__':
    app.run('0.0.0.0')