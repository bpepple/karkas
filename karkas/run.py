from __future__ import annotations

from pathlib import Path

from darkseid.comic import Comic
from darkseid.utils import get_recursive_filelist
from tqdm import tqdm


class Runner:
    """
    Runner class for updating metadata of comics.

    Args:
        path: Path to the comic or folder of comics.

    Returns:
        None
    """

    def __init__(self: Runner, path: Path) -> None:
        self._path = path

    @staticmethod
    def _update_metadata(comic_list: list[Path]) -> int:
        """
        Update metadata of comics in the provided list.

        Args:
            comic_list: List of paths to comics.

        Returns:
            int: The number of comics whose metadata was successfully updated.
        """
        change_count = 0
        old_formats_set = {"cancelled series", "ongoing series"}

        for item in tqdm(comic_list):
            comic = Comic(item)
            if not comic.seems_to_be_a_comic_archive() or not comic.has_metadata():
                continue

            md = comic.read_metadata()
            series_format_lower = md.series.format.lower()

            if any(fmt in series_format_lower for fmt in old_formats_set):
                md.series.format = "Single Issue"
                if comic.write_metadata(md):
                    change_count += 1

        return change_count

    def run(self: Runner) -> None:
        """
        Execute the process of updating metadata for comics.

        Returns:
            None
        """
        comic_list = get_recursive_filelist([self._path])
        result_count = self._update_metadata(comic_list)
        print(f"Updated {result_count} comics.")
