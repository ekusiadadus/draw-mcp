"""Tests for CLI entry point."""

import json
from pathlib import Path

import pytest

from drawio_validator.cli import main


@pytest.fixture
def valid_drawio_file(tmp_path: Path) -> Path:
    content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="P" id="d1">
    <mxGraphModel dx="1200" dy="800" page="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="a" value="Test" style="rounded=1;fontFamily=Noto Sans JP;fontSize=18;"
          vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    f = tmp_path / "valid.drawio"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def invalid_drawio_file(tmp_path: Path) -> Path:
    content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron">
  <diagram name="P" id="d1">
    <mxGraphModel dx="1200" dy="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="a" value="Text" style="fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    f = tmp_path / "invalid.drawio"
    f.write_text(content, encoding="utf-8")
    return f


class TestCli:
    def test_valid_file_returns_zero(self, valid_drawio_file: Path) -> None:
        exit_code = main([str(valid_drawio_file)])
        assert exit_code == 0

    def test_invalid_file_returns_one(self, invalid_drawio_file: Path) -> None:
        exit_code = main([str(invalid_drawio_file)])
        assert exit_code == 1

    def test_json_output(self, valid_drawio_file: Path, capsys: pytest.CaptureFixture) -> None:
        main([str(valid_drawio_file), "--format", "json"])
        output = capsys.readouterr().out
        data = json.loads(output)
        assert "findings" in data
        assert "summary" in data

    def test_nonexistent_file(self, tmp_path: Path) -> None:
        exit_code = main([str(tmp_path / "nonexistent.drawio")])
        assert exit_code == 1
