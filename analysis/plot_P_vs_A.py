import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pressure import compute_stationary_mean_pressure
from utils import load_params, load_outputs_base_path

def compute_pressure_vs_area(L_values):

    A_list, P_avg_list, P_std_list = [], [], []

    for L in L_values:
        # Cargar parámetros de la simulación
        params = load_params(L)
        r = params["radius"]
        
        # Calcular presiones estacionarias
        P_left, P_right, P_avg, P_avg_std = compute_stationary_mean_pressure(L)

        # Calcular área total del sistema
        A_total = (params["BOX1_W"]-r) * (params["BOX1_H"]-r) + (params["BOX2_W"]-r) * (params["L"]-r)

        A_list.append(A_total)
        P_avg_list.append(P_avg)
        P_std_list.append(P_avg_std)

        print(f"L={L:.2f} → A={A_total:.4f}, P_avg={P_avg:.4f}")
    return A_list, P_avg_list, P_std_list


def plot_pressure_vs_area(A_list, P_avg_list, P_std_list, inverse=False, fontsize=12):

    if inverse:
        A_list = [1/A for A in A_list]

    plt.figure(figsize=(8,6))
    plt.plot(A_list, P_avg_list, "o-")
    plt.xlabel("Área total A⁻¹ (1/m²)" if inverse else "Área total A (m²)", fontsize=fontsize)
    plt.ylabel("Presión promedio (Pa)", fontsize=fontsize)
    plt.ylim(0, 2)
    plt.grid(True)

    xtick_labels = [f"{A:.3f}\n(L={L:.2f})" for A, L in zip(A_list, L_values)]
    plt.xticks(A_list, xtick_labels, fontsize=fontsize-1)    
    plt.yticks(fontsize=fontsize)

    plt.errorbar(A_list, P_avg_list, yerr=P_std_list, fmt='o', capsize=5, color='blue', label='P promedio')

    base_path = load_outputs_base_path()
    if inverse:
        save_path = os.path.join(base_path, "presion_vs_inverse_area.png")
    else:
        save_path = os.path.join(base_path, "presion_vs_area.png")
    plt.savefig(save_path, dpi=300)
    print(f"Gráfico guardado en: {save_path}")


def plot_PA_table(A_list, P_avg_list):
    
    # Calcular P·A
    PA_list = [P*A for P, A in zip(P_avg_list, A_list)]

    df = pd.DataFrame({
        "L [m]": L_values,
        "A_total [m²]": A_list,
        "P_avg [Pa]": P_avg_list,
        "P·A [Pa·m²]": PA_list
    })

    base_path = load_outputs_base_path()
    table_file = os.path.join(base_path, "PA_table.csv")
    df.to_csv(table_file, index=False, float_format="%.3f")
    print(f"Tabla guardada en: {table_file}")


def plot_pressure_fit_vs_inverse_area(A_list, P_avg_list, fontsize=12):
    # Transformación A^-1
    A_inv = np.array([1/A for A in A_list])
    P_avg = np.array(P_avg_list)  

    # Ajuste lineal: P = k * (1/A) + b
    coeffs = np.polyfit(A_inv, P_avg_list, 1)  # grado 1 → lineal
    k, b = coeffs

    # Graficar
    plt.figure(figsize=(8,6))
    plt.plot(A_inv, P_avg_list, 'o')
    plt.plot(A_inv, k*A_inv + b, '-')
    plt.xlabel("1 / A [1/m²]", fontsize=fontsize)
    plt.ylabel("P [Pa]", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)    
    plt.yticks(fontsize=fontsize)
    plt.grid(True)

    base_path = load_outputs_base_path()
    save_path = os.path.join(base_path, "ajuste_lineal.png")
    plt.savefig(save_path, dpi=300)
    print(f"Gráfico guardado en: {save_path}")


if __name__ == "__main__":
    
    L_values = [0.03, 0.05, 0.07, 0.09]
    fontsize = 12

    A_list, P_avg_list, P_std_list = compute_pressure_vs_area(L_values)

    plot_pressure_vs_area(A_list, P_avg_list, P_std_list, True, fontsize)
    plot_pressure_vs_area(A_list, P_avg_list, P_std_list, False, fontsize)
    plot_PA_table(A_list, P_avg_list)
    plot_pressure_fit_vs_inverse_area(A_list, P_avg_list, fontsize)
