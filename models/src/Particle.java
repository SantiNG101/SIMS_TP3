public class Particle {
    public double x, y, vx, vy, radius, mass;
    public int collisionCount;

    public Particle(double x, double y, double vx, double vy, double radius, double mass) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.radius = radius;
        this.mass = mass;
        this.collisionCount = 0;
    }

    public void move(double dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
    }

    public double timeToHit(Particle other) {
        if (this == other) return Double.POSITIVE_INFINITY;

        double dx = other.x - this.x;
        double dy = other.y - this.y;
        double dvx = other.vx - this.vx;
        double dvy = other.vy - this.vy;

        double dvdr = dvx * dx + dvy * dy;
        if (dvdr > 0) return Double.POSITIVE_INFINITY;

        double dvdv = dvx * dvx + dvy * dvy;
        if (dvdv == 0) return Double.POSITIVE_INFINITY;

        double drdr = dx * dx + dy * dy;
        double sigma = this.radius + other.radius;

        double d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma);
        if (d < 0) return Double.POSITIVE_INFINITY;

        double t = -(dvdr + Math.sqrt(d)) / dvdv;
        return t > 0 ? t : Double.POSITIVE_INFINITY;
    }

    public double timeToHitVerticalWall(double xMin, double xMax) {
        if (vx > 0) return (xMax - radius - x) / vx;
        if (vx < 0) return (xMin + radius - x) / vx;
        return Double.POSITIVE_INFINITY;
    }

    public double timeToHitHorizontalWall(double yMin, double yMax) {
        if (vy > 0) return (yMax - radius - y) / vy;
        if (vy < 0) return (yMin + radius - y) / vy;
        return Double.POSITIVE_INFINITY;
    }

    public double timeToHitPoint(double px, double py) {
        double dx = px - this.x;
        double dy = py - this.y;
        double dvx = this.vx;
        double dvy = this.vy;

        double dvdr = dx * dvx + dy * dvy;
        if (dvdr <= 0) return Double.POSITIVE_INFINITY;

        double dvdv = dvx * dvx + dvy * dvy;
        if (dvdv == 0) return Double.POSITIVE_INFINITY;

        double drdr = dx * dx + dy * dy;
        double sigma = this.radius;

        double d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma);
        if (d < 0) return Double.POSITIVE_INFINITY;

        double t = -(dvdr + Math.sqrt(d)) / dvdv;
        return t > 0 ? t : Double.POSITIVE_INFINITY;
    }

    public void bounceOff(Particle other) {
        double dx = other.x - this.x;
        double dy = other.y - this.y;
        double dvx = other.vx - this.vx;
        double dvy = other.vy - this.vy;

        double dvdr = dx * dvx + dy * dvy;
        double dist = this.radius + other.radius;

        double impulse = (2 * this.mass * other.mass * dvdr) / ((this.mass + other.mass) * dist);
        double Jx = impulse * dx / dist;
        double Jy = impulse * dy / dist;

        this.vx += Jx / this.mass;
        this.vy += Jy / this.mass;
        other.vx -= Jx / other.mass;
        other.vy -= Jy / other.mass;

        this.collisionCount++;
        other.collisionCount++;
    }

    public void bounceOffVerticalWall() {
        this.vx = -this.vx;
        this.collisionCount++;
    }

    public void bounceOffHorizontalWall() {
        this.vy = -this.vy;
        this.collisionCount++;
    }

    public void bounceOffCorner() {
        // reflejar vx y vy según la normal del corner
        vx = -vx;
        vy = -vy;
        collisionCount++;
    }


    public void bounceOffPoint(double px, double py, double EPS) {
        double dx = this.x - px;
        double dy = this.y - py;
        double dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < EPS) return; // ignorar rebotes demasiado cercanos

        double nx = dx / dist;
        double ny = dy / dist;

        double vdotn = vx * nx + vy * ny;

        vx -= 2 * vdotn * nx;
        vy -= 2 * vdotn * ny;

        collisionCount++;
    }

}



