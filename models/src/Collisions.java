import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Locale;
import java.util.PriorityQueue;

public class Collisions {
    private PriorityQueue<Event> pq;
    private double simTime;
    private final List<Particle> particles;

    private final double BOX1_W = 0.09;
    private final double BOX1_H = 0.09;
    private final double BOX2_W = 0.09;
    private final double L; // Altura del canal / caja derecha

    private final double openingYMin;
    private final double openingYMax;

    private final double EPS = 1e-10;

    public Collisions(List<Particle> particles, double L_channel) {
        this.particles = particles;
        this.L = L_channel;
        this.simTime = 0.0;
        this.pq = new PriorityQueue<>();

        this.openingYMin = (BOX1_H - L) / 2.0;
        this.openingYMax = openingYMin + L;
    }

    private void predict(Particle p) {
        if (p == null) return;

        // 1️⃣ Colisiones con otras partículas
        for (Particle other : particles) {
            double dt = p.timeToHit(other);
            if (dt > 1e-12 && simTime + dt < Double.POSITIVE_INFINITY) {
                pq.add(new Event(simTime + dt, p, other));
            }
        }
        boolean willPassToRight = false;
        // 2️⃣ Colisiones con paredes verticales
        if (p.vx > 0) {
            if (p.x < BOX1_W) { // Caja izquierda
                double t = (BOX1_W - p.radius - p.x) / p.vx;
                double yAtCollision = p.y + p.vy * t;

                if (yAtCollision + p.radius <= openingYMax && yAtCollision - p.radius >= openingYMin) {
                    willPassToRight = true;
                     t = (BOX1_W + BOX2_W - p.radius - p.x) / p.vx;
                    if (t > 1e-12) pq.add(new Event(simTime + t, p, null));
                } else {
                    if (t > 1e-12) pq.add(new Event(simTime + t, p, null));
                    else pq.add(new Event(simTime + 1e-12, p, null));
                }
            } else { // Caja derecha
                double t = (BOX1_W + BOX2_W - p.radius - p.x) / p.vx;
                if (t > 1e-12) pq.add(new Event(simTime + t, p, null));
            }
        } else if (p.vx < 0) {
            double t = (0 + p.radius - p.x) / p.vx;
            if (t > 1e-12) pq.add(new Event(simTime + t, p, null));
        }

        // 3️⃣ Colisiones con paredes horizontales
        double yMin, yMax;
        if (p.x <= BOX1_W && !willPassToRight) {
            yMin = 0.0; yMax = BOX1_H;
        } else {
            yMin = openingYMin; yMax = openingYMax;
        }

        if (p.vy > 0) {
            double t = (yMax - p.radius - p.y) / p.vy;
            if (t > 1e-12) pq.add(new Event(simTime + t, null, p));
        } else if (p.vy < 0) {
            double t = (yMin + p.radius - p.y) / p.vy;
            if (t > 1e-12) pq.add(new Event(simTime + t, null, p));
        }

        // 4️⃣ Colisiones con esquinas (solo si se dirige hacia ellas)
        if (p.vx > 0 && (p.y - p.radius< openingYMin || p.y + p.radius > openingYMax)) {
            double cornerY = (p.y < openingYMin) ? openingYMin : openingYMax;
            double tCorner = p.timeToHitPoint(BOX1_W, cornerY);
            if (tCorner > 1e-12) pq.add(new Event(simTime + tCorner, p, null));
        }
    }



    public void simulate(double maxTime, double outputInterval) throws IOException {
        for (Particle p : particles) {
            predict(p);
        }
        pq.add(new Event(0, null, null)); // evento para estado inicial
        double nextOutputTime = 0;

        String simPath = String.format(Locale.US, "outputs/sim_L_%.2f", L);
        File folder = new File(simPath);
        if (!folder.exists()) {
            folder.mkdirs(); // crea la carpeta si no existe
        }

        try (
            FileWriter paramsWriter = new FileWriter(simPath + "/params.txt");
            FileWriter outputWriter = new FileWriter(simPath + "/output.txt")
            ) {
            paramsWriter.write("# L, N, radius, BOX1_W, BOX2_W, BOX1_H\n");
            paramsWriter.write(String.format(
                Locale.US,
                "%.6f %d %.6f %.6f %.6f %.6f\n",
                L, particles.size(), particles.get(0).radius, BOX1_W, BOX2_W, BOX1_H
            ));
            outputWriter.write("# t\n");
            outputWriter.write("# x y vx vy\n");

            while (!pq.isEmpty()) {
                Event event = pq.poll();
                if (!event.isValid()) continue;
                if (event.time < simTime - 1e-12) continue; // evento en el pasado (por seguridad)

                for (Particle p : particles) {
                    p.move(event.time - simTime);
                }
                simTime = event.time;

                if (simTime + 1e-12 >= nextOutputTime) {
                    outputWriter.write(String.format(Locale.US,"%.6f\n", simTime));
                    for (Particle p : particles) {
                        outputWriter.write(String.format(Locale.US,"%.6f %.6f %.6f %.6f\n", p.x, p.y, p.vx, p.vy));
                    }
                    nextOutputTime += outputInterval;
                }

                if (simTime > maxTime) break;

                Particle a = event.a;
                Particle b = event.b;

                if (a != null && b != null) {
                    a.bounceOff(b);
                } else if (a != null && b == null) {
                    double EPS = 1e-10;
                    if (isCorner(a)) {
                        double cornerY = (aNearBottomCorner(a)) ? openingYMin : openingYMax;
                        a.bounceOffPoint(BOX1_W, cornerY, EPS);
                    } else {
                        a.bounceOffVerticalWall();
                    }
                } else if (a == null && b != null) {
                    b.bounceOffHorizontalWall();
                }

                predict(a);
                predict(b);
            }
        }

        System.out.println("Simulation finished.");
    }

    private boolean isCorner(Particle p) {
        return Math.abs(p.x - BOX1_W) < 1e-6 &&
                (Math.abs(p.y - openingYMin) < 1e-6 || Math.abs(p.y - openingYMax) < 1e-6);
    }

    private boolean aNearBottomCorner(Particle p) {
        return Math.abs(p.y - openingYMin) < Math.abs(p.y - openingYMax);
    }

}








