import matplotlib.pyplot as plt
import numpy as np

# Генерируем комплексные числа в прямоугольных координатах
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y

# Вычисляем условия
condition1 = np.imag(1/Z) < -1/2
condition2 = np.abs(np.angle(Z)) < np.pi/2
final_condition = np.logical_and(condition1, condition2)

# Рисуем график
plt.imshow(final_condition, extent=(x.min(), x.max(), y.min(), y.max()), origin="lower", cmap="viridis")
plt.colorbar(label="Region of Interest")
plt.show()