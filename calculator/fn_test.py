import matplotlib.pyplot as plt
#  Подключаем модуль управления тиками:
import matplotlib.ticker as ticker

y=[3e-2, 3e-2, None, 3e-3, 3e-3, None, 3e-5, 3e-5]
x=[0, 1, None, 1, 2, None, 2, 3]

y1=[3e-2, 3e-3, None, 3e-3, 3e-5]
x1=[1, 1, None, 2, 2]

fig, ax = plt.subplots()

ax.plot(x, y, 'bo', linewidth = 2, linestyle='-')
#  Устанавливаем интервал основных делений:
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

ax.plot(x1, y1, color = 'b', linewidth = 2, linestyle='--')
ax.set_yscale("log")

#  Прежде чем рисовать вспомогательные линии
#  необходимо включить второстепенные деления
#  осей:
ax.minorticks_on()

#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'k',
        linewidth = 0.5)

#  Определяем внешний вид линий вспомогательной
#  сетки:
ax.grid(which='minor',
        color = 'k',
        linestyle = ':')

ax.set_title('F/N - диаграмма')
ax.set_xlabel('Количество погибших, чел')
ax.set_ylabel('Вероятность, 1/год')

fig.set_figwidth(12)
fig.set_figheight(8)

plt.show()