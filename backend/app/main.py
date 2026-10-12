from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="modus-mini")
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}
