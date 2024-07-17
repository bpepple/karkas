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
    def _remove_word_series(txt: str) -> str:
        """
        Summary:
        Removes word series from the input text.

        Explanation:
        This static method takes a string as input, splits it into words, and returns the first word.
        It is used to the word 'Series'.

        Args:
            txt (str): The input text from which the word series will be removed.

        Returns:
            str: The first word from the input text.
        """
        return txt.partition(" ")[0] if txt else txt

    def _update_metadata(self: Runner, comic_list: list[Path]) -> int:
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

            if series_format_lower in old_formats_set:
                md.series.format = "Single Issue"
            elif "series" in series_format_lower:
                if fixed_format := self._remove_word_series(md.series.format):
                    md.series.format = fixed_format
                else:
                    continue
            else:
                continue

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
