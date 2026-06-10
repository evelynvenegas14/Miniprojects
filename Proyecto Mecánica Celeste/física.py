import numpy as np

G=4*np.pi**2 #constante de gravitación en unidades de AU^3/(masa solar*año^2)
#para que cuadrara en la visualización

def aceleraciones(posiciones, masas):
    """
    Aceleraciones de cada cuerpo usando las ecuaciones de movimiento
    dr_i/dt^2 = G * sum_{j!=i} m_j * (r_j - r_i) / |r_j - r_i|^3
    
    Entra:
    posiciones: array de forma (N, 3) con las posiciones de los cuerpos.
    masas: array de forma (N,) con las masas de los cuerpos.
    
    Retorna:
    aceleraciones: array de forma (N, 3) con las aceleraciones de los cuerpos.
    """
    N = len(masas)
    aceleraciones = np.zeros_like(posiciones)
    
    for i in range(N):
        for j in range(N):
            if i != j:
                r_vec = posiciones[j] - posiciones[i]
                r_mag = np.linalg.norm(r_vec)
                if r_mag > 0:
                    aceleraciones[i] += G * masas[j] * r_vec / r_mag**3
    
    return aceleraciones