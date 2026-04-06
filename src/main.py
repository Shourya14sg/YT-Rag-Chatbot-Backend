from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from router import router_yt
#from api.endpoints import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",response_class=HTMLResponse)
def read_root():
    return """<html>
            <body style="background-color: #f0f0f0; font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>Welcome to YT Rag</h1>
            <a href="/docs">Open SwaggerUI</a>
            </body>
        </html>"""
app.include_router(router_yt,prefix="/yt",tags=["Fetch Video Transcript"])
#app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)