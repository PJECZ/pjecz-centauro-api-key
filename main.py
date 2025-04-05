"""
Arrancar pjecz_centauro_api_key.main:app
"""

import os
import sys

MAIN_APP_SERVER = os.environ.get("MAIN_APP_SERVER", "")   # En Dockerfile esta definido como gunicorn

try:
    from pjecz_centauro_api_key.main import app
except ImportError:
    sys.stderr.write("Error: No se encontró la instancia 'app' en pjecz_centauro_api_key.main")


if __name__ == "__main__":
    if MAIN_APP_SERVER == "uvicorn":
        # Run the FastAPI app with uvicorn for local development
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
        sys.exit(0)
    elif MAIN_APP_SERVER == "gunicorn":
        # Run the FastAPI app with gunicorn server ASGI for production
        port = int(os.environ.get("PORT", 8080))
        worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "uvicorn.workers.UvicornWorker")
        workers = int(os.environ.get("GUNICORN_WORKERS", 1))
        cmd = f"gunicorn pjecz_centauro_api_key.main:app -b 0.0.0.0:{port} -w {workers} -k {worker_class} -t 0"
        os.system(cmd)
        sys.exit(0)
    else:
        # If the server is not recognized, print an error message
        sys.stderr.write(f"Error: El servidor '{MAIN_APP_SERVER}' no es reconocido. Declare MAIN_APP_SERVER con 'uvicorn' o 'gunicorn'\n")
        sys.exit(1)
