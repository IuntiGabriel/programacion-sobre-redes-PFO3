# load_balancer.py
import socket
import threading
import itertools

# Lista de backends (nuestros servers workers ojo el puerto)
BACKENDS = [
    ("127.0.0.1", 6001),
    ("127.0.0.1", 6002),
]

LB_HOST = "127.0.0.1"
LB_PORT = 5000

backend_cycle = itertools.cycle(BACKENDS)

def pipe(src, dst):
    """ Copia datos desde src hacia dst mientras haya datos. """
    while True:
        data = src.recv(4096)
        if not data:
            break
        dst.sendall(data)
    src.close()
    dst.close()

def handle_client(client_conn, client_addr):
    # Elegir a cual backend mandar esta conexión
    backend_host, backend_port = next(backend_cycle)
    print(f"[LB] Nueva conexión {client_addr} --> {backend_host}:{backend_port}")

    try:
        backend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_conn.connect((backend_host, backend_port))
    except Exception as e:
        print(f"[LB] ERROR conectando al backend {backend_host}:{backend_port}: {e}")
        client_conn.close()
        return

    # Creamos dos hilos tipo tunel:
    # - uno copia cliente→backend
    # - otro copia backend→cliente
    t1 = threading.Thread(target=pipe, args=(client_conn, backend_conn), daemon=True)
    t2 = threading.Thread(target=pipe, args=(backend_conn, client_conn), daemon=True)
    t1.start()
    t2.start()

def start_lb():
    print(f"[LB] Load balancer escuchando en {LB_HOST}:{LB_PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((LB_HOST, LB_PORT))
    s.listen()

    while True:
        client_conn, client_addr = s.accept()
        threading.Thread(target=handle_client, args=(client_conn, client_addr), daemon=True).start()

if __name__ == "__main__":
    start_lb()
