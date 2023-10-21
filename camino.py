class Camino:
    def __init__(self, puntos):
        self.puntos = puntos  # Lista de puntos que definen el camino

    def dibujar(self, screen, color=(0, 255, 0), grosor=2):
        # Dibuja el camino en la pantalla
        for i in range(1, len(self.puntos)):
            punto_actual = (int(self.puntos[i - 1].x), int(self.puntos[i - 1].y))
            punto_siguiente = (int(self.puntos[i].x), int(self.puntos[i].y))
            pygame.draw.line(screen, color, punto_actual, punto_siguiente, grosor)
