
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STREAMLIT_ROOT = PROJECT_ROOT / "streamlit"

sys.path.insert(0, str(STREAMLIT_ROOT))