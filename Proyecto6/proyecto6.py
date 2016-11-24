from math import log

__author__ = 'Leonardo Niels Pardi bm0068 y Alejandro Mendez Fernandez bm0059'


class IOManager:
    """ Gestor de entrada y salida del programa. """

    def __init__(self, file_input, file_output):
        self.__f_input = open(file_input, 'r')
        self.__f_output = open(file_output, 'w')

    def read_line(self):
        return self.__f_input.readline().strip('\n')

    def write_line(self, line):
        self.__f_output.write(line + "\n")

    @staticmethod
    def print_text(text):
        print text

    def close_file(self):
        self.__f_input.close()
        self.__f_output.close()


class NodoArbol:
    """ Nodo del arbol de decision
        __tipo_atr: 0 = cadena, 1 = entero
    """

    __nodo_izq = None   # Por defecto los nodos
    __nodo_der = None   # apuntan a 'null'

    def __init__(self, clave, tipo=0):
        self.__clave = clave
        self.__tipo_atr = tipo

    def get_clave(self):
        return self.__clave

    def get_nodo_izq(self):
        return self.__nodo_izq

    def set_nodo_izq(self, nodo):
        self.__nodo_izq = nodo

    def get_nodo_der(self):
        return self.__nodo_der

    def set_nodo_der(self, nodo):
        self.__nodo_der = nodo

    def get_tipo_atr(self):
        return self.__tipo_atr


