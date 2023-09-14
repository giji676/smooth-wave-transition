import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fEnd, gStart = 1, -1 # fEnd = where the function f will end, gStart = where the function g will start
minX, maxX = -3, 3 # min and max values of the x axis

def f(x):
    return np.cos(x*3)*1

def g(x):
    return np.cos(x*10)*3

def psi(x): # Ψ or "psi" function
    result = np.zeros_like(x)
    result[x > 0] = np.exp(-1/x[x > 0])
    return result

def phi(x): # Φ or "phi" function
    condition_1 = x <= 0
    condition_2 = (x > 0) & (x < 1)
    condition_3 = x >= 1
    
    result = np.zeros_like(x)
    result[condition_1] = 0
    result[condition_2] = psi(x[condition_2]) / (psi(x[condition_2]) + psi(1 - x[condition_2]))
    result[condition_3] = 1

    return result

def phiab(x, a, b): # phi function with a and b as input for domain control
    return phi((x-a)/(b-a))

def h(x, a, b):
    return (1 - phiab(x,a,b)) * f(x) + phiab(x,a,b) * g(x)

fig, (ax1, ax2, ax_slider_a, ax_slider_b) = plt.subplots(4, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [4, 2, 1, 1]})

slider_a = Slider(ax_slider_a, 'a', -1, 0, valinit=-0.5)
slider_b = Slider(ax_slider_b, 'b', 0, 1, valinit=0.5)

def update(val):
    a = slider_a.val
    b = slider_b.val

    x1 = np.linspace(minX, fEnd, 1000)
    x2 = np.linspace(gStart, maxX, 1000)
    x_diagonal = np.linspace(minX, maxX, 1000)
    y_diagonal = h(x_diagonal, a, b)

    ax1.clear()
    ax2.clear()
    ax1.grid(True)
    ax2.grid(True)
    ax1.plot(x1, f(x1), label='f(x)', color='red')
    ax1.plot(x2, g(x2), label='g(x)', color='green')
    ax1.plot(x_diagonal, y_diagonal, color='purple', label='h(x)')
    ax1.legend()
    
    x_ph = np.linspace(minX, maxX, 1000)
    y_ph = phiab(x_ph, a, b)
    y_neg_ph = 1 - y_ph
    
    ax2.plot(x_ph, y_ph, label='phiab(x)', color='blue')
    ax2.plot(x_ph, y_neg_ph, label='1 - phiab(x)', color='orange')
    ax2.legend()
    
    plt.draw()

slider_a.on_changed(update)
slider_b.on_changed(update)

x1 = np.linspace(minX, fEnd, 1000)
x2 = np.linspace(gStart, maxX, 1000)
x_diagonal = np.linspace(minX, maxX, 1000)
y_diagonal = h(x_diagonal, -1, 0)

ax1.grid(True)
ax1.plot(x1, f(x1), label='f(x)', color='red')
ax1.plot(x2, g(x2), label='g(x)', color='green')
ax1.plot(x_diagonal, y_diagonal, color='purple', label='h(x)')
ax1.legend()

x_ph = np.linspace(minX, maxX, 1000)
y_ph = phiab(x_ph, -1, 0)
y_neg_ph = 1 - y_ph

ax2.grid(True)
ax2.plot(x_ph, y_ph, label='phiab(x)', color='blue')
ax2.plot(x_ph, y_neg_ph, label='1 - phiab(x)', color='orange')
ax2.legend()

plt.tight_layout()
plt.show()
