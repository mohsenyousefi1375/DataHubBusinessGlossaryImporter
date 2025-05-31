from dotenv import load_dotenv
import os

load_dotenv()



gms_server = os.getenv("gms_server","http://localhost:8080")
API_HOST: str = os.getenv("API_HOST", "localhost")
API_PORT: int = int(os.getenv("API_PORT", 8000))
API_RELOAD: bool = bool(os.getenv("API_RELOAD", True))