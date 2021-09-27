import subprocess
import markdown2
from dataclasses import dataclass
from typing import Iterable


NOTES_DIRECTORY = '/Users/tanyatik/Notes/'


@dataclass
class SearchResult:
    filename: bytes
    html: bytes


def search_notes(text) -> Iterable[SearchResult]:
    print(f'about to search notes for text {text}')

    grep_process = subprocess.run(['grep', '-i', '-r', text, NOTES_DIRECTORY], capture_output=True)
    search_result = grep_process.stdout
    # Parse the result?
    entries = search_result.split(b'\n')
    for entry in entries:
        if not entry:
            return
        filename_and_text = entry.split(b':')
        html = markdown2.markdown(filename_and_text[1])

        yield SearchResult(filename=filename_and_text[0], html=html)


