import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os
from utils import load_sim_base_path, load_outputs_base_path

def load_output_file(L, base_path, t_stationary=0):
    """
    Carga el archivo output.txt para un L dado.
    Devuelve tiempos y posiciones (x,y) de todas las partículas, solo a partir de t_stationary.
    """
    file_path = os.path.join(base_path, "output.txt")

    times = []
    positions = []

    with open(file_path, "r") as f:
        lines = f.readlines()

    block = []
    current_time = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values = list(map(float, line.split()))
        if len(values) == 1:
            # nueva marca de tiempo
            if block:
                positions.append(np.array(block))
                block = []
            current_time = values[0]
            times.append(current_time)
        else:
            # fila con x, y, vx, vy
            x, y, vx, vy = values
            block.append([x, y])

    # último bloque
    if block:
        positions.append(np.array(block))

    times = np.array(times)
    positions = np.array(positions)

    # --- Filtrar desde estado estacionario ---
    mask = times >= t_stationary
    times = times[mask] - t_stationary  # reiniciar tiempo desde t_stationary
    positions = positions[mask]

    return times, positions


def compute_msd(times, positions, bin_size):
    """
    Calcula el MSD agrupando los datos de las colisiones por bin.
    Devuelve la media y std de cada bin.
    """
    N_times = len(times)

    r0 = positions[0]
    msd_list = []

    for t_idx in range(N_times):
        r = positions[t_idx]
        dr = r - r0
        dr2 = np.sum(dr**2, axis=1)  # |r-r0|^2 por partícula
        msd_list.append(dr2)

    msd_array = np.array(msd_list)

    # Agrupar cada bin_size pasos
    binned_times = []
    binned_msd = []
    binned_std = []

    for i in range(0, N_times, bin_size):
        bin_times = times[i:i+bin_size]
        bin_msd = msd_array[i:i+bin_size, :].mean(axis=1)
        binned_times.append(bin_times.mean())
        binned_msd.append(bin_msd.mean())
        binned_std.append(bin_msd.std())

    return np.array(binned_times), np.array(binned_msd), np.array(binned_std)


def fit_diffusion_coefficient(times, msd):
    """
    Ajuste lineal del MSD(t) = 4 D t en 2D.
    """
    slope, intercept, r_value, _, _ = linregress(times, msd)
    D = slope / 4  # en 2D

    return D, slope, intercept, r_value**2


def plot_diffusion(t_stationary, fontsize=12, L=0.09):

    base_path = load_sim_base_path(L)
    times, positions = load_output_file(L, base_path, t_stationary=t_stationary)

    # MSD agrupado cada 10000 datos
    bin_size = 10000
    times_b, msd_b, msd_std = compute_msd(times, positions, bin_size)

    # Ajuste lineal
    D, slope, intercept, r2 = fit_diffusion_coefficient(times_b, msd_b)

    times_fit = times_b
    msd_fit = slope*times_fit + intercept

    # Graficar con barra de error
    plt.figure(figsize=(8,6))
    plt.errorbar(times_b, msd_b, yerr=msd_std, fmt='o-', capsize=5, label=f"Datos")
    plt.plot(times_fit, msd_fit, '-', label=f"Ajuste lineal")

    plt.title(f"Coeficiente de difusión D = {D:.5e} m²/s\n")
    plt.xlabel("Tiempo desde estado estacionario (s)", fontsize=fontsize)
    plt.ylabel("MSD (m²)", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize)
    plt.grid(True)

    base_path = load_outputs_base_path()
    save_path = os.path.join(base_path, "msd.png")
    plt.savefig(save_path, dpi=300)
    print(f"Gráfico guardado en: {save_path}")

    print(f"Coeficiente de difusión D = {D:.5e} m²/s")


if __name__ == "__main__":

    t_init_stationary = 200
    fontsize = 14

    plot_diffusion(t_init_stationary, fontsize)