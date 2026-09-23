# conftest.py (at project root)
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # ← Prevents __pycache__ entirely

sys.path.insert(0, str(Path(__file__).parent / "src"))
