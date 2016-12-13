import re

__author__ = 'Alejandro Mendez Fernandez bm0058'


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

    def __init__(self, manager):
        """
        :param manager: managerIO.
        """
        self.__manager = manager
        self.__data_satations = {}      # TODO comment
        self.__stations = ['28079004', '28079038', '28079040']       # TODO comment
        self.__parameters = ['06', '08', '10', '14']
        for station in self.__stations:
            self.__data_satations[station] = {}
            for parameter in self.__parameters:
                self.__data_satations[station][parameter] = {}

    def fill_data(self):
        """
        Obtiene los datos del fichero.
        """
        raw_in = self.__manager.get_f_in()   # Fichero con datos

        line = raw_in.readline().strip('\n')    # Lectura
        while line != '':           # Mientras queden datos en el fichero:
            self.add_data_stations(line)     # Apuntamos fecha del intervalo de datos.
            line = raw_in.readline().strip('\n')    # Lectura

            """interval = []
            while line.find(':') == -1 and line != "":   # Mientras haya datos del intervalo:
                if line == '999999':    # Para medidas indefinidas
                    interval += [1500]  # suponemos que son 25 min.
                else:
                    interval += [int(line)]     # Dato tipo integer
                line = raw_in.readline().strip('\n')    # Lectura
            self.add_times(interval)    # Anhiadimos el intervalo al conjunto de tiempos"""

    def add_data_stations(self, line):   # Anhiadir fecha
        station = line[:8]
        if station in self.get_stations():
            parameter = line[8:10]
            if parameter in self.get_parameters():
                date = line[14:18]
                data = line[18:]

                appear_null_data = data.find('N')
                while appear_null_data != -1:
                    data = data[:appear_null_data - 5] + data[appear_null_data + 1:]
                    appear_null_data = data.find('N')

                self.__data_satations[station][parameter][date] = data.split('V')[:-1]
                print station + " " + parameter + " " + date + " " + str(self.__data_satations[station][parameter][date])

    def get_data_satations(self):
        return self.__data_satations

    def add_times(self, interval):  # Anhiadir intervalo de medidas
        self.__stations += [interval]

    def get_stations(self):
        return self.__stations

    def get_parameters(self):
        return self.__parameters

    def to_string(self):
        """
        Formatea a texto los datos.
        """
        text = ''
        for i in range(len(self.get_data_satations())):
            text += "Captura " + self.get_data_satations()[i] + ":\n"
            text += "->Datos: " + str(self.get_stations()[i]) + "\n"
        return text


class Analyze:
    """
    Sintetiza y opera datos.
    """

    def __init__(self, gestor):
        self.__manager = gestor     # Gestor de entrada y salida
        self.__data = DataBase(gestor)                  # Base de datos
        self.__data.fill_data()     # Se importan los datos.

        """self.__wait_times = []      # Tiempos de espera
        for time_interval in self.__data.get_stations():
            interval = []
            for time in time_interval:
                interval += [time / 60]    # Conversion de segundos a minutos
            self.__wait_times += [interval]

        self.__measure_times = []   # Tiempos de medida.
        for i in range(len(self.__data.get_stations()[0])):
            self.__measure_times += [5 * i]     # Intervalos de captura de 5 min

        self.__total_average = 0.0      # Media total.
        self.__total_variance = 0.0     # Varianza total
        self.__minor_wait_interval = [0, 999999]    # Intervalo de menor tiempo de espera"""

    @staticmethod
    def __average(wait_times):
        """
        Calcula la media de los tiempos de espera.
        :return float:
        """
        number_intervals = len(wait_times)

        total_times = []
        for i in range(number_intervals):       # Concatenamos todos los dias
            for times in wait_times[i]:
                total_times.append(times)       # para su posterior analisis.

        number_elements = len(total_times)   # Numero de elementos en total.

        sumatory = 0.0
        for time in total_times:
            sumatory += time  # Calculo de la media de valores.

        return round(float(sumatory / number_elements), 2)

    def __variance(self, wait_times):
        """
        Calcula la varianza de los tiempos de espera.
        :return float:
        """
        number_intervals = len(wait_times)

        total_times = []
        for i in range(number_intervals):       # Concatenamos todos los dias
            for times in wait_times[i]:
                total_times.append(times)       # para su posterior analisis.

        number_elements = len(total_times)   # Numero de elementos.
        total_average = self.__average(wait_times)

        numerator = 0
        for time in total_times:                        # Calculo del
            numerator += (time - total_average) ** 2    # numerador.

        return round(float(numerator / number_elements), 2)      # varianza

    def analyze(self):
        """
        Realiza 3 calculos sobre la base de datos:
            - Calcula la media de espera total
            - Calcula la varianza
            - Calcula el intervalo de 1 hora con menor media de espera
        """
        self.__total_average = self.__average(self.__wait_times)    # Calculo de la media total.
        self.__total_variance = self.__variance(self.__wait_times)  # Calculo de la varianza

        for i in range(len(self.__measure_times) - 60 / 5):     # Para cada intervalo de 60 mins
            average = 0.0
            for interval in self.__wait_times:  # Para cada intervalo:
                sumatory = 0
                for j in range(60/5):   # Intervalo de 60 minutos entre la frecuencia de recogida de datos.
                    sumatory += interval[j + i]
                average += sumatory / (60 / 5)
            average /= len(self.__wait_times)   # Media del intervalo medido.

            if average < self.__minor_wait_interval[1]:
                self.__minor_wait_interval = [self.__measure_times[i], round(average, 2)]

    def to_string(self):
        text = ""
        text += "Tiempos de espera (min) E=" + str(self.__wait_times) + "\n"
        text += "Tiempos de medida (min) T=" + str(self.__measure_times) + "\n"
        text += "Media total (min) = " + str(self.__total_average) + "\n"
        text += "Intervalo con menor tiempo de media: "
        text += str(self.__minor_wait_interval[0]) + "-" + str(self.__minor_wait_interval[0] + 60) + "\n"
        text += "Donde su valor medio es (min) = " + str(self.__minor_wait_interval[1])
        return text

    def exportar(self):
        text = ""
        text += str(self.__wait_times) + "\n"
        text += str(self.__measure_times)
        self.__manager.write_line(text)


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        self.__manager = IOManager('datos201610.txt', "resul.txt")
        analyze = Analyze(self.__manager)
        # analyze.analyze()
        # self.__manager.print_text(analyze.to_string())
        # analyze.exportar()


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"
