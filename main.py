"""
Main
"""

import uvicorn
from pjecz_centauro_api_key.main import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
