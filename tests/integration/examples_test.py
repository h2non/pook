import platform
import subprocess
from pathlib import Path
import sys
import re

import pytest

examples_dir = Path(__file__).parents[2] / "examples"

examples = list(examples_dir.glob("*.py"))


if platform.python_implementation() == "PyPy":
    # See pyproject.toml note on mocket dependency
    examples.remove(examples_dir / "mocket_example.py")


HTTPBIN_WITH_SCHEMA_REF = re.compile("https?://httpbin.org")


@pytest.mark.parametrize(
    "example", (pytest.param(example, id=example.name) for example in examples)
)
def test_examples(example: Path, local_responder):
    code = example.read_text()
    with_local_responder = HTTPBIN_WITH_SCHEMA_REF.sub(
        local_responder.url, code
    ).replace("httpbin.org", local_responder.host)
    assert "httpbin" not in with_local_responder
    result = subprocess.run([sys.executable, "-c", with_local_responder], check=False)

    assert result.returncode == 0, result.stdout
