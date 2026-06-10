import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from integrador import runge_kutta

#TERCERA SIMULACION
#aqui vamos a considerar al sistema binario como una sola masa en el origen y a
#proxima orbitando alrededor de ese centro de masas, para ver su órbita a largo plazo

tiempo_total = 600000.0  #años
_dt = 15.0  #años por paso


def cond_iniciales_proxima():
    mA = 1.1
    mB = 0.9
    mP = 0.125
    M_ab = mA + mB

    #distancia inicial de proxima, la actual
    r = 13000.0 #UA

    #velocidad relativa
    G = 4 * np.pi**2
    v_rel = np.sqrt(G * (M_ab + mP) / r)

    #posiciones respecto del centro de masas (?)
    x_ab = -mP / (M_ab + mP) * r
    x_p = M_ab / (M_ab + mP) * r

    #velocidades individuales
    v_ab = mP / (M_ab + mP) * v_rel
    v_p = -M_ab / (M_ab + mP) * v_rel

    posiciones = np.array([
        [x_ab, 0.0, 0.0],  #baricentro de Alfa Centauri A/B
        [x_p, 0.0, 0.0],   #Proxima Centauri
    ], dtype=float)

    velocidades = np.array([
        [0.0, v_ab, 0.0],
        [0.0, v_p, 0.0],
    ], dtype=float)

    masas = np.array([M_ab, mP], dtype=float)
    return posiciones, velocidades, masas


def simular(tiempo_total, dt):
    posiciones, velocidades, masas = cond_iniciales_proxima()

    pasos = int(tiempo_total / dt)
    trayectoria = np.zeros((pasos, 2, 3))

    for i in range(pasos):
        trayectoria[i] = posiciones
        posiciones, velocidades = runge_kutta(posiciones, velocidades, masas, dt)

    return trayectoria


if __name__ == "__main__":
    trayectoria = simular(tiempo_total, _dt)

    fig, ax = plt.subplots(figsize=(10, 10))

    colores = ["tab:blue", "tab:orange"]
    nombres = ["Baricentro A/B", "Proxima Centauri"]

    lineas = [ax.plot([], [], color=colores[i], linewidth=1.5, label=nombres[i])[0]
              for i in range(2)]
    puntos = [ax.plot([], [], 'o', color=colores[i], markersize=10 if i == 1 else 8)[0]
              for i in range(2)]

    ax.set_xlim(-15000, 15000)
    ax.set_ylim(-15000, 15000)
    # Desactivar autoescalado para evitar que los artistas cambien los límites
    ax.set_autoscalex_on(False)
    ax.set_autoscaley_on(False)
    ax.set_title('Órbita de Proxima Centauri alrededor del sistema Alfa Centauri A/B')
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.legend(loc='upper right')
    ax.axis('equal')
    ax.grid(True)

    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    def animate(frame):
        for i in range(2):
            x_data = trayectoria[:frame, i, 0]
            y_data = trayectoria[:frame, i, 1]
            x_now = trayectoria[frame, i, 0]
            y_now = trayectoria[frame, i, 1]
            lineas[i].set_data(x_data, y_data)
            puntos[i].set_data([x_now], [y_now])

        time_text.set_text(f'Tiempo: {frame * _dt:.0f} años')
        return lineas + puntos + [time_text]

    frame_step = max(1, trayectoria.shape[0] // 600)
    frames = range(0, trayectoria.shape[0], frame_step)
    anim = FuncAnimation(fig, animate, frames=frames, interval=50, blit=True, repeat=True)

    plt.tight_layout()
    plt.show()
