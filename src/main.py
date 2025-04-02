import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True,
    )