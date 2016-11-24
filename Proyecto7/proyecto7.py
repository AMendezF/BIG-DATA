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
        self.__datos = ()       # Conjunto de datos de entrada, organizados en diccionarios
        self.__claves = ()      # Subconjunto de datos
        self.__resultado = ()   # Pareja de resultados posanalisis

    def fill_data(self):
        num_atrib = int(self.__gestor.read_line())      # Numero de atributos
        num_ejemplos = int(self.__gestor.read_line())   # Numero de ejemplos

        for i in range(num_atrib):      # Reservar tantos diccionarios como atributos
            self.__datos += {},

        for i in range(num_ejemplos):   # Obtencion de los datos
            lista_aux = []
            for j in range(num_atrib):
                lista_aux += [int(self.__gestor.read_line())]

            atributo_objetivo = self.__gestor.read_line()

            for j in range(num_atrib):      # Almacenamiento de los datos en diccionarios
                if lista_aux[j] in self.__datos[j]:
                    self.__datos[j][lista_aux[j]] += [atributo_objetivo]
                else:
                    self.__datos[j][lista_aux[j]] = [atributo_objetivo]

        for i in range(num_atrib):      # Copia de las claves de cada diccionario
            self.__claves += sorted(self.__datos[i]),

    def analizar_datos(self):
        """
        Metodo principal para el analisis de datos
        """
        for i in range(len(self.__datos)):
            self.__resultado += self.__algortimo(self.__claves[i], self.__datos[i]),

    @staticmethod
    def __algortimo(claves, diccionario):
        """
        Algoritmo para determinar un valor de corte para un conjunto de datos de entrada
        """

        k = claves[0] - 1       # Valor de corte inicial

        izq_positivos = 0       # Numero de valores positivos por la izquierda
        izq_negativos = 0       # Numero de valores negativos por la izquierda
        der_postivos = 0        # Numero de valores positivos por la derecha
        der_negativos = 0       # Numero de valores negativos por la derecha

        for clave in claves:                    # Recuento de valores por la derecha
            for valor in diccionario[clave]:
                if valor == 'True':
                    der_postivos += 1
                else:
                    der_negativos += 1

        ep1 = der_postivos      # izq_negativos + der_positivos
        ep2 = der_negativos     # izq_positivos + der_negativos
        ep = min(ep1, ep2)      # Valor de epsilon inicial
        ep_sol = ep             # Valor de epsilon solucion (Determina el mejor valor de corte)

        for j in range(len(claves) - 1):    # Desplazamiento del valor de corte
            for valor in diccionario[claves[j]]:    # Recuento de valores
                if valor == 'True':
                    izq_positivos += 1
                    der_postivos -= 1
                    ep1 -= 1
                    ep2 += 1
                else:
                    izq_negativos += 1
                    der_negativos -= 1
                    ep1 += 1
                    ep2 -= 1

            ep = min(ep1, ep2)

            if ep < ep_sol:     # Pregunta por nuevo mejor valor de epsilon
                ep_sol = ep
                k = (claves[j] + claves[j+1])/2.0

        for valor in diccionario[claves[-1]]:   # Recuento final de valores por la izquierda
            if valor == 'True':
                izq_positivos += 1
                der_postivos -= 1
                ep1 -= 1
                ep2 += 1
            else:
                izq_negativos += 1
                der_negativos -= 1
                ep1 += 1
                ep2 -= 1

        ep = min(ep1, ep2)
        if ep < ep_sol:         # Ultima comprobacion del mejor epsilon
            k = claves[-1] + 1

        return k, ep_sol

    def to_string(self):
        """
        Metodo para mostrar los datos
        """
        text = ""
        for i in range(len(self.__resultado)):
            text += "Datos = " + str(self.__datos[i]) + "\n"
            text += "k = " + str(self.__resultado[i]) + "\n"
        self.__gestor.print_text(text)

    def exportar(self):
        """
        Metodo para exportar los datos
        """
        text = ""
        for i in range(len(self.__datos)):
            text += str(self.__resultado[i][0]) + " " + str(self.__resultado[i][1])
            text += "\n"
        self.__gestor.write_line(text)
        self.__gestor.close_file()


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        data = DataBase("data.txt", "resul.txt")
        data.fill_data()
        data.analizar_datos()
        data.to_string()
        data.exportar()


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"
