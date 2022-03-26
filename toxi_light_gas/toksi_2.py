import math #импорт математических функций
v_veter = float(input('Введите скорость ветра, м/с___'))#скорость ветра, м/с
h_vibros = float(input('Введите высоту выброса, м___'))#значение высоты
m_vibros = float(input('Введите массу выброса, кг___'))#значение масса
q_vibros = float(input('Введите расход вторичного облака, кг/с___ '))#значение расхода ОХВ
t_vibros = float(input('Введите время поступления вторичного облака, с___'))#время поступления вторичного облака
po_vibros = float(input('Введите плотность ОХВ в выбросе, кг/м3___'))#плотность выброса
r_iskat = float(input('Введите радиус до которого надо посчитать облако, м___'))# радиус до которого надо посчитать облако

C1, C2, D1, D2 = 1.56, 0.000625, 0.048, 0.45 #шероховатость z=1
A1, A2, B1, B2, C3 = 0.069, 0.00196, 0.895, 0.684, 0.06

r=1
r_oblaka = (((3/(4*3.14))*(m_vibros/po_vibros)) ** (1/3))
sigma_x = (C3 * r)/((1 + 0.0001*r)**(1/2))
sigma_y = r/v_veter
if sigma_y >= 600:
    sigma_y = sigma_x*((220.2*60+r/v_veter)/(220.2*60+600))
elif sigma_y < 600:
    sigma_y = sigma_x

sigma_z =((A1*(r ** B1))/(1 + A2 * (r ** B2))) * math.log((C1 * (r ** D1))/(1+C2*(r ** D2)))


G0 = math.exp(-(h_vibros ** 2)/(2 * (sigma_z ** 2)))


c_max = ((2*m_vibros)/((8/3)*3.14*(r_oblaka ** 3)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)) * G0+((2*q_vibros*t_vibros)/(((2*q_vibros*t_vibros)/po_vibros)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x))*G0
d_max =((((2*m_vibros*((2*3.14) ** (1/2)))*sigma_x)/(v_veter*((8/3)*3.14*(r_oblaka ** 3)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)))*G0*16.67)+(((2*q_vibros*((2*3.14) ** (1/2))*sigma_x*t_vibros)/((v_veter*((2*q_vibros*t_vibros)/po_vibros)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)))*G0*16.67)



while r < r_iskat: #выполняем до тех пор пока искомый радиус больше r

    r_oblaka = (((3/(4*3.14))*(m_vibros/po_vibros)) ** (1/3))
    sigma_x = (C3 * r)/((1 + 0.0001*r)**(1/2))
    sigma_y = r/v_veter
    if sigma_y >= 600:
        sigma_y = sigma_x*((220.2*60+r/v_veter)/(220.2*60+600))
    elif sigma_y < 600:
        sigma_y = sigma_x

    sigma_z =((A1*(r ** B1))/(1 + A2 * (r ** B2))) * math.log((C1 * (r ** D1))/(1+C2*(r ** D2)))


    G0 = math.exp(-(h_vibros ** 2)/(2 * (sigma_z ** 2)))


    c_max = ((2*m_vibros)/((8/3)*3.14*(r_oblaka ** 3)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)) * G0+((2*q_vibros*t_vibros)/(((2*q_vibros*t_vibros)/po_vibros)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x))*G0
    d_max =((((2*m_vibros*((2*3.14) ** (1/2)))*sigma_x)/(v_veter*((8/3)*3.14*(r_oblaka ** 3)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)))*G0*16.67)+(((2*q_vibros*((2*3.14) ** (1/2))*sigma_x*t_vibros)/((v_veter*((2*q_vibros*t_vibros)/po_vibros)+((2*3.14) ** (3/2))*sigma_y*sigma_z*sigma_x)))*G0*16.67)



    print('На расстоянии = ',r,'м, концентрация = ', round(c_max,2),'кг/м3, и токсодоза = ', round(d_max,2), 'мг*мин/литр')

    r += 1
konec = float(input('Расчет окончен'))#значение коэф.