class Arbol:
    """
    Arbol binario de decision.
    Genera el arbol de decision.
    """

    def __init__(self):
        self.__raiz = NodoArbol("")  # Se inicializa la raiz.

    def generar_arbol(self, lista_ejemplos, lista_atributos, lista_valores, lista_tipo):
        """
        Lanzadera del algoritmo principal que se encarga de inicializar la raiz.
        """

        valores_positivos = 0
        valores_negativos = 0

        for ejemplo in lista_ejemplos:      #Contamos los valores True y False del conjunto de ejemplos
            if ejemplo[-1] == 'True':
                valores_positivos += 1
            else:
                valores_negativos += 1

        if valores_positivos == 0:      # Si todos los ejemplos son negativos devolver un nodo negativos
            self.__raiz = NodoArbol('False')
        elif valores_negativos == 0:    # Si todos los ejemplos son positivos devolver un nodo positivos
            self.__raiz = NodoArbol('True')
        elif len(lista_atributos) == 0:  # Si atributos esta vacio devolver un nodo con el voto mayoritario
            self.__raiz = NodoArbol(self.__resul_mayoritario(lista_ejemplos))
        else:                                   #En otro caso escogemos el mejor atributo como nodo raiz
            if lista_tipo[lista_atributos[0]] == 1:
                self.__raiz = NodoArbol(lista_atributos[0], 1)  # Asignacion de nodo tipo numerico
            else:
                self.__raiz = NodoArbol(lista_atributos[0])     # Asignacion de nodo tipo string

            valor_1 = ()
            valor_2 = ()
            # Recuento de valores en los ejemplos:
            if lista_tipo[lista_atributos[0]] == 1:  # Para atributos de tipo numerico
                for ejemplo in lista_ejemplos:
                    if ejemplo[lista_atributos[0]] <= lista_valores[lista_atributos[0]][0]:
                        valor_1 += (ejemplo,)
                    else:
                        valor_2 += (ejemplo,)
            else:   # Para atributos de tipo string
                for ejemplo in lista_ejemplos:
                    if ejemplo[lista_atributos[0]] == lista_valores[lista_atributos[0]][0]:
                        valor_1 += (ejemplo,)
                    else:
                        valor_2 += (ejemplo,)

            if len(valor_1) == 0:       # Si el subconjunto de ejemplos del primer valor esta vacio voto mayoritario
                self.__raiz.set_nodo_izq(NodoArbol(self.__resul_mayoritario(lista_ejemplos)))   # en nodo hijo
                self.__raiz.set_nodo_der(self.__algoritmo_id3(valor_2, lista_atributos[1:], lista_valores, lista_tipo))
                # Para el nodo hijo derecho se llama recursivamente al algoritmo id3 con el subconjunto de ejemplos
                # Que tienen el segundo valor y quitando el mejor de la lista de atributos
            elif len(valor_2) == 0:     # Se presenta la misma situacion con el segundo valor como subconjunto vacio
                self.__raiz.set_nodo_der(NodoArbol(self.__resul_mayoritario(lista_ejemplos)))
                self.__raiz.set_nodo_izq(self.__algoritmo_id3(valor_1, lista_atributos[1:], lista_valores, lista_tipo))
            else:   # En el caso de que ninguno de los subconjunto de valores sea vacio se llamara recursivamente
                    # al algoritmo id3 enviando el subconjunto de valores
                self.__raiz.set_nodo_izq(self.__algoritmo_id3(valor_1, lista_atributos[1:], lista_valores, lista_tipo))
                self.__raiz.set_nodo_der(self.__algoritmo_id3(valor_2, lista_atributos[1:], lista_valores, lista_tipo))

    def __algoritmo_id3(self, lista_ejemplos, lista_atributos, lista_valores, lista_tipo):

        val_pos = 0
        val_neg = 0

        for ejemplo in lista_ejemplos:     # Se hace el recuento del valor objetivo en el conjunto de elementos recibidos
            if ejemplo[-1] == 'True':
                val_pos += 1
            else:
                val_neg += 1

        if val_pos == 0:        # Si todos los ejemplos son negativos devolver un nodo negativos
            nodo = NodoArbol('False')
        elif val_neg == 0:      # Si todos los ejemplos son positivos devolver un nodo positivos
            nodo = NodoArbol('True')
        elif len(lista_atributos) == 0:     # Si atributos esta vacio devolver un nodo con el voto mayoritario
            nodo = NodoArbol(self.__resul_mayoritario(lista_ejemplos))
        else:
            val_1 = ()
            val_2 = ()
            # Recuento de valores en los ejemplos:
            if lista_tipo[lista_atributos[0]] == 1:     # Para atributos de tipo numerico
                for ejemplo in lista_ejemplos:
                    if ejemplo[lista_atributos[0]] <= lista_valores[lista_atributos[0]][0]:
                        val_1 += (ejemplo,)
                    else:
                        val_2 += (ejemplo,)
            else:       # Para atributos de tipo string
                for ejemplo in lista_ejemplos:
                    if ejemplo[lista_atributos[0]] == lista_valores[lista_atributos[0]][0]:
                        val_1 += (ejemplo,)
                    else:
                        val_2 += (ejemplo,)
            # Colocamos el mejor atributo en el nodo:
            if lista_tipo[lista_atributos[0]] == 1:     # Senialamos en el nodo si es numerico
                nodo = NodoArbol(lista_atributos[0], 1)
            else:                                       # o de tipo string
                nodo = NodoArbol(lista_atributos[0])

            if len(val_1) == 0:     # Si el subconjunto de ejemplos del primer valor esta vacio voto mayoritario
                nodo.set_nodo_izq(NodoArbol(self.__resul_mayoritario(lista_ejemplos)))      # en nodo hijo
                nodo.set_nodo_der(self.__algoritmo_id3(val_2, lista_atributos[1:], lista_valores, lista_tipo))
                # Para el nodo hijo derecho se llama recursivamente al metedo con el subconjunto de ejemplos
                # que tienen el segundo valor y quitando el mejor atributo de la lista
            elif len(val_2) == 0:   # Se presenta la misma situacion con el segundo valor como subconjunto vacio
                nodo.set_nodo_der(NodoArbol(self.__resul_mayoritario(lista_ejemplos)))
                nodo.set_nodo_izq(self.__algoritmo_id3(val_1, lista_atributos[1:], lista_valores, lista_tipo))
            else:   # En el caso de que ninguno de los subconjunto de valores sea vacio se llamara recursivamente
                    # al metodo enviando el subconjunto de valores
                nodo.set_nodo_izq(self.__algoritmo_id3(val_1, lista_atributos[1:], lista_valores, lista_tipo))
                nodo.set_nodo_der(self.__algoritmo_id3(val_2, lista_atributos[1:], lista_valores, lista_tipo))

        return nodo

    @staticmethod
    def __resul_mayoritario(lista_ejemplo):     # Devuelve el valor objetivo mayoritario de la conjunto de ejemplos
                                                # recibido
        voto_pos = 0
        voto_neg = 0

        for i in lista_ejemplo:     # Se hace el recuento de valores objetivo
            if i[:-1] == 'True':
                voto_pos += 1
            else:
                voto_neg += 1

        if voto_pos > voto_neg:     # Solo si el numero de valores objetivo positivo es mayor estrictamente que el de
            resul = 'True'          # negativos se devuelve un True considerando asi que cuando el numero de Trues
        else:                       # y Falses son iguales se devuelve un resultado pesimista ( False )
            resul = 'False'

        return resul

    def __preorden(self, nodo, lista_valores, lista_tipo):   # Metodo recursivo que devuelve un string con el formato
        text = ""                                            # de salida del arbol en preorden
        if nodo.get_clave() != 'False' and nodo.get_clave() != 'True':
            if nodo.get_tipo_atr() == 1:    # Si el nodo en el que nos hallamos no es hoja y ademas es de tipo entero
                text += "["                 # casteamos su clave ( el atributo ) y su valor discriminatorio de entero
                text += str(nodo.get_clave()) + ", "    # a string
                text += str(lista_valores[nodo.get_clave()][0]) + ", "
                text += self.__preorden(nodo.get_nodo_izq(), lista_valores, lista_tipo) + ", "  # Los nodos hijos se
                text += self.__preorden(nodo.get_nodo_der(), lista_valores, lista_tipo) # obtendran de la llamada
                text += "]"                                                             # recursiva
            else:       # En caso de que la clave sea un atributo con valores de tipo string solo se castea el numero
                text += "["     # del atributo
                text += str(nodo.get_clave()) + ", "
                text += lista_valores[nodo.get_clave()][0] + ", "
                text += lista_valores[nodo.get_clave()][1] + ", "
                text += self.__preorden(nodo.get_nodo_izq(), lista_valores, lista_tipo) + ", "
                text += self.__preorden(nodo.get_nodo_der(), lista_valores, lista_tipo)
                text += "]"
        else:   # Si estamos en el nodo hijo devolvemos su clave que sera False o True
            text = nodo.get_clave()

        return text

    def to_string(self, lista_valores, lista_tipo):     # Metodo to string que invoca al metodo preorden
        return self.__preorden(self.__raiz, lista_valores, lista_tipo)


