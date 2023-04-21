import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Square parametric equations
def square(t, a=1):
    x = a * np.cos(t)
    y = a * np.sin(t)
    return np.sign(x), np.sign(y)

# Fourier coefficients
def fourier_coeffs(x, y, n, dt):
    c = np.exp(-1j * n * t)
    a_n = np.trapz(x * c, dx=dt) / (2 * np.pi)
    b_n = np.trapz(y * c, dx=dt) / (2 * np.pi)
    return a_n, b_n

# Fourier series
def fourier_series(t, coeffs, N):
    x = np.zeros_like(t, dtype=complex)
    y = np.zeros_like(t, dtype=complex)

    for n in range(-N, N + 1):
        a_n, b_n = coeffs[n]
        x += a_n * np.exp(1j * n * t)
        y += b_n * np.exp(1j * n * t)

    return x.real, y.real

# Animation update function
def update(frame):
    global N, coeffs, rotation_speed
    plt.gca().clear()

    t = np.linspace(0, 2 * np.pi, 1000)
    x, y = fourier_series(t + frame * rotation_speed, coeffs, N)

    # Draw square
    plt.plot(x, y, 'b')

    # Draw epicycles
    center_x, center_y = 0, 0
    center_points = []
    for n in range(-N, N + 1):
        a_n, b_n = coeffs[n]
        prev_x, prev_y = center_x, center_y
        center_x += (a_n * np.exp(1j * n * (t[-1] + frame * rotation_speed))).real
        center_y += (b_n * np.exp(1j * n * (t[-1] + frame * rotation_speed))).real

        # Draw circle
        radius = np.sqrt(a_n.real**2 + b_n.imag**2)
        plt.gca().add_artist(plt.Circle((prev_x, prev_y), radius, color='r', fill=False))

        # Draw center point
        plt.plot(center_x, center_y, 'ro', markersize=3)
        center_points.append((center_x, center_y))

    # Connect the center points of the circles
    for i in range(1, len(center_points)):
        plt.plot([center_points[i - 1][0], center_points[i][0]], [center_points[i - 1][1], center_points[i][1]], 'g--')

    plt.axis("equal")
    plt.axis("off")

# Calculate Fourier coefficients
N_points = 1000
t = np.linspace(0, 2 * np.pi, N_points, endpoint=False)
dt = t[1] - t[0]
x_square, y_square = square(t)
N = 20  # Define N before using it in the dictionary comprehension
coeffs = {n: fourier_coeffs(x_square, y_square, n, dt) for n in range(-N, N + 1)}

# Animation parameters
rotation_speed = 0.05  # Slower rotation speed
frames = 400  # Number of frames for one full rotation

# Create the animation
fig = plt.figure()
ani = FuncAnimation(fig, update, frames=frames, interval=50, repeat=True)
plt.show()
