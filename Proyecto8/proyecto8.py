__author__ = 'Leonardo Niels Pardi bm0068 y Alejandro Mendez Fernandez bm0059'


class IOManager:
    """ Gestor de entrada y salida del programa. """

    def __init__(self, file_input, file_output):
        self.__f_input = open(file_input, 'r')
        self.__f_output = open(file_output, 'w')

    def get_f_in(self):
        return self.__f_input

    def get_f_out(self):
        return self.__f_output

    def read_line(self):
        return self.get_f_in().readline().strip('\n')

    def write_line(self, line):
        self.get_f_out().write(line + "\n")

    @staticmethod
    def print_text(text):
        print text

    def close_file(self):
        self.get_f_in().close()
        self.get_f_out().close()


class DataBase:
    """
    Obtiene, almacena y procesa los datos.
    """

    def __init__(self, data_in, data_out):
        self.__gestor = IOManager(data_in, data_out)
        self.__puntos = ()       # Conjunto de datos de entrada
        self.__k = 0
        self.__matriz_datos = []
        self.__matriz_indice = []
        self.__resultado = []   # Pareja de resultados
        self.elj = 0

    def colect_datos(self):
        self.__k = int(self.__gestor.read_line())
        n_puntos = int(self.__gestor.read_line())

        self.__matriz_datos = [[0] * n_puntos for i in range(self.__k)]
        self.__matriz_indice = [[0] * n_puntos for i in range(self.__k)]

        for i in range(n_puntos):
            self.__puntos += float(self.__gestor.read_line()),

    def procesar_datos(self):
        """
        Aplicacion del algoritmo para hallar la solucion optima
        """
        for m in range(1, self.__k + 1):                # Para cada cluster:
            self.elj = m                                    # Valor actual del cluster a calcular
            for i in range(1, len(self.__puntos) + 1):      # Para cada punto:
                self.__matriz_datos[m-1][i-1] = self.__algoritmo(i, m)  # Guardamos el resultado numerico en la matriz

        self.__salida_algoritmo()

    def __algoritmo(self, i, m):
        """
        Calculo de la solucion optima mediante algoritmo recursivo
        """
        if i <= m:      # Caso base
            return 0.0

        elif m > 1:     # Para los cluster distintos del primero
            lista_distancias = []   # Lista contenedor de las distancias
            for j in range(m, i+1):     # Para cada valor de 'm' a 'i'

                suma = 0.0
                for punto in self.__puntos[j-1:i]:  # Calculo del promedio de los puntos
                    suma += punto

                promedio = (1.0 / len(self.__puntos[j-1:i])) * suma     # Almacenamiento del promedio

                sumatorio = 0
                for k in range(j, i+1):     # Calculo de la suma de las distancias al cuadrado
                    sumatorio += (self.__puntos[k-1] - promedio)**2

                lista_distancias += [round(self.__algoritmo(j-1, m-1) + sumatorio, 2)]  # Almacenar posible solucion
            if m == self.elj:   # Si nos encontramos en el valor del cluster a calcular:
                x = min(lista_distancias)   # Buscamos la solucion optima (minima)
                self.__matriz_indice[m-1][i-1] = lista_distancias.index(x) + m  # Almacenamos el indice del subconjunto
                return x    # Devolvemos el valor minimo
            return min(lista_distancias)    # Devolvemos el valor minimo

        else:   # Para m = 1 (el primer cluster)
            suma = 0.0
            for punto in self.__puntos[m-1:i]:  # Calculo del promedio
                suma += punto

            promedio = (1.0 / len(self.__puntos[m-1:i])) * suma     # Almacenamiento del promedio

            sumatorio = 0
            for k in range(m, i+1):     # Calculo de la suma de las distancias al cuadrado
                sumatorio += (self.__puntos[k-1] - promedio)**2

            return round(sumatorio, 2)  # Retorno de la suma de las distancias al cuadrado

    def __salida_algoritmo(self):
        self.__resultado += [self.__matriz_datos[self.__k - 1][len(self.__puntos) - 1]]     # Colocamos en la lista de
                                                                                            # resultados la solucion
        m = self.__k    # Inicializamos los indices de la matriz                            # optima
        i = len(self.__puntos)
        while m > 1:
            self.__resultado += [self.__matriz_indice[m-1][i-1]]    # Almacenamos los indice j del elemento mas
            i = self.__matriz_indice[m-1][i-1] - 1                  # pequenio del cluster
            m -= 1

        self.__resultado += [1]

    def to_string(self):
        """
        Metodo para mostrar los datos
        """
        text = "Solucion optima: " + str(self.__resultado[0]) + "\n"      # Colocamos la solucion optima y despues los
        for i in reversed(self.__resultado[1:]):                          # indices del primer elemento de los
            text += "Indice de Subconjunto: " + str(i) + "\n"                       # subconjuntos

        self.__gestor.print_text(text)  # Pintamos el resultado en consola

    def exportar(self):
        """
        Metodo para exportar los datos
        """
        text = str(self.__resultado[0]) + "\n"                           # Idem a to_string
        for i in reversed(self.__resultado[1:]):
            text += str(i) + "\n"
        self.__gestor.write_line(text)                                   # Grabamos en el fichero de salida
        self.__gestor.close_file()                                       # Cerramos


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        data = DataBase("data.txt", "resul.txt")
        data.colect_datos()
        data.procesar_datos()
        data.to_string()
        data.exportar()


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"
