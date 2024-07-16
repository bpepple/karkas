import pytest
from pathlib import Path
from karkas.options import make_parser


@pytest.mark.parametrize(
    ("input_path", "expected_path"),
    [
        ("/path/to/comic", Path("/path/to/comic")),
        ("/path/to/folder", Path("/path/to/folder")),
    ],
    ids=["single_comic", "folder_of_comics"],
)
def test_make_parser_happy_path(input_path, expected_path):
    # Act
    parser = make_parser()
    args = parser.parse_args([input_path])

    # Assert
    assert args.path == expected_path


def test_make_parser_version_flag():
    # Act
    parser = make_parser()

    # Assert
    with pytest.raises(SystemExit) as excinfo:
        parser.parse_args(["--version"])
    assert excinfo.value.code == 0
