from fastapi import FastAPI

app = FastAPI(title="modus-mini")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check."""
    return {"status": "ok"}
