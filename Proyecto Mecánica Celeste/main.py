#aquí va la simulación numérica como tal, debe arrojar la trayectoria de cada cuerpo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cond_iniciales import cond_iniciales
from integrador import runge_kutta

tiempo_total = 20000.0  #años pq proxima es muy lento
dt = 1.0  #años por paso, si le ponía más la simulación se inestabilizaba
 
def simular(tiempo_total, dt):
    posiciones, velocidades, masas = cond_iniciales()
    
    N = len(masas)
    pasos = int(tiempo_total / dt)
    
    trayectoria = np.zeros((pasos, N, 3))
    
    for i in range(pasos):
        trayectoria[i] = posiciones
        posiciones, velocidades = runge_kutta(posiciones, velocidades, masas, dt)
    
    return trayectoria

#a partir de aquí, la IA me ayudó con el código de visualización
if __name__ == "__main__":
    trayectoria = simular(tiempo_total, dt)
    
    # Crear figura y ejes para vista completa y vista zoom de A/B
    fig, (ax_zoom, ax_full) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Colores para cada cuerpo
    colors = plt.cm.tab10(np.linspace(0, 1, trayectoria.shape[1]))
    
    # Nombres personalizados para cada cuerpo
    nombres = ["Alfa Centauri A", "Alfa Centauri B", "Proxima Centauri"]
    
    # Inicializar líneas y puntos para cada cuerpo en ambas vistas
    lines_zoom = [ax_zoom.plot([], [], color=colors[i], linewidth=1.5)[0]
                  for i in range(2)]
    points_zoom = [ax_zoom.plot([], [], 'o', color=colors[i], markersize=6)[0]
                   for i in range(2)]
    lines_full = [ax_full.plot([], [], color=colors[i], linewidth=1.5 if i < 2 else 2.5, label=nombres[i] if i < len(nombres) else f'Cuerpo {i+1}')[0]
                  for i in range(trayectoria.shape[1])]
    points_full = [ax_full.plot([], [], 'o', color=colors[i], markersize=8 if i < 2 else 12)[0]
                   for i in range(trayectoria.shape[1])]
    proxima_highlight, = ax_full.plot([], [], marker='*', color='magenta', markersize=18, zorder=10)
    
    # Configurar límites
    max_range = np.max(np.abs(trayectoria[:, :, :2])) * 1.2
    full_range = 20000.0
    ax_full.set_xlim(-full_range, full_range)
    ax_full.set_ylim(-full_range, full_range)
    ax_full.set_title('Sistema completo')
    ax_full.set_xlabel('X (AU)')
    ax_full.set_ylabel('Y (AU)')
    ax_full.legend(loc='upper right')
    ax_full.axis('equal')
    ax_full.grid()
    
    # Zoom en el par A/B
    zoom_range = 30.0
    ax_zoom.set_xlim(-zoom_range, zoom_range)
    ax_zoom.set_ylim(-zoom_range, zoom_range)
    ax_zoom.set_title('Zoom: Alfa Centauri A/B')
    ax_zoom.set_xlabel('X (AU)')
    ax_zoom.set_ylabel('Y (AU)')
    ax_zoom.axis('equal')
    ax_zoom.grid()
    
    time_text = ax_full.text(0.02, 0.95, '', transform=ax_full.transAxes)
    
    def animate(frame):
        # Actualizar solo A/B en el zoom
        for i in range(2):
            x_data = trayectoria[:frame, i, 0]
            y_data = trayectoria[:frame, i, 1]
            x_now = trayectoria[frame, i, 0]
            y_now = trayectoria[frame, i, 1]
            lines_zoom[i].set_data(x_data, y_data)
            points_zoom[i].set_data([x_now], [y_now])

        # Actualizar los tres cuerpos en la vista completa
        for i in range(trayectoria.shape[1]):
            x_data = trayectoria[:frame, i, 0]
            y_data = trayectoria[:frame, i, 1]
            x_now = trayectoria[frame, i, 0]
            y_now = trayectoria[frame, i, 1]
            lines_full[i].set_data(x_data, y_data)
            points_full[i].set_data([x_now], [y_now])

        # Resaltar Proxima Centauri en la vista completa
        x_p = trayectoria[frame, 2, 0]
        y_p = trayectoria[frame, 2, 1]
        proxima_highlight.set_data([x_p], [y_p])
        
        time_text.set_text(f'Tiempo: {frame * dt:.2f} años')
        return lines_zoom + points_zoom + lines_full + points_full + [proxima_highlight, time_text]
    
    # Ajustar la velocidad de la animación para que dure cerca de 30 segundos
    frame_step = max(1, trayectoria.shape[0] // 600)
    frames = range(0, trayectoria.shape[0], frame_step)
    anim = FuncAnimation(fig, animate, frames=frames, 
                        interval=50, blit=True, repeat=True)
    
    plt.tight_layout()
    plt.show()