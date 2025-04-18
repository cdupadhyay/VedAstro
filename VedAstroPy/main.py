
from fastapi import FastAPI
from api.endpoints import app

app = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
