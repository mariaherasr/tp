import pygame


# Clase Vector2D para gestionar vectores
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        return Vector2D(self.x / mag, self.y / mag)


# Clase Escenario para gestionar el escenario de la simulación
class Escenario:
    def __init__(self, width, height, is_closed, nombre):
        self.width = width
        self.height = height
        self.is_closed = is_closed
        self.nombre = nombre
        self.entidades = []  # Lista de entidades en el escenario

    def agregar_entidad(self, entidad):
        entidad.escenario = self
        self.entidades.append(entidad)

    def quitar_entidad(self, entidad):
        entidad.escenario = None
        self.entidades.remove(entidad)

    def actualizar(self, delta_time, restitucion):
        for entidad in self.entidades:
            entidad.actualizar(delta_time, restitucion)

    def dibujar(self, screen):
        screen.fill((255, 255, 255))  # Color de fondo blanco
        for entidad in self.entidades:
            entidad.dibujar(screen)
        pygame.display.update()


# Aquí puedes continuar implementando las demás clases y métodos necesarios.


class Ente:
    def __init__(self, posicion, velocidad, radio, color):
        self.posicion = posicion
        self.velocidad = velocidad
        self.radio = radio
        self.escenario = None
        self.color = color

    def actualizar(self, delta_time, restitucion):
        # Actualizar la posición del ente en función de su velocidad
        self.posicion = self.posicion + self.velocidad * delta_time

        # Comprobar si el ente ha colisionado con otros objetos en el escenario
        if self.escenario:
            for entidad in self.escenario.entidades:
                if entidad != self and isinstance(entidad, Ente):
                    distancia = (self.posicion - entidad.posicion).magnitude()
                    if distancia < self.radio + entidad.radio:
                        # Realizar acciones de colisión
                        self.comportamiento_colision(entidad, distancia, delta_time, restitucion)

    def dibujar(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.posicion.x), int(self.posicion.y)), self.radio)

    def comportamiento_colision(self, entidad, distancia, delta_time, restitucion):
        # Calcula el vector de separación entre las entidades
        separacion = self.posicion - entidad.posicion
        distancia_actual = separacion.magnitude()

        # Si las entidades están superpuestas, corrige su posición
        if distancia_actual < (self.radio + entidad.radio):
            # Calcula el vector de corrección
            correccion = separacion * (self.radio + entidad.radio - distancia_actual) / distancia_actual

            # Aplica la corrección a ambas entidades
            self.posicion += correccion * 0.5
            entidad.posicion -= correccion * 0.5

            # Calcula las velocidades relativas
            velocidad_relativa = self.velocidad - entidad.velocidad

            # Calcula la componente en la dirección de la corrección
            normal = correccion.normalized()
            velocidad_normal = velocidad_relativa.dot(normal)

            # Si las entidades se alejan, no hay colisión elástica
            if velocidad_normal > 0:
                return

            # Aplica la colisión elástica
            impulso = -(1 + restitucion) * velocidad_normal
            impulso /= (1 / self.radio + 1 / entidad.radio)

            # Calcula el cambio en velocidad para ambas entidades
            cambio_velocidad = impulso * normal

            # Actualiza las velocidades de las entidades
            self.velocidad += cambio_velocidad
            entidad.velocidad -= cambio_velocidad

    class Camino:
        def __init__(self, puntos):
            self.puntos = puntos  # Lista de puntos que definen el camino

        def dibujar(self, screen, color=(0, 255, 0), grosor=2):
            # Dibuja el camino en la pantalla
            for i in range(1, len(self.puntos)):
                punto_actual = (int(self.puntos[i - 1].x), int(self.puntos[i - 1].y))
                punto_siguiente = (int(self.puntos[i].x), int(self.puntos[i].y))
                pygame.draw.line(screen, color, punto_actual, punto_siguiente, grosor)

    class Comportamiento:
        def __init__(self, entidad):
            self.entidad = entidad

        def comportamiento_personalizado(self, delta_time):
            # Controlar el movimiento del jugador
            teclas = pygame.key.get_pressed()
            velocidad = 5  # Velocidad de movimiento

            if teclas[pygame.K_LEFT]:
                self.entidad.posicion.x -= velocidad * delta_time
            if teclas[pygame.K_RIGHT]:
                self.entidad.posicion.x += velocidad * delta_time
            if teclas[pygame.K_UP]:
                self.entidad.posicion.y -= velocidad * delta_time
            if teclas[pygame.K_DOWN]:
                self.entidad.posicion.y += velocidad * delta_time

    class Laberinto:
        def __init__(self, escenario, caminos):
            self.escenario = escenario
            self.caminos = caminos  # Lista de objetos Camino

        def dibujar(self, screen):
            # Dibujar el escenario
            self.escenario.dibujar(screen)

            # Dibujar los caminos en el laberinto
            for camino in self.caminos:
                camino.dibujar(screen)


# Ejemplo de uso:
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    escenario = Escenario(800, 600, True, "MiEscenario")

    # Crea y agrega entidades al escenario
    entidad1 = Ente(posicion=Vector2D(100, 100), velocidad=Vector2D(1, 0), radio=10, color=(255, 0, 0))
    entidad2 = Ente(posicion=Vector2D(200, 200), velocidad=Vector2D(-1, 0), radio=10, color=(255, 0, 0))
    escenario.agregar_entidad(entidad1)
    escenario.agregar_entidad(entidad2)

    reloj = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        delta_time = reloj.tick(60)  # Limita la velocidad de actualización a 60 FPS
        escenario.actualizar(delta_time, 1.0)
        escenario.dibujar(screen)

    pygame.quit()
