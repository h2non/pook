from pathlib import Path

BINARY_FILE_PATH = Path(__file__).parent / "nothing.bin"
BINARY_FILE = BINARY_FILE_PATH.read_bytes()
