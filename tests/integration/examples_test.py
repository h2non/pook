import sys
import subprocess
import pytest
from pathlib import Path
import platform


examples_dir = Path(__file__).parents[2] / "examples"

examples = [f.name for f in examples_dir.glob("*.py")]

if sys.version_info >= (3, 11) or platform.python_implementation() == "PyPy":
    # See pyproject.toml note on mocket dependency
    examples.remove("mocket_example.py")


if sys.version_info >= (3, 12):
    # See pyproject.toml note on aiohttp dependency
    examples.remove("aiohttp_client.py")
    examples.remove("decorator_activate_async.py")


@pytest.mark.parametrize("example", examples)
def test_examples(example):
    result = subprocess.run(["python", "examples/{}".format(example)])

    assert 0 == result.returncode, result.stdout
