import os

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import imageio_ffmpeg as ffmp
import matplotlib as mpl

def animate_simulation(L_value):
    """
    Analiza los datos de la simulación y crea una animación en Matplotlib.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sim_folder = os.path.join(base_dir, "outputs", f"sim_L_{L_value:.2f}")

    output_file = os.path.join(sim_folder, "output.txt")
    params_file = os.path.join(sim_folder, "params.txt")
    gif_file = os.path.join(sim_folder, f"animation.gif")

    if not os.path.exists(output_file):
        print(f"No se encontró el archivo de salida en {output_file}")
        return
    if not os.path.exists(params_file):
        print(f"No se encontró el archivo de parámetros en {params_file}")
        return

    # --- Leer parámetros ---
    with open(params_file, 'r') as f:
        lines = [line for line in f.readlines() if not line.startswith("#")]
        L_CHANNEL, num_particles, radius, BOX1_WIDTH, BOX2_WIDTH, BOX1_HEIGHT = map(float, lines[0].split())
        num_particles = int(num_particles)

    # --- Leer frames ---
    frames = []
    with open(output_file, 'r') as f:
        content = f.read().strip().split("\n")
        i = 0
        while i < len(content):
            if not content[i].strip() or content[i].startswith("#"):
                i += 1
                continue
            # línea del tiempo (no la usamos, pero la salteamos)
            i += 1
            frame_data = []
            for _ in range(num_particles):
                if i >= len(content):
                    break
                parts = list(map(float, content[i].split()))
                frame_data.append(parts[:2])  # solo x, y
                i += 1
            if len(frame_data) == num_particles:
                frames.append(np.array(frame_data))

    if not frames:
        print("No se encontraron frames válidos para animar. Saliendo.")
        return

    print("Frame 0:", frames[0][:5])  # primeras 5 partículas
    print("Frame 1:", frames[1][:5])

    print(f"Se leyeron {len(frames)} frames para {num_particles} partículas.")

    # --- Configurar el gráfico ---
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_aspect('equal')
    ax.set_title(f"Difusión de Gas 2D (L={L_CHANNEL:.2f})")

    # --- Dibujar el contorno del contenedor ---
    opening_y_min = (BOX1_HEIGHT - L_CHANNEL) / 2
    opening_y_max = opening_y_min + L_CHANNEL
    total_width = BOX1_WIDTH + BOX2_WIDTH

    wall_vertices = [
        (0, 0),
        (BOX1_WIDTH, 0),
        (BOX1_WIDTH, opening_y_min),
        (total_width, opening_y_min),
        (total_width, opening_y_max),
        (BOX1_WIDTH, opening_y_max),
        (BOX1_WIDTH, BOX1_HEIGHT),
        (0, BOX1_HEIGHT),
        (0, 0)
    ]
    wall_x, wall_y = zip(*wall_vertices)
    ax.plot(wall_x, wall_y, color='black')

    ax.set_xlim(-0.01, total_width + 0.01)
    ax.set_ylim(-0.01, BOX1_HEIGHT + 0.01)

    # --- Crear partículas ---
    patches = [plt.Circle(xy, radius, fc='royalblue') for xy in frames[0]]
    for patch in patches:
        ax.add_patch(patch)

    # --- Función de actualización ---
    def update(frame_index):
        positions = frames[frame_index]
        for i, patch in enumerate(patches):
            patch.center = (positions[i, 0], positions[i, 1])
        return patches

    # --- Animación ---
    ani = animation.FuncAnimation(
        fig, update, frames=len(frames),
        blit=True, interval=30, repeat=False
    )

    mpl.rcParams["animation.ffmpeg_path"] = ffmp.get_ffmpeg_exe()
    ani.save(f"simulation_L_{L_value}_.mp4", writer='ffmpeg', fps=30)
    #    ani.save('simulation_L_0.03_.gif', writer='pillow', fps=30)
    print(f"Animación guardada exitosamente como 'animation_L_{L_value}.gif'!")


if __name__ == '__main__':
    animate_simulation(0.05)