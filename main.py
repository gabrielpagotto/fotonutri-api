from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handler import router
from app.genai import configure_genai
from app.firebase import initialize_firebase

configure_genai()
initialize_firebase()

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
