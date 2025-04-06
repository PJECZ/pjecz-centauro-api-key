"""
Launch FastAPI server with Uvicorn
"""

import os
import uvicorn

from pjecz_centauro_api_key.main import app


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