class DataBase:
    """
    Obtiene, almacena y procesa los datos.
    """
    __arbol = Arbol()

    def __init__(self, data_in, data_out):  # En este metodo se inicializan las listas con las que almacenaremos
        self.__gestor = IOManager(data_in, data_out)    # y operaremos los datos recibidos
        self.__atributos = []
        self.__tipo_atrib = ()
        self.__val_atrib = ()
        self.__tabla_datos = ()

    def fill_data(self):    # Aqui se almacenara los datos del fichero recibido en las correspondientes listas
        num_atrib = int(self.__gestor.read_line())  # Cargamos el numero de atributos de la tabla
        self.__atributos = self.__list_atr(num_atrib)   # Inicializamos la lista de atributos en orden
                                                        # (0, 1, ..., num_atrib-1) llamando a un metodo list_atr
        for i in range(num_atrib - 1):      # Cargamos los valores de los atributos salvo el atributo objetivo
            linea = self.__gestor.read_line()   # Guardamos en un string la linea del fichero leida
            if linea is 's':       # Si el atributo es de tipo string lo almacenamos como un 0 en la tupla de tipos
                self.__tipo_atrib += (0,)   # de atributos 'tipo_atrib'
                aux = (self.__gestor.read_line(),)  # Almacenamos los valores en una tupla auxiliar para despues
                aux += (self.__gestor.read_line(),) # guardarla como subtupla dentro de val_atrib
                self.__val_atrib += (aux,)
            else:       # Si el atributo es de tipo entero almacenamos un 1 en la lista de tipos y solo el valor
                self.__tipo_atrib += (1,)   # discriminatorio en la lista de valores
                self.__val_atrib += ((int(self.__gestor.read_line()),),)

        self.__tipo_atrib += (self.__gestor.read_line(),)   # Guardamos el tipo booleano en la lista de tipos y
        self.__val_atrib += (('True', 'False'),)            # sus valores en la lista de valores

        num_ejemplos = int(self.__gestor.read_line())   # Ahora comenzamos a capturar los valores de cada uno de los
                                                        # ejemplos en la tupla tabla_datos
        for i in range(num_ejemplos):   # Para cada uno de los ejemplos de la tabla recibida
            tabla_aux = ()
            for j in range(num_atrib):  # leemos sus valores segun su tipo de atributo
                if self.__tipo_atrib[j] == 1:
                    tabla_aux += (int(self.__gestor.read_line()),)  # y lo almacenamos como subtupla en una tupla
                else:                                               # auxiliar
                    tabla_aux += (self.__gestor.read_line(),)
            self.__tabla_datos += (tabla_aux,)      # para despues cargarla en la tupla de datos

    @staticmethod
    def __list_atr(num_atrib):  # Metodo que devuelve una lista con el numero del atributo como identificador
        lista = []              # de 0 a num_atrib-1, (0, 1, 2, ..., num_atrib-1)

        for i in range(num_atrib - 1):
            lista += [i]

        return lista

    def sintesis_datos(self):   # Este metodo utilizando los datos recibidos y almacenados en las corresponientes tuplas
                                # para calcular la entropia para la ganancia de informacion y con ello iniciar el
        gain_list = []          # algoritmo ID3 con los datos necesarios
        entropy_obj = 0.0
        # Iniciamos la lista de ganancia y la entropia objetivo
        val_pos = 0
        val_neg = 0
        total_elem = 0.0    # Inicializamos el numero total de elementos como float para poder realizar la division
        for dato in self.__tabla_datos:     # Contamos los valores positivos/negativos de los ejemplos
            total_elem += 1
            if dato[-1] == 'True':
                val_pos += 1
            else:
                val_neg += 1

        if val_neg != 0 and val_pos != 0:   # Si se da el caso en que uno de los valores sea 0 entonces la entropia
                                            # objetivo se dejara como 0 en caso contrario la calculamos
            entropy_obj += -(val_pos / total_elem) * (log(val_pos / total_elem) / log(2)) - (val_neg / total_elem) * (
                log(val_neg / total_elem) / log(2))

        num_atrib = len(self.__atributos)
        for i in range(num_atrib):      # Ahora calculamos el resto de entropias de cada atributo
            entropy_list = ()

            if self.__tipo_atrib[i] == 1:   # Si el atributo es un entero
                for j in range(len(self.__val_atrib[i])):
                    entropy_list += self.__entropy_int(i, j)    # Llamamos al metodo entropy_int que devolvera una
                                                                # lista de las entropias de los valores
            else:   # Si el atributo es un string calculamos la entropia de cada valor del atributo
                for j in range(len(self.__val_atrib[i])):
                    entropy_list += self.__entropy(i, j)
            entropy_list += entropy_obj,    # Guardamos en la ultima posicion de la lista de entropias la entropia
                                            # objetivo que sera necesaria para calcular la ganacia de informacion
            if self.__tipo_atrib[i] == 1:       # Ahora llamamos al metodo que devolvera la ganancia del atributo
                aux = self.__gain_int(entropy_list, i)  # pasando la lista de entropias y el indice del atributo
            else:   # Uno de los metodos calcula la ganancia en base a un atributo de tipo entero el otro por el tipo
                aux = self.__gain(entropy_list, i)      # string

            gain_list += [aux]      # Finalmente guardamos las ganacias de informacion en la lista gain_list que tendra
                                    # las ganacias ordenadas por la posicion del atributo
        self.__sort_data(gain_list, num_atrib)  # Se llama al algoritmo de ordenacion que ordenara la lista de atributos
                                                # en funcion de la lista de ganancia
        self.__arbol.generar_arbol(self.__tabla_datos, self.__atributos, self.__val_atrib, self.__tipo_atrib)
        # Para acabar se llamara al metodo para generar el arbol de decision
    def __entropy_int(self, i_atributo, i_valor):   # Metodo que devuelve una tupla con la entropia de los valores
        resul = ()                                  # del atributo entero

        val_pos = 0
        val_neg = 0
        total_elem = 0.0
        for dato in self.__tabla_datos:     # Se cuentan los valores objetivo en base al valor menor o igual al
            if dato[i_atributo] <= self.__val_atrib[i_atributo][i_valor]:   # discriminador
                total_elem += 1
                if dato[-1] == 'True':
                    val_pos += 1
                else:
                    val_neg += 1

        if val_neg == 0 or val_pos == 0:    # En caso de no haber un valor positivo o negativo la entropia sera 0
            resul += (0.0,)
        else:   # Sino se calculara la entropia del valor menor o igual al discriminador
            resul += (-(val_pos / total_elem) * (log(val_pos / total_elem) / log(2)) - (val_neg / total_elem) * (
                log(val_neg / total_elem) / log(2)),)
        # Se repite el mismo proceso para los valores mayores estrictamente del discriminador
        val_pos = 0
        val_neg = 0
        total_elem = 0.0
        for dato in self.__tabla_datos:
            if dato[i_atributo] > self.__val_atrib[i_atributo][i_valor]:
                total_elem += 1
                if dato[-1] == 'True':
                    val_pos += 1
                else:
                    val_neg += 1

        if val_neg == 0 or val_pos == 0:
            resul += 0.0,
        else:
            resul += -(val_pos / total_elem) * (log(val_pos / total_elem) / log(2)) - (val_neg / total_elem) * (
                log(val_neg / total_elem) / log(2)),

        return resul

    def __entropy(self, i_atributo, i_valor):   # Metodo que devuelve la entropia del valor string de un atributo
        val_pos = 0
        val_neg = 0
        total_elem = 0.0

        for dato in self.__tabla_datos:     # Se cuentan los valores objetivo de los ejemplos con el valor pasado
            if dato[i_atributo] == self.__val_atrib[i_atributo][i_valor]:
                total_elem += 1
                if dato[-1] == 'True':
                    val_pos += 1
                else:
                    val_neg += 1
        # Se calcula y devuelve la entropia del valor pasado
        if val_neg == 0 or val_pos == 0:
            return 0.0,

        return -(val_pos / total_elem) * (log(val_pos / total_elem) / log(2)) - (val_neg / total_elem) * (
            log(val_neg / total_elem) / log(2)),

    def __gain_int(self, entropy_list, i_atributo): # Este metodo devuelve la ganacia del atributo entero
        suma = 0.0

        apariciones = 0.0
        for dato in self.__tabla_datos:     # Se calcula el peso del valor menorigual al discriminador por
            if dato[i_atributo] <= self.__val_atrib[i_atributo][0]:     # la entropia de ese valor y se almacena en
                apariciones += 1                                        # la variable suma
        suma += (apariciones / len(self.__tabla_datos)) * entropy_list[0]

        apariciones = 0.0
        for dato in self.__tabla_datos:     # Se calcula el peso del valor mayorestricto al discriminador por la
            if dato[i_atributo] > self.__val_atrib[i_atributo][0]:  # entropia de ese valor y se almacena en la variable
                apariciones += 1                                    # suma
        suma += (apariciones / len(self.__tabla_datos)) * entropy_list[1]

        return entropy_list[-1] - suma  # Se devuelve el resultado de la formula de la ganancia

    def __gain(self, entropy_list, i_atributo): # Al igual que el anterior devuelve la ganancia del atributo string
        suma = 0.0

        for i in range(len(self.__val_atrib[i_atributo])):  # Se calcula el peso del primer y segundo valor del atributo
            apariciones = 0.0                               # string por la entropia de ese valor
            for dato in self.__tabla_datos:
                if dato[i_atributo] == self.__val_atrib[i_atributo][i]:
                    apariciones += 1
            suma += (apariciones / len(self.__tabla_datos)) * entropy_list[i]
        return entropy_list[-1] - suma      # Se devuelve el resultado de la formula de la ganancia

    def __sort_data(self, gain_list, num_atrib):    # Metodo de algoritmo de ordenacion por seleccion que ordena la
        for i in range(num_atrib):                  # lista de atributos en funcion de los valores de la lista de
            k = i                                   # ganancia de informacion
            for j in range(i + 1, num_atrib):
                if gain_list[j] > gain_list[k]:
                    k = j
            aux = self.__atributos[i]
            self.__atributos[i] = self.__atributos[k]
            self.__atributos[k] = aux
            aux = gain_list[i]
            gain_list[i] = gain_list[k]
            gain_list[k] = aux

    def mostrar(self):      # Metodo que muestra en consola el arbol
        self.__gestor.print_text(self.__arbol.to_string(self.__val_atrib, self.__tipo_atrib))

    def guardar(self):      # Metodo que escribe el arbol de decision en el fichero deseado y cierra el fichero
        self.__gestor.write_line(self.__arbol.to_string(self.__val_atrib, self.__tipo_atrib))
        self.__gestor.close_file()


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        data = DataBase("data.txt", "resul.txt")
        data.fill_data()
        data.sintesis_datos()
        data.mostrar()
        data.guardar()


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"
