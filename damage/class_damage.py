# -----------------------------------------------------------
# The class demonstrates the calculation of a damage
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# Released under GNU Public License (GPL)
# -----------------------------------------------------------
import random

from prettytable import PrettyTable
import math

CONST = 0.02 # часть ущерба

class     Damage:

    def direct_damage(self, volume = 0, diametr =114,  #полный ущерб
                      lenght = 1000, cost_sub = 0.012,
                      part_sub = 1):
        """
        For stationary object
        volume, m3 (объем в м3)
        For line object
        diametr, mm (диаметр трубы в мм)
        length, m (длина, м)
        For all
        cost_sub, mln.rub/m3 (стоимость млн.руб/м3)
        part_sub - part substance loss

        Return:
        - damage of equipment, millions of rubles
        """
        if diametr == 0 and lenght == 0:                #если расчитываем стац.объект
            new_obj = (0.0036 * volume + 0.6061)          #стоимость нового объекта, млн
                                                        #данные апроксимировал с коэф.0.2 с http://rezervuarstroy.ru/page/prajs-listy.html
            sub_loss = cost_sub * volume * part_sub     #стомость вещества с потерей доли
                                                        #(т.к. бывают разные сценарии (пожар, взрыв, шар и пр.)
            dis_obj = new_obj * 0.2                     #примерно 20% на демонтаж объекта

            direct_damage = new_obj + sub_loss + dis_obj#строительство + потеря вещества + демонтаж

        elif volume == 0:                                 #если расчитываем линейный объект
            new_obj = \
                ((0.0195*diametr + 1.0519)*lenght/1000)   #стоимость нового объекта, млн
                                                              #данные апроксимировал с коэф.0.2 с http://www.ozti.org/upload/iblock/637/COSTS.pdf
            volume_lin = \
                math.pi*math.pow(diametr/2000,2)*lenght

            sub_loss = cost_sub * volume_lin * part_sub #стомость вещества с потерей доли
                                                        #(т.к. бывают разные сценарии (пожар, взрыв, шар и пр.)
            dis_obj = new_obj * 0.2                     #примерно 20% на демонтаж объекта

            direct_damage = new_obj + sub_loss + dis_obj #строительство + потеря вещества + демонтаж
        else:
            direct_damage = 3                            #если все вызвано с 0 то ущерб принять 3 млн.

        direct_damage = round(direct_damage,2)

        return direct_damage


    def se_damage(self, death_person = 1, injured_person = 1):#Socio_economic_damage (социально-экономический)
        """
        death_person
        injured_person

        Return:
        - damage of person, millions of rubles
        """
        se_damage = (death_person *
                     (12000 * 18 * 12 + 2000000 + 1000000) +    #ФЗ-225 и 125
                     injured_person * 250000)*math.pow(10,-6)

        se_damage = round(se_damage, 2)
        return se_damage

    def damage_air(self, m_out_spill=3.4):
        """
         - mass of the evaporated substance,  tons (тонны);


        Return:
        - damage of air, millions of rubles

        При расчете ущерба от загрязнения воздуха при расчете ущерба
        принимались следующие коэффициенты:
        Загрязняющее вещество - Углеводороды С1-С5
        Норматив платы, руб./т (Мсрi) - 108
        Коэффициент за 2021 г. (Нплi) - 1,08
        Коэффициент Кср - 25 (ПРИКАЗ Минприроды) от 9 января 2017 г. N 3



        См. Постановление Правительства РФ от 11.09.2020 N 1393
        "О применении в 2021 году ставок платы за негативное
        воздействие на окружающую среду"

        Постановление Правительства РФ от 13.09.2016 № 913
        «О ставках платы за негативное воздействие на окружающую
        среду и дополнительных коэффициентах»
        """

        tax_1_tonn = 108*1*1.08*25
        damage_air = round(m_out_spill * tax_1_tonn * pow(10, -6), 4)

        return damage_air

    def damage_air_fire(self, m_in_spill=50.5):
        """
         - mass of the  substance,  tons (тонны);


        Return:
        - damage to air from oil combustion, millions of rubles

        ____________________________________________________
        Ущерб от загрязнения атмосферного воздуха
        при сгорании 1 тонны нефти:
        ____________________________________________________
        Загрязняющее вещество - Оксид углерода (СО)* (0,798т)
        Норматив платы, руб./т (Мсрi) - 1.6
        ____________________________________________________
        Загрязняющее вещество - Оксиды азота (NОx)* (0,066т)
        Норматив платы, руб./т (Мсрi) - 138,8
        ____________________________________________________
        Загрязняющее вещество - Оксиды серы (SO2)** (0,26т)
        Норматив платы, руб./т (Мсрi) - 45,4
        ____________________________________________________
        Загрязняющее вещество - Сероводород (H2S)* (0,001т)
        Норматив платы, руб./т (Мсрi) - 686,2
        ____________________________________________________
        Загрязняющее вещество - Сажа (С)** (1.615т)
        Норматив платы, руб./т (Мсрi) - 109,5
        ____________________________________________________
        Загрязняющее вещество - Синильная кислота (НСN)* (0,01т)
        Норматив платы, руб./т (Мсрi) - 547,4
        ____________________________________________________
        Загрязняющее вещество - Формальдегид (HCHO)* (0,01т)
        Норматив платы, руб./т (Мсрi) - 1823,6
        ____________________________________________________
        Загрязняющее вещество - Органич. к-ты (на СН3СООН)* (0,14т)
        Норматив платы, руб./т (Мсрi) - 93,5

        Коэффициент за 2021 г. (Нплi) - 1,08
        Коэффициент Кср - 25 (ПРИКАЗ Минприроды от 9 января 2017 г. N 3)



        См. Постановление Правительства РФ от 11.09.2020 N 1393
        "О применении в 2021 году ставок платы за негативное
        воздействие на окружающую среду"

        Постановление Правительства РФ от 13.09.2016 № 913
        «О ставках платы за негативное воздействие на окружающую
        среду и дополнительных коэффициентах»
        """

        tax_CO = 1.6 * 1.08 * 25 * 0.798
        tax_NOx = 138.8 * 1.08 * 25 * 0.066
        tax_SO2 = 45.4 * 1.08 * 25 * 0.26
        tax_H2S = 686.2 * 1.08 * 25 * 0.001
        tax_C = 109.5 * 1.08 * 25 * 1.615
        tax_HCN = 547.4 * 1.08 * 25 * 0.01
        tax_HCHO = 1823.6 * 1.08 * 25 * 0.01
        tax_CH3COOH = 93.5 * 1.08 * 25 * 0.14

        tax_all_1_tonn = tax_CO + tax_NOx + tax_SO2 + tax_H2S + tax_C + tax_HCN + tax_HCHO + tax_CH3COOH

        damage_air_fire = round(m_in_spill * tax_all_1_tonn * pow(10, -6), 4)

        return damage_air_fire

    def damage_earth(self, S_spill=1124):
        """
        S_spill - spill, m2;


        Return:
        - damage of earth, millions of rubles

        При расчете ущерба от загрязнения почвы при расчете ущерба
        принимались следующие коэффициенты СЗ =1,5 (степень загрязнения),
        Kr = 1 (показатель в зависимости от глубины загрязнения),
        Кисх=1,6 (показатель в зависимости от кат.земель и
        целевого назначения),
        Тх = 500 руб/м2 (расценка для исчисления размера вреда).
        Итого за 1 м2: 1200 руб.

        См. Методика исчисления размера вреда,
        причиненного почвам как объекту охраны окружающей среды
        (утверждена Приказом Минприроды России от 08.07.2010 № 238
        (ред. от 25.04.2014)
        (Зарегистрировано в Минюсте России 07.09.2010 № 18364)
        """

        tax_1m2 = 1.5*1*1.6*500
        damage_earth = round(S_spill * tax_1m2 * pow(10, -6), 3)

        return damage_earth


    def damage_array(self,volume = 0, diametr =114,
                      lenght = 1000, cost_sub = 0.012,
                      part_sub = 1,
                     death_person = 1, injured_person = 1,
                     m_out_spill = 3, m_in_spill=50.5, S_spill=1124):
        """

        Parametrs:
        For stationary object
        volume, m3 (объем в м3)
        For line object
        diametr, mm (диаметр трубы в мм)
        length, m (длина, м)

        For all
        cost_sub, mln.rub/m3 (стоимость млн.руб/м3)
        part_sub - part substance loss
        death_person
        injured_person
        m_out_spill - mass of the evaporated substance,  tons (тонны);
        m_in_spill - mass of the  substance,  tons (тонны);
        S_spill - spill, m2;


        Return:
        damage_array, mln.RUB
        """
        direct_damage = self.direct_damage(volume, diametr, lenght, cost_sub, part_sub)
        if direct_damage < 0.1:
            direct_damage = random.uniform(0.11, 0.15)
        liquidation_failures = round(direct_damage * 0.1,2)
        se_damage = self.se_damage(death_person, injured_person)
        consequential_damage = round((se_damage + direct_damage)*0.125,2)
        # ________________Ecological____________________________________
        damage_air = self.damage_air(m_out_spill)               #от испарения
        damage_air_fire = self.damage_air_fire(m_in_spill)      #от горения
        damage_earth = self.damage_earth(S_spill)               #от пролива
        ecological_damage = round(damage_air +
                                  damage_air_fire +
                                  damage_earth,2)
        # __________________________________________________________________
        new_man = round(death_person*(30000*(3200/170000)/(52*5)),2)

        sum_damage = round(round(direct_damage * CONST,2) + liquidation_failures + se_damage +
                           consequential_damage +
                           damage_air + damage_air_fire + damage_earth +
                           ecological_damage +
                           new_man,2)

        damage_array = [round(direct_damage * CONST,2), liquidation_failures, se_damage, consequential_damage,
                        damage_air, damage_air_fire, damage_earth, ecological_damage,
                        new_man,sum_damage]

        return damage_array


    def report_table(self, volume = 0, diametr =114,
                      lenght = 1000, cost_sub = 0.012,
                      part_sub = 1,
                     death_person = 1, injured_person = 1,
                     m_out_spill = 3, m_in_spill=50.5, S_spill=1124):
        """

        Parametrs:
        For stationary object
        volume, m3 (объем в м3)
        For line object
        diametr, mm (диаметр трубы в мм)
        length, m (длина, м)

        For all
        cost_sub, mln.rub/m3 (стоимость млн.руб/м3)
        part_sub - part substance loss
        death_person
        injured_person
        m_out_spill - mass of the evaporated substance,  tons (тонны);
        m_in_spill - mass of the  substance,  tons (тонны);
        S_spill - spill, m2;

        Return:
        report_table (str)
        """

        damage_array = self.damage_array(volume, diametr, lenght, cost_sub,
                                         part_sub, death_person, injured_person,
                                         m_out_spill, m_in_spill, S_spill)
        report_table = PrettyTable()
        report_table.field_names = ["№ п/п","Параметр", "Стоимость, млн.руб"]
        report_table.add_row(["1.","Прямые потери", damage_array[0]])
        report_table.add_row(["2.","Затраты на ликвидацию", damage_array[1]])
        report_table.add_row(["3.","Социальные потери", damage_array[2]])
        report_table.add_row(["4.","Косвенный ущерб", damage_array[3]])
        report_table.add_row(["5.","Экологический ущерб", str("")])
        report_table.add_row(["5.а", " - ущерб воздуху от испарения", damage_array[4]])
        report_table.add_row(["5.б", " - ущерб воздуху от горения", damage_array[5]])
        report_table.add_row(["5.в", " - ущерб земле от пролива", damage_array[6]])
        report_table.add_row(["", "Суммарный экологический ущерб", damage_array[7]])
        report_table.add_row(["6.","Выбытие трудовых ресурсов", damage_array[8]])
        report_table.add_row(["7.","Суммарный ущерб", damage_array[9]])

        return report_table


# import matplotlib.pyplot as plt
# names = ['group_a', 'group_b', 'group_c']
# values = [1, 10, 100]
#
# plt.figure(figsize=(9, 3))
#
# plt.subplot(131)
# plt.bar(names, values)
# plt.subplot(132)
# plt.scatter(names, values)
# plt.subplot(133)
# plt.plot(names, values)
# plt.suptitle('Categorical Plotting')
# plt.show()


# f = Damage()
# print(f.report_table())
