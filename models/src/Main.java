import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Main {
    public static void main(String[] args) throws IOException {
        // --- Simulation Parameters ---
        int N = 150;                  // Número de partículas
        double L_CHANNEL = 0.05;      // Altura del "canal" o de la caja derecha (variable)
        double RADIUS = 0.0015;       // Radio de la partícula
        double MASS = 1.0;            // Masa de la partícula
        double INITIAL_SPEED = 0.01;  // Magnitud de la velocidad inicial

        // Dimensiones de las cajas (usadas para la inicialización)
        double BOX1_WIDTH = 0.09;
        double BOX1_HEIGHT = 0.09;

        // --- Crear Partículas ---
        List<Particle> particles = new ArrayList<>();
        Random rand = new Random();

        for (int i = 0; i < N; i++) {
            double x, y;
            boolean overlap;
            do {
                overlap = false;
                // Inicialmente, todas las partículas en la cámara izquierda
                x = RADIUS + rand.nextDouble() * (BOX1_WIDTH - 2 * RADIUS);
                y = RADIUS + rand.nextDouble() * (BOX1_HEIGHT - 2 * RADIUS);

                // Verificar solapamiento con partículas existentes
                for (Particle existing : particles) {
                    double distSq = Math.pow(x - existing.x, 2) + Math.pow(y - existing.y, 2);
                    if (distSq < Math.pow(2 * RADIUS, 2)) {
                        overlap = true;
                        break;
                    }
                }
            } while (overlap);

            // Asignar velocidad inicial aleatoria
            double angle = 2 * Math.PI * rand.nextDouble();
            double vx = INITIAL_SPEED * Math.cos(angle);
            double vy = INITIAL_SPEED * Math.sin(angle);
            particles.add(new Particle(x, y, vx, vy, RADIUS, MASS));
        }

        // --- Ejecutar Simulación ---
        Collisions system = new Collisions(particles, L_CHANNEL);
        // Simular por 50 segundos, guardando el estado cada 0.1 segundos
        system.simulate(100.0, 0.1, 100);
    }
}
