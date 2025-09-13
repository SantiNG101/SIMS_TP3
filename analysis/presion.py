import numpy as np
import os
import matplotlib.pyplot as plt
from utils import load_params, load_collisions


def compute_pressure(box_id, t, vx, vy, wall, params, dt=2.0):

    perimeters = {
        1: 2 * params["BOX1_H"] + params["BOX1_W"],
        2: 2 * params["L"] + params["BOX2_W"]
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


def plot_pressure(times, pressures, base_path, fontsize=12):
    plt.figure(figsize=(10,5))
    for b in pressures:
        if b == 1: label = "Caja izquierda"
        else: label = "Caja derecha"
        plt.plot(times, pressures[b], label=label)
    plt.xlabel("Tiempo [s]", fontsize=fontsize)
    plt.ylabel("Presión [Pa]", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.grid(True)
    save_path = os.path.join(base_path, f"presion_vs_t.png")
    plt.savefig(save_path, dpi=300)
    print(f"Gráfico guardado en: {save_path}")




if __name__ == "__main__":
    
    L = 0.09

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "..", "outputs", f"sim_L_{L}")
    base_path = os.path.abspath(base_path) 

    params = load_params(os.path.join(base_path, "params.txt"))
    box_id, t, vx, vy, wall = load_collisions(os.path.join(base_path, "bounce_wall_output.txt"))

    times, pressures = compute_pressure(box_id, t, vx, vy, wall, params)

    plot_pressure(times, pressures, base_path, fontsize=12)
