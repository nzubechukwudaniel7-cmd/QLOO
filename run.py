import uvicorn

if __name__ == "__main__":
    print("[*] Starting NeuroTaste Backend Server on http://localhost:8000 (0.0.0.0:8000)...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
