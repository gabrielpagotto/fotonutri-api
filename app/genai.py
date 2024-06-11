import google.generativeai as genai
from app.config import config


def configure_genai():
    genai.configure(api_key=config.genapi_key)
