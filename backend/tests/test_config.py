import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config


def test_load_environment_reads_dotenv_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=test-key\n", encoding="utf-8")

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    config.load_environment(env_file)

    assert os.environ["OPENAI_API_KEY"] == "test-key"
