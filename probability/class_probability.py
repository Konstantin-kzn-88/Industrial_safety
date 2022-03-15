class Probability:

    def probability_rosteh(self, type: int, length: float) -> tuple:
        """

        Parametrs:
        :param type: тип оборудования
        0 - трубопровод
        1 - емкость под давлением
        2 - насос герметичный
        3 - колонны конденсаторы фильтры
        4 - резервуар хранения
        5 - теплообменники
        6 - цистерны
        Return:
        probability_array множество вероятностей инициирующих событий (приказ РТН от 11 апреля 2016 г. N 144)
        """

        if type == 0:
            return (3 * pow(10, -7) * length, 2 * pow(10, -6) * length)

        if type == 1:
            return (1 * pow(10, -6), 1 * pow(10, -5))

        if type == 2:
            return (1 * pow(10, -5), 5 * pow(10, -5))

        if type == 3:
            return (1 * pow(10, -5), 1 * pow(10, -4))

        if type == 4:
            return (1 * pow(10, -5), 1 * pow(10, -4))

        if type == 5:
            return (1.5 * pow(10, -5), 1 * pow(10, -3))

        if type == 6:
            return (5 * pow(10, -7), 4 * pow(10, -5))
