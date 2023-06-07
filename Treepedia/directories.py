from pathlib import Path


# Define directories
REPO_ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT_DIR / "data"
SPATIAL_DATA = DATA_DIR / "spatial_data"

# Make directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
SPATIAL_DATA.mkdir(parents=True, exist_ok=True)
