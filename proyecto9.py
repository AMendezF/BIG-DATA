from math import sqrt
__author__ = 'Alejandro Mendez Fernandez (bm0058) y Leonardo Niels Pardi (bm0068)'


class IOManager:
    """
    Gestor de entrada y salida del programa.
    """

    def __init__(self, file_input, file_output):
        try:
            self.__f_input = open(file_input, 'r')
            self.__f_output = open(file_output, 'w')
        except IOError:
            self.print_text("No such file or directory: 'data.txt'")

    def get_f_in(self):
        return self.__f_input

    def get_f_out(self):
        return self.__f_output

    def read_line(self):
        """
        Retorna una linea en el fichero.
        """
        try:
            return self.get_f_in().readline().strip('\n')

        except ValueError:
            self.print_text("Oops! Valor invalido o no hay datos.")

        except EOFError:
            self.print_text("Final del fichero. No more data")

    def write_line(self, line):
        """
        Imprime en fichero.
        :param line: texto a imprimir.
        """
        try:
            self.get_f_out().write(line + "\n")
        except:
            self.print_text("Error at write on file")

    @staticmethod
    def print_text(text):
        """
        Imprime por la salida por defecto.
        :param text: texto a imprimir
        """
        print text

    def close_file(self):
        self.get_f_in().close()
        self.get_f_out().close()


class DataBase:
    """
    Obtiene y almacena datos.
    """

    def __init__(self, gestor):
        """
        :param gestor: gestorIO.
        """
        self.__gestor = gestor
        self.__puntos = []       # Lista conjunto de puntos

    def fill_data(self):
        """
        Obtiene los datos del fichero.
        """
        num_puntos = int(self.__gestor.read_line())     # Numero de puntos
        dimension = int(self.__gestor.read_line())      # Dimension de los puntos

        for i in range(num_puntos):   # Obtencion de los puntos
            lista_aux = ()
            for j in range(dimension):
                lista_aux += int(self.__gestor.read_line()),
            self.__puntos += [lista_aux]

    def get_puntos(self):
        return self.__puntos

    def to_string(self):
        """
        Formatea a texto los datos.
        """
        return str(self.__puntos)


class NodoArbol:
    """
    Nodo del arbol de clusters.
    """

    def __init__(self, clave, izq, der):
        """
        :param clave: clave o nombre del nodo.
        :param izq: nodo hijo por la izquierda.
        :param der: nodo hijo por la derecha.
        """
        self.__clave = clave
        self.__nodo_izq = izq
        self.__nodo_der = der

    def get_clave(self):
        return self.__clave

    def get_izq(self):
        return self.__nodo_izq

    def get_der(self):
        return self.__nodo_der

    def set_izq(self, nodo):
        self.__nodo_izq = nodo

    def set_der(self, nodo):
        self.__nodo_der = nodo


class Arbol:
    """
    Arbol binario de decision.
    """

    def __init__(self, data_in, data_out):
        """
        :param data_in: fichero de texto de entrada.
        :param data_out: fichero de texto de salida.
        """
        self.__gestor = IOManager(data_in, data_out)    # GestorIO
        self.__raiz = NodoArbol([], None, None)         # Inicializar raiz arbol
        self.__datos = DataBase(self.__gestor)          # Almacen de datos de entrada
        self.__datos.fill_data()                        # Rellenar almacen de datos

    def __distancia_euclidea(self, cluster1, cluster2):
        """
        Calcula la distancia euclidea entre dos clusters.
        :param cluster1: cluster de puntos 1.
        :param cluster2: cluster de puntos 2.
        """
        dimension = len(self.__datos.get_puntos()[0])   # Dimension de los puntos (2D,3D...)
        cluster1_size = len(cluster1)
        cluster2_size = len(cluster2)

        distancia = 0
        for i in range(cluster1_size):      # Sumatorio de las distancias entre
            for j in range(cluster2_size):  # todos los puntos de ambos clusters.
                cluster1_point = self.__datos.get_puntos()[cluster1[i]]
                cluster2_point = self.__datos.get_puntos()[cluster2[j]]
                sumatorio = 0
                for k in range(dimension):  # Para cada dimension
                    sumatorio += (cluster1_point[k] - cluster2_point[k]) ** 2
                distancia += sqrt(sumatorio)

        return distancia / (cluster1_size * cluster2_size)

    def clusters_union(self):
        """
        Crea el arbol de clusters de puntos
        en funcion de la distancia euclidea.
        """
        cantidad_clusters = len(self.__datos.get_puntos())  # Cantidad inicial de clusters

        index_clusters = []
        for i in range(cantidad_clusters):    # Lista inicial de los indices de los clusters
            index_clusters += [[i]]

        clusters_list = []
        for i in range(cantidad_clusters):    # Lista inicial de nodos clusters (Nodos Hoja)
            clusters_list += [NodoArbol([i], None, None)]

        while len(index_clusters) > 1:  # Mientras queden clusters por unir
            smallest_distance = self.__distancia_euclidea(index_clusters[0], index_clusters[1])
            index_points = [0, 1]   # Indices de los puntos con menor distancia

            for i in range(cantidad_clusters):                # Compara todos los clusters
                for j in range(i + 1, cantidad_clusters):     # entre si.
                    distance = self.__distancia_euclidea(index_clusters[i], index_clusters[j])
                    if distance < smallest_distance:    # Si encontramos distancia menor entre puntos
                        smallest_distance = distance
                        index_points = [i, j]

            # Composicion del nuevo cluster:
            clave_nodo = index_clusters[index_points[0]] + index_clusters[index_points[1]]
            nodo_izq = clusters_list[index_points[0]]
            nodo_der = clusters_list.pop(index_points[1])
            clusters_list[index_points[0]] = NodoArbol(clave_nodo, nodo_izq, nodo_der)

            index_clusters[index_points[0]] += index_clusters.pop(index_points[1])

            cantidad_clusters -= 1    # Al haber unificado 2 clusters reducimos en 1 la cantidad restante

        self.__raiz = clusters_list[0]  # Nodo raiz del arbol

    def to_string(self):
        """
        Retorna en formato texto el arbol.
        """
        return self.__pre_orden(self.__raiz)

    def __pre_orden(self, nodo):
        """
        Retorna las claves recorriendo el arbol en preorden.
        :param nodo: nodo actual del arbol.
        """
        text = ""
        if nodo is not None:
            text += "[" + str(nodo.get_clave()) + ", "
            text += self.__pre_orden(nodo.get_izq())
            text += self.__pre_orden(nodo.get_der())
            text += "]"
        return text

    def mostrar(self):
        """
        Muestra en la salida por defecto los puntos y el arbol.
        """
        self.__gestor.print_text("Puntos: " + self.__datos.to_string())
        self.__gestor.print_text("Arbol: " + self.to_string())

    def exportar(self):
        """
        Exporta los datos al fichero.
        """
        self.__gestor.write_line(self.to_string())
        self.__gestor.close_file()


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        arbol = Arbol("data.txt", "resul.txt")
        arbol.clusters_union()
        arbol.mostrar()
        arbol.exportar()


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"
