import numpy as np
import os

def load_sim_base_path(L):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "..", "outputs", f"sim_L_{L}")
    base_path = os.path.abspath(base_path) 
    return base_path


def load_outputs_base_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "..", "outputs")
    base_path = os.path.abspath(base_path)
    return base_path


def load_params(L):
    base_path = load_sim_base_path(L)
    file_path = os.path.join(base_path, "params.txt")

    with open(file_path, "r") as f:
        lines = [l.strip() for l in f.readlines() if not l.startswith("#")]
    L, N, radius, BOX1_W, BOX2_W, BOX1_H = map(float, lines[0].split())
    return {
        "L": L,
        "N": int(N),
        "radius": radius,
        "BOX1_W": BOX1_W,
        "BOX2_W": BOX2_W,
        "BOX1_H": BOX1_H
    }


def load_collisions(L):
    base_path = load_sim_base_path(L)
    file_path = os.path.join(base_path, "bounce_wall_output.txt")

    dtype = {
        "names": ("box_id", "t", "vx", "vy", "wall"),
        "formats": (int, float, float, float, "U1")  # U1 = string unicode de 1 caracter
    }
    data = np.loadtxt(file_path, comments="#", dtype=dtype)
    
    return (
        data["box_id"],
        data["t"],
        data["vx"],
        data["vy"],
        data["wall"]
    )


def load_stationary_time(L):
    base_path = load_sim_base_path(L)
    path = os.path.join(base_path, "stationary.txt")

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            return float(line.split()[0])  # primera columna
    raise ValueError(f"No se encontró un valor válido en {path}")
