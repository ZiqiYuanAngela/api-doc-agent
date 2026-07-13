from fastapi import FastAPI

from app.api.questions import router as questions_router
from app.api.specifications import router as specifications_router
from app.api.validation import router as validation_router

app = FastAPI(title="API Documentation Agent", version="1.0.0")
app.include_router(specifications_router)
app.include_router(questions_router)
app.include_router(validation_router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}
