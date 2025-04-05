"""
Launch FastAPI
"""

import os
import sys

try:
    from pjecz_centauro_api_key.main import app
except ImportError:
    sys.stderr.write("Error: Not found instance 'app' in pjecz_centauro_api_key.main")


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn for local development
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    sys.exit(0)
# else:
    # Run the FastAPI app with gunicorn server ASGI for production
    # port = int(os.environ.get("PORT", 8080))
    # worker_class = os.environ.get("WORKER_CLASS", "uvicorn.workers.UvicornWorker")
    # workers = int(os.environ.get("GUNICORN_WORKERS", 1))
    # cmd = f"gunicorn --bind 0.0.0.0:{port} --workers {workers} --threads 8 --timeout 0 -k {worker_class} pjecz_centauro_api_key.main:app"
    # os.system(cmd)
    # sys.exit(0)
