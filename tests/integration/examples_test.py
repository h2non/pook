import platform
import subprocess
from pathlib import Path
import sys

import pytest

examples_dir = Path(__file__).parents[2] / "examples"

examples = [f.name for f in examples_dir.glob("*.py")]


if platform.python_implementation() == "PyPy":
    # See pyproject.toml note on mocket dependency
    examples.remove("mocket_example.py")


@pytest.mark.parametrize("example", examples)
def test_examples(example):
    result = subprocess.run([sys.executable, f"examples/{example}"], check=False)

    assert result.returncode == 0, result.stdout
