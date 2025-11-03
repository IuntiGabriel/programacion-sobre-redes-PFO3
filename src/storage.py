# storage.py
import time

def save_to_postgres(task_id, payload, result):
    """
    En producción esto sería un INSERT en una base Postgres distribuida.
    Acá solo mostramos la intención.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[POSTGRES] {timestamp} | task_id={task_id} payload={payload} result={result}")

def save_to_s3(task_id, result):
    """
    En producción esto subiría un archivo/objeto a S3 u otro storage tipo objeto.
    Acá lo simulamos con un print.
    """
    preview = result[:60].replace("\n", " ")
    print(f"[S3] Guardando resultado de task {task_id}: {preview} ...")
