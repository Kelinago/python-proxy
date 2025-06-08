import re

from typing import Optional


DEFAULT_MARKER_LIST = ['👍', '🔥']

class WordLengthMarkerHandler:
    """
    Marks words of a specific length in a text with an element from specified list.
    """

    def __init__(self, word_length: int = 7, markers: Optional[list[str]] = None):
        self._next_index = 0
        self.markers = markers if markers else DEFAULT_MARKER_LIST
        self.regex = re.compile(fr'(?P<word>\b\w{{{word_length}}}\b)')

    def handle(self, text: str) -> str:
        return self.regex.sub(
            lambda match: self._mark_word(match.group('word')),
            text
        )

    def __call__(self, text: str) -> str:
        return self.handle(text)

    def _mark_word(self, word: str) -> str:
        return f'{word}{self._get_next_marker()}'

    def _get_next_marker(self) -> str:
        marker = self.markers[self._next_index]
        self._next_index = (self._next_index + 1) % len(self.markers)
        return marker
