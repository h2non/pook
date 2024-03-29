import sys
import subprocess
import pytest
from pathlib import Path
import platform


examples_dir = Path(__file__).parents[2] / "examples"

examples = [f.name for f in examples_dir.glob("*.py")]


if platform.python_implementation() == "PyPy":
    # See pyproject.toml note on mocket dependency
    examples.remove("mocket_example.py")


@pytest.mark.parametrize("example", examples)
def test_examples(example):
    result = subprocess.run(["python", "examples/{}".format(example)])

    assert 0 == result.returncode, result.stdout
