from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from app.routes import chat, order, recommend, faq

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include different routes under /api prefix
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(order.router, prefix="/api/order", tags=["Order"])
app.include_router(recommend.router, prefix="/api/recommend", tags=["Recommendation"])
app.include_router(faq.router, prefix="/api/faq", tags=["FAQ"])

# API root endpoint
@app.get("/api")
def api_root():
    return {"message": "E-commerce Chatbot API is running!"}

# Serve React frontend in production
frontend_build_path = Path("../frontend/dist")

# Check if the build directory exists
if frontend_build_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_build_path / "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(request: Request, full_path: str):
        # Serve the index.html for any path that doesn't start with /api
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")

        # Check if the requested file exists
        requested_file = frontend_build_path / full_path
        if requested_file.exists() and requested_file.is_file():
            return FileResponse(str(requested_file))

        # Default to index.html for client-side routing
        return FileResponse(str(frontend_build_path / "index.html"))
else:
    # Development mode or frontend not built yet
    @app.get("/")
    def root():
        return {"message": "E-commerce Chatbot API is running! Frontend not built yet."}
