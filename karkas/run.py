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
        self._fails: list[str] = []

    def _update_metadata(self: Runner, comic_list: list[Path]) -> int:
        """
        Updates metadata for comics in the given list based on specific conditions.

        Args:
            comic_list: A list of Path objects representing the comics to update metadata for.

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

            if series_format_lower in old_formats_set:
                md.series.format = "Single Issue"
            elif "annual" in series_format_lower:
                md.series.format = "Annual"
            elif "hard cover" in series_format_lower:
                md.series.format = "Hardcover"
            else:
                continue

            if comic.write_metadata(md):
                change_count += 1
            else:
                self._fails.append(str(comic.path))

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
        if self._fails:
            print(f"Failed to write changes to the following {len(self._fails)} comics.")
            for fail in self._fails:
                print(fail)
