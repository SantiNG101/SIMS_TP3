import numpy as np

def load_params(file_path="params.txt"):
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


def load_collisions(file_path="bounce_wall_outputs.txt"):
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