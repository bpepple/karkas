import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from karkas.run import Runner


@pytest.mark.parametrize(
    "comic_files, update_return, expected_output",
    [
        (["comic1.cbz", "comic2.cbz"], 2, "Updated 2 comics."),  # happy path
        ([], 0, "Updated 0 comics."),  # edge case: no comics
        (["comic1.cbz"], 1, "Updated 1 comics."),  # single comic
    ],
    ids=[
        "multiple_comics",
        "no_comics",
        "single_comic",
    ],
)
def test_run_happy_path(comic_files, update_return, expected_output, capsys):
    # Arrange
    runner = Runner(Path("/some/path"))
    runner._update_metadata = MagicMock(return_value=update_return)

    with patch("darkseid.utils.get_recursive_filelist", return_value=comic_files):
        # Act
        runner.run()

        # Assert
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_output


@pytest.mark.parametrize(
    "comic_files, update_return, expected_output",
    [
        (
            ["comic1.cbz", "comic2.cbz"],
            2,
            "Updated 2 comics.",
        ),  # edge case: multiple comics
        ([], 0, "Updated 0 comics."),  # edge case: no comics
    ],
    ids=[
        "multiple_comics",
        "no_comics",
    ],
)
def test_run_edge_cases(comic_files, update_return, expected_output, capsys):
    # Arrange
    runner = Runner(Path("/some/path"))
    runner._path = "/some/path"
    runner._update_metadata = MagicMock(return_value=update_return)

    with patch("darkseid.utils.get_recursive_filelist", return_value=comic_files):
        # Act
        runner.run()

        # Assert
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_output


@pytest.mark.parametrize(
    "exception, expected_output",
    [
        (Exception("Error"), "Error"),  # error case: exception raised
    ],
    ids=[
        "exception_raised",
    ],
)
def test_run_error_cases(exception, expected_output, capsys):
    # Arrange
    runner = Runner(Path("/some/path"))
    runner._update_metadata = MagicMock(side_effect=exception)

    with patch("darkseid.utils.get_recursive_filelist", return_value=["comic1.cbz"]):
        # Act
        with pytest.raises(Exception) as excinfo:
            runner.run()

        # Assert
        assert str(excinfo.value) == expected_output
