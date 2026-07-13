from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.questions import router as questions_router
from app.api.specifications import router as specifications_router
from app.api.validation import router as validation_router

app = FastAPI(title="API Documentation Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(specifications_router)
app.include_router(questions_router)
app.include_router(validation_router)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}
