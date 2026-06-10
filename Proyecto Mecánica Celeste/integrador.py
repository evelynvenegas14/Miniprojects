#aquí va la evolución temporal con el método de RungeKutta de cuarto orden
import numpy as np
from física import aceleraciones
def runge_kutta(posiciones, velocidades, masas, dt):
    """
    Integra las ecuaciones de movimiento usando el método de Runge-Kutta 4.
    
    Entra:
    posiciones: array de forma (N, 3) con las posiciones actuales de los cuerpos.
    velocidades: array de forma (N, 3) con las velocidades actuales de los cuerpos.
    masas: array de forma (N,) con las masas de los cuerpos.
    dt: paso de tiempo.
    
    Retorna:
    nuevas_posiciones: array de forma (N, 3) con las nuevas posiciones de los cuerpos.
    nuevas_velocidades: array de forma (N, 3) con las nuevas velocidades de los cuerpos.
    """
    k1_v = aceleraciones(posiciones, masas)
    k1_p = velocidades
    
    k2_v = aceleraciones(posiciones + 0.5 * dt * k1_p, masas)
    k2_p = velocidades + 0.5 * dt * k1_v
    
    k3_v = aceleraciones(posiciones + 0.5 * dt * k2_p, masas)
    k3_p = velocidades + 0.5 * dt * k2_v
    
    k4_v = aceleraciones(posiciones + dt * k3_p, masas)
    k4_p = velocidades + dt * k3_v
    
    nuevas_posiciones = posiciones + (dt / 6) * (k1_p + 2*k2_p + 2*k3_p + k4_p)
    nuevas_velocidades = velocidades + (dt / 6) * (k1_v + 2*k2_v + 2*k3_v + k4_v)
    
    return nuevas_posiciones, nuevas_velocidades