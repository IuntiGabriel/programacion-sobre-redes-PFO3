# server2.py
import socket
import threading
from worker import WorkerNode

HOST = "127.0.0.1"   # IP privada del worker en este caso LOCALHOST
PORT = 6002          # Distinto puerto por worker si se corren varios

worker_node = WorkerNode(name="worker-2", num_threads=4)

def handle_client(conn, addr):
    print(f"[SERVER] Conexión desde {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            payload = data.decode().strip()
            print(f"[SERVER] Recibido payload='{payload}' de {addr}")

            if payload.lower() == "exit":
                conn.sendall(b"bye\n")
                break

            # Enviamos la tarea al pool de hilos a traves del worker node
            task_id = worker_node.enqueue_task(payload)

            # Devolvemos un ACK inmediato
            response = f"OK task_id={task_id}\n"
            conn.sendall(response.encode())

    print(f"[SERVER] Conexión cerrada {addr}")

def start_server():
    print(f"[SERVER] Iniciando servidor en {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    start_server()
