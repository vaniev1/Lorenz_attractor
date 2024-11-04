import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Используем TkAgg как бэкенд для matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

# Параметры системы Лоренца
sigma = 10.0
beta = 8.0 / 3.0
rho = 28.0

# Уравнения Лоренца
def lorenz(state, t):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Начальные условия и время
state0 = [1.0, 1.0, 1.0]
t = np.linspace(0, 100, 10000)

# Решение системы уравнений
states = odeint(lorenz, state0, t)

# Создаем главное окно
root = tk.Tk()
root.title("Аттрактор Лоренца")
root.geometry("800x600")  # Устанавливаем начальный размер окна

# Создаем фрейм с черным фоном
frame = tk.Frame(root, bg='black')
frame.pack(fill=tk.BOTH, expand=True)

# Создаем график
fig = plt.figure(figsize=(10, 7), facecolor='black')  # Черный фон для графика
ax = fig.add_subplot(111, projection='3d')

# Настраиваем фон и цвет
ax.set_facecolor('black')  # Черный фон для осей
ax.xaxis.set_pane_color((0, 0, 0, 1))  # Черный фон оси X
ax.yaxis.set_pane_color((0, 0, 0, 1))  # Черный фон оси Y
ax.zaxis.set_pane_color((0, 0, 0, 1))  # Черный фон оси Z

# Убираем линии
ax.xaxis.line.set_color('green')  # Цвет линии X
ax.yaxis.line.set_color('green')  # Цвет линии Y
ax.zaxis.line.set_color('green')  # Цвет линии Z

# Устанавливаем ограничения осей
ax.set_xlim([-30, 30])
ax.set_ylim([-30, 30])
ax.set_zlim([0, 50])

# Убираем сетку
ax.grid(False)

# Подготавливаем анимацию
line, = ax.plot([], [], [], lw=0.5, color='green')  # Линия для анимации

def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return line,

def update(frame):
    line.set_data(states[:frame, 0], states[:frame, 1])  # Обновляем данные по X и Y
    line.set_3d_properties(states[:frame, 2])  # Обновляем данные по Z
    return line,

# Создаем анимацию с меньшим интервалом
ani = FuncAnimation(fig, update, frames=len(states), init_func=init, blit=True, interval=1)  # interval=1 для максимальной скорости

# Добавляем график в фрейм
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Запускаем основной цикл приложения
root.mainloop()
