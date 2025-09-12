import os

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import imageio_ffmpeg as ffmp
import matplotlib as mpl

def animate_simulation(filename="simulation_output_L_0.07_.txt"):
    """
    Analiza los datos de la simulación y crea una animación en Matplotlib.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, filename)

    with open(filepath, 'r') as f:
        # --- Leer cabecera ---
        num_particles, radius = map(float, f.readline().split())
        num_particles = int(num_particles)
        L_CHANNEL, BOX1_WIDTH, BOX2_WIDTH, BOX1_HEIGHT = map(float, f.readline().split())

        # --- Leer frames ---
        frames = []
        content = f.read().strip().split("\n")
        i = 0
        while i < len(content):
            if not content[i].strip():
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

    print("Guardando animación como GIF... Esto puede tardar un momento. ✨")
    # ani.save('simulation_L_0.03_.gif', writer='pillow', fps=30)
    mpl.rcParams["animation.ffmpeg_path"] = ffmp.get_ffmpeg_exe()
    ani.save('simulation_L_0.03_.mp4', writer='ffmpeg', fps=30)
    print("Animación guardada exitosamente como 'simulation_L_0.05_.gif'!")


if __name__ == '__main__':
    animate_simulation()