from fastapi import FastAPI
from apps.server.routes.student import router as StudentRouter

app = FastAPI()

@app.get("/", tags=["Root"])
async def read_root():
    return { "message": "hello world!"}


app.include_router(StudentRouter, tags=["Student"], prefix="/student")