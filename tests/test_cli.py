import pytest
from unittest.mock import patch, MagicMock
from karkas.cli import main


@pytest.mark.parametrize(
    "args_path, expected_runner_path",
    [
        ("/valid/path1", "/valid/path1"),
        ("/valid/path2", "/valid/path2"),
        ("/valid/path3", "/valid/path3"),
    ],
    ids=["valid_path1", "valid_path2", "valid_path3"],
)
def test_main_happy_path(args_path, expected_runner_path):
    # Arrange
    mock_args = MagicMock()
    mock_args.path = args_path

    # Act
    with patch("karkas.cli.get_args", return_value=mock_args):
        with patch("karkas.cli.Runner") as MockRunner:
            main()

            # Assert
            MockRunner.assert_called_once_with(expected_runner_path)
            MockRunner.return_value.run.assert_called_once()


@pytest.mark.parametrize(
    "args_path",
    [
        "/edge/case/path1",
        "/edge/case/path2",
    ],
    ids=["edge_case_path1", "edge_case_path2"],
)
def test_main_edge_cases(args_path):
    # Arrange
    mock_args = MagicMock()
    mock_args.path = args_path

    # Act
    with patch("karkas.cli.get_args", return_value=mock_args):
        with patch("karkas.cli.Runner") as MockRunner:
            main()

            # Assert
            MockRunner.assert_called_once_with(args_path)
            MockRunner.return_value.run.assert_called_once()
