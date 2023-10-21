import pygame as pg
NEGRO=(0,0,0)
BLANCO=(255,255,255)
AMARILLO=(255,255,0)
ROSA=(255,0,255)
AZUL=(0,255,255)

screen=pg.display.set_mode(size=(500,500))
clock=pg.time.Clock()
run=True
rect=pg.Rect(200,100,50,90) #2 primeros posicion, largo y ancho

while run:
    screen.fill(BLANCO) #rellenamos la pantalla de blanco
    pg.draw.rect(screen,AZUL,rect)
    pg.draw.circle(screen, AMARILLO, (122, 258), 20, 0)
    pg.display.update()

    for event in pg.event.get():
        if event.type==pg.QUIT:
            run=False

pg.quit()
