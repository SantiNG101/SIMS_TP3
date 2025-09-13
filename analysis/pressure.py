import numpy as np
from utils import load_params, load_collisions, load_stationary_time


def compute_pressure(L, dt=2.0):

    params = load_params(L)
    r = params["radius"]
    box_id, t, vx, vy, wall = load_collisions(L)

    perimeters = {
        1: 2 * (params["BOX1_H"] + params["BOX1_W"] - 2*r),
        2: 2 * (params["L"] + params["BOX2_W"] - 2*r)
    }
    
    # Busco el tiempo máximo de la simulación
    t_max = np.max(t) 

    # Creo un arreglo de intervalos de tiempo (bins) que va desde 0 hasta t_max, con pasos de dt.
    bins = np.arange(0, t_max + dt, dt)

    # Inicializo un diccionario para almacenar las presiones calculadas para cada caja
    pressures = {1: np.zeros(len(bins)-1), 2: np.zeros(len(bins)-1)}

    for b in [1, 2]:
        mask = box_id == b
        t_box, vx_box, vy_box, wall_box = t[mask], vx[mask], vy[mask], wall[mask]

        # Δp por choque = 2 * |componente normal de la velocidad|
        dp = np.zeros_like(t_box)
        dp[wall_box == "V"] = 2 * np.abs(vx_box[wall_box == "V"])   # choque con pared vertical
        dp[wall_box == "H"] = 2 * np.abs(vy_box[wall_box == "H"])   # choque con pared horizontal
        dp[wall_box == "C"] = 2 * np.sqrt(vx_box[wall_box == "C"]**2 + vy_box[wall_box == "C"]**2)  # esquina

        # Counts = array donde cada posición representa el impulso total acumulado en ese intervalo de tiempo.
        counts, _ = np.histogram(t_box, bins=bins, weights=dp)

        # Presión = (Δp/Δt) / "área"
        pressures[b] = counts / (dt * perimeters[b])
    
    return bins[:-1], pressures


# Calcula la presión promedio estacionaria de ambas cajas (promedio de P_left y P_right).
def compute_stationary_mean_pressure(L):
    t_stationary = load_stationary_time(L)
    times, pressures = compute_pressure(L, dt=10.0)

    mask = times >= t_stationary

    P_left_data = pressures[1][mask]
    P_right_data = pressures[2][mask]

    P_left = np.mean(P_left_data)
    P_right = np.mean(P_right_data)
    P_avg = 0.5 * (P_left + P_right)

    P_left_std = np.std(P_left_data)
    P_right_std = np.std(P_right_data)
    P_avg_std = 0.5 * (P_left_std + P_right_std)

    return P_left, P_right, P_avg, P_avg_std
