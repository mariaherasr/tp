import math
import vector2d

class Color:
    NEGRO = (0, 0, 0)
    BLANCO = (255, 255, 255)
    AMARILLO = (255, 255, 0)
    ROSA = (255, 0, 0)
    AZUL = (0, 255, 255)
    VERDE = (0, 255, 0)

class Ente:
    def __init__(self, posicion, forma, color: Color, velocidad, width, height=None):
        self.posicion = posicion
        self.forma = forma
        self.width = width
        self.escenario = None #va a indicar el escenario al que pertenece
        self.esta_fijo = False #true si está fijo, false si no se mueve
        self.color = color
        self.velocidad = velocidad

        if self.forma == 'circle':
            self.height = forma.width #el círculo solo necesita un radio para definirse
        elif self.forma == 'rectangle':
            if height is None:
                raise ValueError("Para crear un rectángulo se necesitan el ancho y el alto")
            self.height = height
        else:
            raise ValueError("Forma no válida: usa 'circle' o 'rectangle'.")

    def asignar_escenario(self, escenario):
        self.escenario = escenario

    def dist(self, other) -> float: #la distancia de una identidad (self) a otra(other)
        if self.forma == 'circle' and other.forma == 'circle': #necesitamos centro y radio del circulo asociado a cada elemento, elegimos el menor radio cuyo circulo permita cubrir todo el elemento
            return (self.posicion - other.posicion).magnitude()
        elif self.forma == 'rectangle' and other.forma == 'rectangle':
            self.posicion
            dx = max(0, abs(self.x - other.x) - (self.width + other.width) / 2)
            dy = max(0, abs(self.y - other.y) - (self.height + other.height) / 2)
            return math.sqrt(dx ** 2 + dy ** 2)
        else: #self es rectangle y other circle
            aprox_x = max(other.x - other.width / 2, min(self.x, other.x + other.width / 2))
            aprox_y = max(other.y - other.height / 2, min(self.y, other.y + other.height / 2))
            dx = self.x - aprox_x
            dy = self.y - aprox_y
            return math.sqrt(dx ** 2 + dy ** 2)

    def colision(self, other) -> bool: #hay que distinguir entre formas
        if self.forma == 'circle' and other.forma == 'circle':
            distancia = self.dist(other)
            return distancia < self.width + other.width
        elif self.forma == 'rectangle' and other.rectangle =='rectangle':
            if self.x > (other.x + other.width):
                return False
            elif (self.x + self.width) < other.x:
                return False
            elif self.y > (other.y + other.height):
                return False
            elif (self.y + self.height) < other.y:
                return False
            else:
                return True
        else: #hay colision cuando la distancia del centro del circulo y el punto del perimetro del rectangulo qie esté más cerca del mismo sea menor que el radio del circulo
            '''
            tomamos x e y del circulo como las coordenadas de su centro
            y las coordenadas x e y del rectangulo representaran las coordenadas del punto de la esquina superior izquierda
            (px,py) punto del perimetro del rectángulo 
            '''
            px = self.x #al principio son iguales
            if px < other.x:
                px = other.x
            elif px > other.x + other.width:
                px = other.x + other.width

            py = self.y  # al principio son iguales
            if py < other.y:
                py = other.y
            elif py > other.y + other.width:
                py = other.y + other.width

            distancia = math.sqrt((self.x - px)**2 + (self.y - py)**2)
            if distancia < self.width:
                return True
            else:
                return False

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



