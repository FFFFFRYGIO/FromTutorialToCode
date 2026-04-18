import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).with_name("notion.env")
load_dotenv(dotenv_path=env_path)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
