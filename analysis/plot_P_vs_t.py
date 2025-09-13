import os
import matplotlib.pyplot as plt
from pressure import compute_pressure
from utils import load_base_path

def plot_pressure_vs_time(times, pressures, base_path, fontsize=12):
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
    
    L = 0.05
    dt = 2.0
    fontsize = 12

    times, pressures = compute_pressure(L, dt)

    base_path = load_base_path(L)
    plot_pressure_vs_time(times, pressures, base_path, fontsize)