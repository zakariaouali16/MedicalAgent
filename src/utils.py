import os
from dotenv import load_dotenv
#
def load_secrets():
    """Loads API keys from .env file"""
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    if not project_id:
        raise ValueError("Project ID not found in .env")
    return project_id