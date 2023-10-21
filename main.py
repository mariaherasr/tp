import logging
if __name__ == '__main__':
logging.basicConfig(filename='mylog.log', # Fichero donde se guardar´an los registros.
filemode='w',
level=logging.DEBUG, # Se registrar´a todo.
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
6
escena1(...)
escena2(...)
escena3(...)
...

