from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Olá Mundo do Backend SportsBet +EV AI!"}

@app.get("/api/health")
async def health_check():
    return {"status": "Backend saudável e operante!"}
