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
        if (this == other) {
            return Double.POSITIVE_INFINITY;
        }

        double dx = other.x - this.x;
        double dy = other.y - this.y;
        double dvx = other.vx - this.vx;
        double dvy = other.vy - this.vy;

        double dvdr = dvx * dx + dvy * dy;
        if (dvdr > 0) {
            return Double.POSITIVE_INFINITY;
        }

        double dvdv = dvx * dvx + dvy * dvy;
        double drdr = dx * dx + dy * dy;
        double sigma = this.radius + other.radius;

        double d = (dvdr * dvdr) - dvdv * (drdr - sigma * sigma);
        if (d < 0) {
            return Double.POSITIVE_INFINITY;
        }

        return -(dvdr + Math.sqrt(d)) / dvdv;
    }

    public double timeToHitVerticalWall(double wallX, double boxWidth) {
        if (vx > 0) return (boxWidth - radius - x) / vx;
        if (vx < 0) return (radius - x) / vx;
        return Double.POSITIVE_INFINITY;
    }

    public double timeToHitHorizontalWall(double wallY, double boxHeight) {
        if (vy > 0) return (boxHeight - radius - y) / vy;
        if (vy < 0) return (radius - y) / vy;
        return Double.POSITIVE_INFINITY;
    }

    public void bounceOff(Particle other){
        double dx = other.x - this.x;
        double dy = other.y - this.y;
        double dvx = other.vx - this.vx;
        double dvy = other.vy - this.vy;

        double dvdr = dvx * dx + dvy * dy;
        double dist = this.radius + other.radius;

        double impulse = (2 * this.mass * other.mass * dvdr) / ((this.mass + other.mass) * dist);
        double jx = impulse * dx / dist;
        double jy = impulse * dy / dist;

        this.vx += jx / this.mass;
        this.vy += jy / this.mass;
        other.vx -= jx / other.mass;
        other.vy -= jy / other.mass;

        this.collisionCount++;
        other.collisionCount++;
    }

    public void bounceOffVerticalWall(){
        this.vx = -this.vx;
        this.collisionCount++;
    }

    public void bounceOffHorizontalWall(){
        this.vy = -this.vy;
        this.collisionCount++;
    }
}
