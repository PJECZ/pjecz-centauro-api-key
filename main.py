"""
Main
"""

import os


try:
    from pjecz_centauro_api_key.main import app
except ImportError:
    import sys
    sys.exit("Error: Could not find 'app' instance in pjecz_centauro_api_key.main")

if __name__ == "__main__":
    # This block is ONLY executed when you run 'python main.py' directly
    import uvicorn
    # Listen on all interfaces
    host = "0.0.0.0"
    # Google Cloud Run sets the PORT environment variable
    try:
        port = int(os.getenv("PORT", 8080))
    except ValueError:
        port = 8080
    # Run the Uvicorn server programmatically
    uvicorn.run(app, host=host, port=port)
