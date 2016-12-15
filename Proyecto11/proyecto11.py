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


class Station:
    # TODO comment all

    def __init__(self):
        self.__data = {}

    def __variance(self, values):
        """
        Calcula la varianza.
        :return float:
        """
        number_values = len(values)
        total_average = self.__average(values)

        numerator = 0
        for value in values:                             # Calculo del
            numerator += (value - total_average) ** 2    # numerador.

        return round(float(numerator / (number_values - 1)), 2)      # varianza

    def typical_deviation(self, parameter, year_month):
        values = map(float, self.get_data()[parameter][year_month])
        return self.__variance(values)

    @staticmethod
    def __average(values):

        sumatory = 0.0
        for value in values:
            sumatory += value

        return sumatory / len(values)

    def average_value(self, parameter, year_month):
        values = map(float, self.get_data()[parameter][year_month])
        return self.__average(values)

    def __worst_days(self, parameter, legal_limit):
        worst_days = {}
        for year_month in sorted(self.get_data()[parameter]):
            day = 1
            worst_days[year_month] = []
            for value_per_day in map(float, self.get_data()[parameter][year_month]):
                if value_per_day >= legal_limit:
                    worst_days[year_month] += [[day, value_per_day]]
                day += 1
            if [] in worst_days[year_month]:
                worst_days.pop(year_month)
        return worst_days

    def warning_days(self, legal_limits):
        parameters = {}
        for parameter in sorted(self.get_data()):
            parameters[parameter] = self.__worst_days(self.get_data()[parameter], map(float, legal_limits[parameter]))
        return parameters

    def __add_parameter(self, parameter):
        self.get_data()[parameter] = {}

    def add_data(self, raw_data, parameter):
        if parameter not in self.__data:
            self.__add_parameter(parameter)

        date = raw_data[14:18]
        data = raw_data[18:]

        """def format(string):
            print 'hola'"""

        data = map(''.join, zip(*[iter(data)] * 6))
        print data
        exit()

        appear_null_data = data.find('N')
        while appear_null_data != -1:
            data = data[:appear_null_data - 5] + data[appear_null_data + 1:]
            appear_null_data = data.find('N')

        self.__data[parameter][date] = data.split('V')[:-1]

    def get_data(self):
        return self.__data

    def tostring(self):
        """
        Formatea a texto los datos.
        """
        text = ""

        for parameter in sorted(self.get_data()):
            text += "  > Polluting Agent(" + parameter + "):\n"
            text += "    > Year/Month:\n"
            for date in sorted(self.get_data()[parameter]):
                text += "        " + date[:2] + "/" + date[2:] + ":" + str(self.get_data()[parameter][date]) + "\n"

        return text


class DataBase:
    """
    Obtiene y almacena datos.
    """

    def __init__(self, manager):
        """
        :param manager: managerIO.
        """
        self.__manager = manager
        self.__data = {}      # TODO comment
        self.__stations = ['28079004', '28079038', '28079040']       # TODO comment
        self.__parameters = {'06': '10', '08': '200', '10': '50', '14': '110'}
        for station in self.__stations:
            self.__data[station] = Station()

    def fill_data(self):
        """
        Obtiene los datos del fichero.
        """
        raw_in = self.__manager.get_f_in()   # Fichero con datos

        line = raw_in.readline().strip('\n')    # Lectura
        while line != '':           # Mientras queden datos en el fichero:
            self.add_data(line)     # TODO comment
            line = raw_in.readline().strip('\n')    # Lectura

    def add_data(self, line):   # TODO comment
        station = line[:8]
        if station in self.get_stations():
            parameter = line[8:10]
            if parameter in self.get_parameters():
                self.__data[station].add_data(line, parameter)

    def get_data(self):     # TODO comment
        return self.__data

    def get_stations(self):
        return self.__stations

    def get_parameters(self):
        return self.__parameters

    def tostring(self):
        """
        Formatea a texto los datos.
        """
        text = ""

        for station in sorted(self.get_data()):
            text += "\nStation(" + station + "):\n"
            text += self.get_data()[station].tostring()

        return text


class Analyze:
    """
    Sintetiza y opera datos.
    """

    def __init__(self, gestor):
        self.__manager = gestor     # Gestor de entrada y salida
        self.__data = DataBase(gestor)                  # Base de datos
        self.__data.fill_data()     # Se importan los datos.
        print self.__data.tostring()
        print str(self.__data.get_data()['28079004'].average_value('08', '1601'))

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
