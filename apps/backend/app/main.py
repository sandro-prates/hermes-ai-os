from fastapi import FastAPI

app = FastAPI(
    title="Hermes AI OS",
    description="Plataforma profissional para agentes de IA.",
    version="0.0.1",
)


@app.get("/")
async def root():
    return {
        "project": "Hermes AI OS",
        "status": "running",
        "version": "0.0.1",
        "phase": "Foundation",
    }