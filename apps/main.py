import uvicorn

if __name__ == "main":
    uvicorn.run("apps.server.app:app", host="0.0.0.0", port=8000, reload=True)