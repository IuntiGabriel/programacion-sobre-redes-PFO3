# client.py
import socket

LB_HOST = "127.0.0.1"
LB_PORT = 5000

def main():
    print("[CLIENT] Conectando al balanceador...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((LB_HOST, LB_PORT))

    try:
        while True:
            msg = input("Ingrese tarea (o 'exit' para salir): ").strip()
            s.sendall((msg + "\n").encode())

            data = s.recv(1024)
            if not data:
                print("[CLIENT] Conexión cerrada por el servidor")
                break

            print("[CLIENT] Respuesta:", data.decode().strip())

            if msg.lower() == "exit":
                break
    finally:
        s.close()

if __name__ == "__main__":
    main()
