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


testdata = [
    # Happy path tests
    (
        ["/path/to/comic1.cbz", "/path/to/comic2.cbz"],
        True,
        True,
        MagicMock(series=MagicMock(format="Ongoing Series")),
        True,
        1,
    ),
    (
        ["/path/to/comic1.cbz", "/path/to/comic2.cbz"],
        True,
        True,
        MagicMock(series=MagicMock(format="Cancelled Series")),
        True,
        1,
    ),
    (
        ["/path/to/comic1.cbz", "/path/to/comic2.cbz"],
        True,
        True,
        MagicMock(series=MagicMock(format="Single Issue")),
        False,
        0,
    ),
    # Edge cases
    ([], True, True, MagicMock(series=MagicMock(format="Ongoing Series")), True, 0),
    (
        ["/path/to/comic1.cbz"],
        False,
        True,
        MagicMock(series=MagicMock(format="Ongoing Series")),
        True,
        0,
    ),
    (
        ["/path/to/comic1.cbz"],
        True,
        False,
        MagicMock(series=MagicMock(format="Ongoing Series")),
        True,
        0,
    ),
    # Error cases
    (
        ["/path/to/comic1.cbz"],
        True,
        True,
        MagicMock(series=MagicMock(format="Ongoing Series")),
        False,
        0,
    ),
]


@pytest.mark.parametrize(
    "comic_list,seems_to_be_a_comic_archive,has_metadata,read_metadata,write_metadata,expected_count",
    testdata,
    ids=[
        "happy_path_single_update",
        "happy_path_single_update_cancelled",
        "happy_path_no_update_needed",
        "empty_list",
        "not_a_comic_archive",
        "no_metadata",
        "write_metadata_failure",
    ],
)
def test_update_metadata(
    comic_list,
    seems_to_be_a_comic_archive,
    has_metadata,
    read_metadata,
    write_metadata,
    expected_count,
):
    comic_list = [Path(p) for p in comic_list]

    # Arrange
    with patch("karkas.run.Comic") as MockComic:
        mock_comic_instance = MockComic.return_value
        mock_comic_instance.seems_to_be_a_comic_archive.return_value = (
            seems_to_be_a_comic_archive
        )
        mock_comic_instance.has_metadata.return_value = has_metadata
        mock_comic_instance.read_metadata.return_value = read_metadata
        mock_comic_instance.write_metadata.return_value = write_metadata

        # Act
        run = Runner(Path("/tmp"))
        result = run._update_metadata(comic_list)

        # Assert
        assert result == expected_count
