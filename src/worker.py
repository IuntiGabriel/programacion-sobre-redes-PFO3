# worker.py
import threading
import queue
import time
import uuid
from storage import save_to_postgres, save_to_s3

class WorkerNode:
    def __init__(self, name, num_threads=4):
        self.name = name
        self.task_queue = queue.Queue()
        self.num_threads = num_threads
        self._start_threads()

    def _start_threads(self):
        for i in range(self.num_threads):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            print(f"[{self.name}] Hilo worker {i} iniciado")

    def _worker_loop(self):
        while True:
            task_id, payload = self.task_queue.get()
            try:
                print(f"[{self.name}] Procesando tarea {task_id} payload={payload}")

                # Simulacion de carga de trabajo
                time.sleep(2)

                # Resultado final de la tarea
                result = payload.upper()  # ejemplo pasar a mayusculas

                # Seguimos
                save_to_postgres(task_id, payload, result)
                save_to_s3(task_id, result)

                print(f"[{self.name}] Tarea {task_id} completada.")
            except Exception as e:
                print(f"[{self.name}] ERROR procesando {task_id}: {e}")
            finally:
                self.task_queue.task_done()

    def enqueue_task(self, payload):
        """
        Recibe una payload un string eque envia el cliente),
        genera un task_id y lo encola para ser procesado por algun hilo interno.
        Devuelve el task_id para que el server se lo mande al cliente.
        """
        task_id = str(uuid.uuid4())
        self.task_queue.put((task_id, payload))
        print(f"[{self.name}] Tarea {task_id} en cola")
        return task_id
