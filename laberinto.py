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