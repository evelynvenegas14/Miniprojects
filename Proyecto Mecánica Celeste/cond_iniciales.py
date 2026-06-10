import numpy as np

#CONDICIONES INICIALES PARA LA VISUALIZACION DOBLE

def cond_iniciales():
    #en masas solares
    mA = 1.1
    mB = 0.9
    mP = 0.125

    #sistema binario
    a_AB = 23.3          #semieje mayor, UA
    e_AB = 0.52          #excentricidad
    r_peri_AB = a_AB * (1 - e_AB)

    #posicion respecto del baricentro A/B, con A a la izquierda y B a la derecha
    rA = - mB / (mA + mB) * r_peri_AB
    rB =   mA / (mA + mB) * r_peri_AB

    #velocidad relativa, vis-viva
    G = 4 * np.pi**2
    v_rel = np.sqrt(G * (mA + mB) * (2 / r_peri_AB - 1 / a_AB))

    #velocidades individuales de A y B
    vA =  mB / (mA + mB) * v_rel
    vB = -mA / (mA + mB) * v_rel

    #proxima muy lejos del par A-B
    rP = 13000.0  #distancia inicial en AU, la distancia actual
    vP = np.sqrt(G * (mA + mB + mP) / rP)

    posiciones = np.array([
        [rA, 0.0, 0.0],   #alfa centauri A
        [rB, 0.0, 0.0],   #alfa centauri B
        [rP, 0.0, 0.0],   #proxima centauri
    ], dtype=float)

    velocidades = np.array([
        [0.0,  vA, 0.0],  #A  se mueve hacia +y
        [0.0,  vB, 0.0],  #B se mueve hacia -y
        [0.0,  vP, 0.0],  #proxima orbita el baricentro
    ], dtype=float)

    masas = np.array([mA, mB, mP], dtype=float)

    return posiciones, velocidades, masas