from pathlib import Path


# Define directories
REPO_ROOT_DIR = Path(__file__).parent
APP_DIR = REPO_ROOT_DIR / "app"
DATA_DIR = REPO_ROOT_DIR / "data"


# Make directories
DATA_DIR.mkdir(parents=True, exist_ok=True)