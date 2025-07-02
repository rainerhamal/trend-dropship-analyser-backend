from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analysis import router as analysis_router
from fastapi.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

# Prevent 404 logs for Chrome DevTools probing
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def devtools_probe():
    return Response(status_code=204)