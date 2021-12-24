import math


def ri(h_eff, po_eff, u_dinamic):  # 99
    return 9.81 * ((po_eff - 1.29) / 1.29) * (h_eff / pow(u_dinamic, 2))


def u_up_mixing(h_eff, po_eff, u_dinamic):
    ri = 9.81 * ((po_eff - 1.29) / 1.29) * (h_eff / pow(u_dinamic, 2))
    a = pow(1 + 0.8 * ri, 1 / 2) / (1 + 0.65)
    b = pow(1 - 0.6 * ri, -1 / 2) / (1 + 0.65)
    f_ri = a if ri > 0 else b
    return 0.41*u_dinamic/f_ri




# _____
# Volume = 1000 m3
# alpha = 0.1
# _____
p3 = 3  # pressure (MPa)
t3 = 10  # temperature (deg.C)
q_gas = 9035.265  # mass gas (kg)
q_lig = 1397700  # mass liquid (kg)
f_spill = 500  # m2
# ____Substance____
steam_pressure = 5950  # mm.rt.st, давление пара
t_kip = 44.7  # s, time boiling
q_gas_boiling = 1390  # mass gas boiling (kg)
q_gas_spray = 175000  # mass gas spray (kg)
q_gas_in_spray = 175000  # mass gas spray (kg)
po_first_cloud = 6.95  # density of first cloud (kg/m3)
t_first_cloud = -31  # temperature (deg.C)
mass_gas_in_first_cloud = q_gas + q_gas_boiling + q_gas_spray + q_gas_in_spray
r_3 = pow(mass_gas_in_first_cloud / (math.pi * po_first_cloud), 1 / 3)
h_3 = r_3  # eq.41

h_eff = (1/1.65)*h_3*1.49 #Г(1/1,65)
u_eff = (1/1.49)*1*pow(h_3/10,0.65)

# ____Second cloud____
po_second_cloud = 3.57  # density of second cloud (kg/m3)
t_second_cloud = -31  # temperature (deg.C)
q_i_3 = 4.61  # speed evaporated (kq/s)
u_0_eff = 0.108  # speed eff (kq/s)
b_3 = 0.5 * pow(f_spill, 1 / 2)
h_3_s = q_i_3 / (2 * u_0_eff * b_3 * po_second_cloud)

# ____All____
time_ev_lig = (q_lig - q_gas_spray - q_gas_boiling - q_gas_in_spray) / q_i_3
l_mo = 26 * pow(0.55, 0.17)
u_dinamic = (0.41 * 1) / (math.log(((10 + 0.55) / 0.55) - (-6.9 * 10 / l_mo)))  # u*

if __name__ == "__main__":
    print(f'Масса ОВ (газа и жидкости) в первичном облаке: {mass_gas_in_first_cloud} кг')
    print(f'Начальный радиус первичного облака ОВ: {r_3} м')
    print(f'Начальная высота первичного облака ОВ: {h_3} м')
    print(f'Начальная полуширина вторичного облака: {b_3} м')
    print(f'Начальная высота вторичного облака: {h_3_s} м')
    print(f'Время испарения пролива: {time_ev_lig} с')
    print(f'Масштаб Монина - Обухова: {l_mo} -')
    print(f'Динамическая скорость: {u_dinamic} м/с')
    print(f'Эффективная высота: {h_eff} м')
    print(f'Эффективная скорость: {u_eff} м/с')
