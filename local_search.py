import subprocess
import markdown2
import re
from dataclasses import dataclass
from typing import Iterable


NOTES_DIRECTORY = '/Users/tanyatik/Notes/'
SEARCH_CONTEXT_LINES_BEFORE = 2
SEARCH_CONTEXT_LINES_AFTER = 10
HIGHLIGHT_BACKGROUND_COLOR = '#FFFF00'


@dataclass
class SearchResult:
    filename: bytes
    html: bytes


def search_notes(query) -> Iterable[SearchResult]:
    """
    Search notes saved in a local filesystem and return result formatted in HTML.
    Search term
    """
    grep_command = ['grep', '-i', '-r', '-A', str(SEARCH_CONTEXT_LINES_AFTER), '-B', str(SEARCH_CONTEXT_LINES_BEFORE), query, NOTES_DIRECTORY]
    grep_process = subprocess.run(grep_command, capture_output=True)
    search_result = grep_process.stdout

    # Parse the result
    # It can look similar to this:

    # users/Tanya/notes/bash.md-
    # users/Tanya/notes/bash.md-
    # users/Tanya/notes/bash.md:IF statements
    # users/Tanya/notes/bash.md-
    # users/Tanya/notes/bash.md-* \[ symlink\_to\_file\_a -ef file\_a \] returns True
    # users/Tanya/notes/bash.md-
    entries = search_result.split(b'--\n--')

    for entry in entries:
        if not entry:
            return

        # Expecting each line to start with a filename + 1 more symbol
        regex = rb'^([a-zA-Z0-9/._]+)[-:]'
        cleaned_text = re.sub(regex, b'', entry, flags=re.MULTILINE)
        filename = re.search(regex, entry, flags=re.MULTILINE).group(1)
        html = markdown2.markdown(cleaned_text)

        # Highlight query in the resulting text (modifying the HTML)
        query_found = re.search(query, html, flags=re.IGNORECASE | re.MULTILINE)
        html = html[:query_found.start()] + f'<span style="background-color: {HIGHLIGHT_BACKGROUND_COLOR}">' + html[query_found.start():query_found.end()] + '</span>' + html[query_found.end():]

        yield SearchResult(filename=filename, html=html)
