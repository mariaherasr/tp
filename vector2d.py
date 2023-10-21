import math
class Vector2D:
    def __init__(self, x: float, y:float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sumar__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __restar__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mult_escalar__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __dividir_escalar__(self, scalar):
        if scalar != 0:
            return Vector2D(self.x / scalar, self.y / scalar)
        else:
            raise ValueError("No se puede dividir por cero")

    def producto_escalar(self, other):
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return Vector2D(self.x / mag, self.y / mag)
        else:
            raise ValueError("Cannot normalize the zero vector")
