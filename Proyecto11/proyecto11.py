import math
__author__ = 'Alejandro Mendez Fernandez bm0058 y Leonardo Niels Pardi Quilici bm0068'


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
    """
    Objeto estacion que formatea y contiene los datos diarios en funcion de los meses y los contaminantes.
    Puede ofrecer los datos crudos, la desviacion tipica y media de datos mensuales pertenecientes a un
    contaminante, y los dias que superan el limite de peligrosidad que se le sirve.
    """

    def __init__(self):
        self.__data = {}    # Diccionario de diccionarios, contiene toda la informacion de Station.

    def __variance(self, values):
        """
        Calcula la varianza.
        Hace uso de un metodo auxiliar para calcular la media.
        :return float:
        """

        number_values = len(values)     # Cantidad numerica de valores.
        average = self.__average(values)      # Media de esos valores.

        numerator = 0.0
        for value in values:                        # Calculo del
            numerator += (value - average) ** 2     # numerador.

        return math.sqrt(float(numerator / (number_values - 1)))      # Retorna la varianza calculada.

    def __typical_deviation(self, polluting_agent, year_month):
        """
        Devuelve la desvacion tipica de un mes perteneciente a un contaminante.
        Prepara los datos para hacer uso del metodo auxiliar self.__variance().
        :return float:
        """

        values = map(float, self.get_data()[polluting_agent][year_month].values())  # Prapara los datos en formato float.
        return self.__variance(values)      # Devuelve la desviacion tipica.

    def typical_deviations(self):
        """
        Devuelve las desviaciones tipicas de cada mes para cada contaminante.
        Formatea y envia al metodo self.__typical_deviation() los datos necesarios para el calculo de los datos.
        Recopila los datos solicitados ordenandolos por contaminantes en diccionarios.
        :return:
        """

        polluting_agents = {}
        for polluting_agent in sorted(self.get_data()):   # Para cada diccionario que posee Station.

            polluting_agents[polluting_agent] = {}
            for year_month in sorted(self.get_data()[polluting_agent]):
                polluting_agents[polluting_agent][year_month] = self.__typical_deviation(polluting_agent, year_month)

        return polluting_agents     # Devuelve la desviacion tipica, ordenada.

    @staticmethod
    def __average(values):
        """
        Calcula la media.
        :return float:
        """

        sumatory = 0.0
        for value in values:    # Sumatorio de todos los valores.
            sumatory += value

        return sumatory / len(values)       # Devuelve la media calculada.

    def __average_value(self, polluting_agent, year_month):
        """
        Devuelve la media de un mes perteneciente a un contaminante.
        Prepara los datos para hacer uso del metodo auxiliar self.__average().
        :return float:
        """
        value = map(float, self.get_data()[polluting_agent][year_month].values())  # Prapara los datos en formato float.
        return self.__average(value)       # Devuelve la media.

    def average_values(self):
        """
        Devuelve las medias de cada mes para cada contaminante.
        Formatea y envia al metodo self.__average_value() los datos necesarios para el calculo de los datos.
        Recopila los datos solicitados ordenandolos por contaminantes en diccionarios.
        :return string:
        """

        polluting_agents = {}
        for polluting_agent in sorted(self.get_data()):   # Para cada diccionario que posee Station.

            polluting_agents[polluting_agent] = {}
            for year_month in sorted(self.get_data()[polluting_agent]):
                polluting_agents[polluting_agent][year_month] = str(self.__average_value(polluting_agent, year_month))

        return polluting_agents         # Devuelve la media, ordenada.

    @staticmethod
    def __worst_days(polluting_agent, legal_limit):
        """
        Devuelve los dias que superan el limite legal recibido del contaminante solicitado.
        Recopila los datos solicitados ordenandolos por meses en diccionarios.
        :return dict:
        """

        worst_days = {}     # Diccionario almacen.
        for year_month in sorted(polluting_agent):   # Para cada mes del parametro.

            worst_days[year_month] = {}             # Contiene diccionarios.
            for days in sorted(polluting_agent[year_month]):      # Para cada dia del mes.
                if float(polluting_agent[year_month][days]) >= float(legal_limit):
                    worst_days[year_month][days] = polluting_agent[year_month][days]

            if {} == worst_days[year_month]:
                worst_days.pop(year_month)

        return worst_days           # Devuelve los peores dias, ordenados.

    def warning_days(self, legal_limits):
        """
        Devuelve los dias que superan los limetes legales recibidos de todos los contaminantes.
        Formatea y envia al metodo self.__worst_days() los datos necesarios para la consulata de los datos.
        Recopila los datos solicitados ordenandolos por contaminantes en diccionarios.
        :return dict:
        """

        polluting_agents = {}
        for polluting_agent in sorted(self.get_data()):   # Para cada diccionario que posee Station.
            # Se obtienen los datos facilitando a self.__worst_days(), metodo auxiliar, los datos necesarios.
            polluting_agents[polluting_agent] = self.__worst_days(self.get_data()[polluting_agent], legal_limits[polluting_agent])

            if {} == polluting_agents[polluting_agent]:
                polluting_agents.pop(polluting_agent)

        return polluting_agents         # Devuelve los peores dias, ordenados.

    def __add_parameter(self, parameter):   # Crea diccionario.
        self.get_data()[parameter] = {}

    def add_data(self, raw_data, polluting_agent):
        """
        Recibe una linea de datos cruda y obtiene los datos de ella.
        """
        if polluting_agent not in self.__data:      # Si es un contaminante nuevo.
            self.__add_parameter(polluting_agent)

        date = raw_data[14:18]
        data = raw_data[18:]

        data = map(''.join, zip(*[iter(data)] * 6))     # Truquito para separar en grupos de 6 caracteres.

        auxdict = {}
        for i in range(0, len(data)):       # Se enumeran los dias y se eliminan aquellos que sean nulos.
            if data[i].find('N') == -1:
                day = str(i + 1)
                if i + 1 < 10:      # Formato '00' de los dias.
                    day = "0" + day
                auxdict[day] = str(float(data[i][:-1]))

        self.__data[polluting_agent][date] = auxdict    # Incorpora los valores por dia.

    def get_polluting_agents(self):
        """
        Devuelve los contaminantes.
        """
        return sorted(self.get_data().keys())

    def get_months(self):
        """
        Devuelve los meses.
        """
        return sorted(self.get_data()[self.get_polluting_agents()[0]].keys())

    def get_data(self):
        """
        Devuelve los datos.
        """
        return self.__data

    def tostring(self):
        """
        Formatea a texto los datos.
        """
        text = ""

        for polluting_agent in sorted(self.get_data()):
            text += "  > Polluting Agent(" + polluting_agent + "):\n"
            text += "    > Year/Month:\n"
            for date in sorted(self.get_data()[polluting_agent]):
                text += "        " + date[:2] + "/" + date[2:] + ":"
                for day in sorted(self.get_data()[polluting_agent][date]):
                    text += " D" + day + "(" + str(self.get_data()[polluting_agent][date][day]) + "),"
                text = text[:-1] + "\n"

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
        self.__data = {}      # Almacen de objetos Station.
        self.__stations = ['28079004', '28079038', '28079040']       # Las estaciones objetivo
        self.__polluting_agents = {'06': '10', '08': '200', '10': '50', '14': '110'}    # Contaminantes / valores max.
        for station in self.__stations:     # Inicializacion de objetos Station.
            self.__data[station] = Station()

    def fill_data(self):
        """
        Obtiene los datos del fichero.
        """
        raw_in = self.__manager.get_f_in()   # Fichero con datos

        line = raw_in.readline().strip('\n')    # Lectura
        while line != '':           # Mientras queden datos en el fichero:
            self.add_data(line)     # Se procesan los datos.
            line = raw_in.readline().strip('\n')    # Lectura

    def add_data(self, line):
        """
        Comprueba si contiene informacion relevante, si es asi se incorpora a su estacion.
        """
        station = line[:8]
        if station in self.get_stations():
            parameter = line[8:10]
            if parameter in self.get_polluting_agents():
                self.__data[station].add_data(line, parameter)      # Se incorpora a su estacion.

    def __show_table(self, averages, typical_deviations, warning_days):
        """
        Formatea los datos en tablas con los resultados.
        """
        text = "Limites Legales(Contaminante = valor):\n"
        for parameter in self.get_polluting_agents():
            text += parameter + " = " + self.get_polluting_agents()[parameter] + "\n"

        text += "\nTable of results:"
        for month in sorted(self.get_data()[self.get_stations()[0]].get_months()):  # Por cada mes...
            text += "\n\n+-------------- Month: " + month[2:] + \
                     " ----------------------------------------------------------+\n"
            text += "|magnitude |station   |average |deviation |worst days   [day (value)]               |\n"
            text += "+----------+----------+--------+----------+-----------------------------------------+\n"
            # Creamos una tabla con sus respectivas columnas.
            for station in sorted(self.get_stations()):  # Rellenamos las columnas reocrriendo cada elemento por estacion.
                for parameter in sorted(self.get_polluting_agents()):
                    if parameter in self.get_data()[station].get_polluting_agents():     # Siempre que la estacion haya capturado tal elemento.
                        text += "|    " + parameter + "    | "   # Escribimos el correpondiente resultado.
                        text += station   # Por columna
                        for i in range(9-len(station)):    # Y anyadimos espacios para encuadrar las columans.
                            text += " "
                        text += "| " + str(round(float(averages[station][parameter][month]), 2))    # Y asi para cada columna.
                        for i in range(7-len(str(round(float(averages[station][parameter][month]), 2)))):
                            text += " "
                        text += "| " + str(round(float(typical_deviations[station][parameter][month]), 2))
                        for i in range(9-len(str(round(float(typical_deviations[station][parameter][month]), 2)))):
                            text += " "
                        text += "| "
                        spaces = 0
                        if parameter in warning_days[station]:
                            if month in warning_days[station][parameter]:
                                for day in warning_days[station][parameter][month]:
                                    to_print = "D" + day + "(" + warning_days[station][parameter][month][day] + ") "
                                    text += to_print
                                    spaces += len(to_print)

                        for i in range(40 - spaces):
                            text += " "
                        text += "|\n"
                text += "+----------+----------+--------+----------+-----------------------------------------+\n"
        return text

    def show_table(self):
        """
        Prepara los datos para su representacion en tabla.
        """
        averages = {}       # Medias por meses.
        typical_deviations = {}     # Desviaciones tipicas por meses.
        warning_days = {}           # Dias peligrosos por meses.
        for station in self.get_stations():     # Se obtienen los datos.
            averages[station] = self.get_averages(station)
            typical_deviations[station] = self.get_typical_deviations(station)
            warning_days[station] = self.get_warning_days(station)

        return self.__show_table(averages, typical_deviations, warning_days)

    def get_data(self):
        """
        Devuelve los datos.
        """
        return self.__data

    def get_stations(self):
        """
        Devuelve las estaciones objetivo.
        """
        return self.__stations

    def get_polluting_agents(self):
        """
        Devuelve los agentes contaminantes con sus limites legales.
        """
        return self.__polluting_agents

    def get_averages(self, station):
        """
        Obtiene las medias de una estacion para cada contaminante en cada mes.
        """
        return self.get_data()[station].average_values()

    def get_typical_deviations(self, station):
        """
        Obtiene la desviaciones tipicas de una estacion para cada contaminante en cada mes.
        """
        return self.get_data()[station].typical_deviations()

    def get_warning_days(self, station):
        """
        Obtiene los dias peligrosos de una estacion para cada contaminante en cada mes.
        """
        return self.get_data()[station].warning_days(self.get_polluting_agents())

    def tostring(self):
        """
        Formatea a texto los datos.
        """
        text = ""

        for station in sorted(self.get_data()):
            text += "\nStation(" + station + "):\n"
            text += self.get_data()[station].tostring()

        return text


class Aplicacion:
    """
    Inicia y acaba el programa.
    """

    def __init__(self):
        self.__manager = IOManager('datos201610.txt', "resul.txt")  # Gestor de entrada y salida
        datos = DataBase(self.__manager)        # Base de datos
        datos.fill_data()                       # Se importan los datos.
        self.__manager.print_text(datos.tostring())     # Datos a pantalla.
        tabla = datos.show_table()      # Formato tabla de informacion.
        self.__manager.print_text(tabla)    # Muestra por pantalla.
        self.exportar(tabla)

    def exportar(self, text):
        """
        Exporta a un fichero.
        :param text:
        """
        self.__manager.write_line(text)


print "----------\nINICIO\n----------"
Aplicacion()
print "----------\nFIN\n----------"

