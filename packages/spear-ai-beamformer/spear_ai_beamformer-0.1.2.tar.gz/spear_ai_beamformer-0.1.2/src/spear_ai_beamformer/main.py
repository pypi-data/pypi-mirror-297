"""A conventional beamformer CLI."""

import pytest

from spear_ai_beamformer import library


def main() -> None:
    """Entry point python execution function."""
    print(library.add(1, 2))  # noqa: T201


def test_main(capsys: pytest.CaptureFixture) -> None:
    """Test entry point python execution function."""
    main()
    captured = capsys.readouterr()
    assert captured.out == "3\n"


if __name__ == "__main__":
    main()  # pragma: no cover
