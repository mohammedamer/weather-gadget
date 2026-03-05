

def lipo_percent(v):
    # Clamp to expected 1S LiPo range
    if v <= 3.20:
        return 0
    if v >= 4.20:
        return 100

    # Piecewise approximation (rested battery, light load)
    # Tuned to feel reasonable for small LiPos in real devices
    points = [
        (3.20, 0),
        (3.50, 5),
        (3.60, 10),
        (3.70, 20),
        (3.75, 30),
        (3.80, 40),
        (3.85, 55),
        (3.90, 70),
        (4.00, 85),
        (4.10, 95),
        (4.20, 100),
    ]

    # Linear interpolation between the nearest points
    for i in range(len(points) - 1):
        v0, p0 = points[i]
        v1, p1 = points[i + 1]
        if v0 <= v <= v1:
            return int(p0 + (p1 - p0) * (v - v0) / (v1 - v0))

    return 0
