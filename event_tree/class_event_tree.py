class Event_tree:

    def event_tree_inflammable(self, flash_temperature: float, flow_rate: float, probability: float) -> tuple:
        """

        Parametrs:
        :param flash_temperature: температура вспышки, град.С
        :param flow_rate: аварийный расход, кг/с (0 - полняй разрыв)
        :param probability: частота первичного события, 1/год (например probability = 20)

        Return:
        scenarios_array (probability scenarios)
        """

        global a, b, c
        if flash_temperature < 28 and flow_rate == 0:
            a = 0.2
            b = 0.24
            c = 0.6

        elif flash_temperature >= 28 and flow_rate == 0:  # gap
            a = 0.05
            b = 0.061
            c = 0.1

        elif flash_temperature < 28 and flow_rate <= 0.5:
            a = 0.005
            b = 0.005
            c = 0.08

        elif flash_temperature >= 28 and flow_rate <= 0.5:
            a = 0.005
            b = 0.005
            c = 0.05

        elif flash_temperature < 28 and 0.5 < flow_rate <= 10:
            a = 0.035
            b = 0.036
            c = 0.24
        # print (a,b,c)
        elif flash_temperature >= 28 and 0.5 < flow_rate <= 10:
            a = 0.015
            b = 0.015
            c = 0.05

        elif flash_temperature < 28 and 10 < flow_rate <= 10000:  # очень большой расход
            a = 0.15
            b = 0.176
            c = 0.6

        elif flash_temperature >= 28 and 10 < flow_rate <= 10000:
            a = 0.04
            b = 0.042
            c = 0.05

        # the calculation scenarios of the accident
        instant_ignition = "{:.2e}".format(probability * a)  # мгновенное воспламенение
        overpressure = "{:.2e}".format(probability * (1 - a) * b * c)
        no_overpressure = "{:.2e}".format(probability * (1 - a) * b * (1 - c))
        elimination = "{:.2e}".format(probability * (1 - a) * (1 - b))

        scenarios_array = (instant_ignition, overpressure, no_overpressure, elimination)

        return scenarios_array
