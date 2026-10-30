import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure .env is loaded reliably regardless of execution working directory
root_dir = Path(__file__).resolve().parent.parent
dotenv_path = root_dir / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

class Settings(BaseModel):
    qloo_api_key: str = os.getenv("QLOO_API_KEY", "")
    qloo_base_url: str = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com")
    app_name: str = "NeuroTaste API - Qloo-Powered Autonomous Reminiscence Care"
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()
