import subprocess
import markdown2
import re
from dataclasses import dataclass
from typing import Iterable

NOTES_DIRECTORY = '/Users/tanyatik/cheatnotes/'
SEARCH_CONTEXT_LINES_BEFORE = 2
SEARCH_CONTEXT_LINES_AFTER = 10
HIGHLIGHT_BACKGROUND_COLOR = '#FFFF00'


@dataclass
class SearchResult:
    filename: str
    markdown: bytes


@dataclass
class FormattedSearchResult:
    filename: str
    html: str


def format_search_result(search_result: SearchResult) -> FormattedSearchResult:
    return FormattedSearchResult(filename=search_result.filename, html=markdown2.markdown(search_result.markdown))


def grep_search_results_iterator(search_process_stdout) -> Iterable[SearchResult]:
    """
    Parses the result of grep search and returns an iterator over SearchResult
    """
    # Parse the result
    # It can look similar to this:

    # /Users/tanyatik/cheatnotes//test_note_1.md-# Paragraph three
    # /Users/tanyatik/cheatnotes//test_note_1.md-
    # /Users/tanyatik/cheatnotes//test_note_1.md:Thee paragrath three recursion
    # /Users/tanyatik/cheatnotes//subdir/subdir2/test_note_4.md:This is test note with even more recursion
    # /Users/tanyatik/cheatnotes//subdir/subdir2/test_note_4.md-
    # --
    # --
    # /Users/tanyatik/cheatnotes//subdir/test_note_3.md:This is test recursive note to test recursion
    # /Users/tanyatik/cheatnotes//subdir/test_note_3.md-
    # /Users/tanyatik/cheatnotes//subdir/test_note_3.md-more text

    # Lines with -- in them need to be skipped

    previous_filename = None
    previous_text = b''
    for line in search_process_stdout.split(b'\n'):
        if not line or not line.strip():
            continue
        if line == b'--':
            continue

        regex = rb'^([a-zA-Z0-9/._]+)[-:]'
        text = re.sub(regex, b'', line, flags=re.MULTILINE)
        filename = re.search(regex, line, flags=re.MULTILINE).group(1)

        # Results corresponding to the same filename as previous result are added to the previous result
        if filename == previous_filename or previous_filename is None:
            previous_text += b'\n' + text
        else:
            yield SearchResult(filename=previous_filename.decode(), markdown=previous_text)
            previous_text = text

        previous_filename = filename

    yield SearchResult(filename=previous_filename.decode(), markdown=previous_text)
    return


def search_notes(query) -> Iterable[FormattedSearchResult]:
    """
    Search notes saved in a local filesystem and return result formatted in HTML.
    Search term
    """
    grep_command = ['grep', '-i', '-I', '-r', '-A', str(SEARCH_CONTEXT_LINES_AFTER), '-B',
                    str(SEARCH_CONTEXT_LINES_BEFORE), query, NOTES_DIRECTORY]
    grep_process = subprocess.run(grep_command, capture_output=True)
    search_result = grep_process.stdout

    for search_result in grep_search_results_iterator(search_result):
        if not search_result:
            return

        formatted_search_result = format_search_result(search_result)

        # Highlight query in the resulting text (modifying the HTML)
        query_found = re.search(query, formatted_search_result.html, flags=re.IGNORECASE | re.MULTILINE)
        html = formatted_search_result.html[:query_found.start()] + \
               f'<span style="background-color: {HIGHLIGHT_BACKGROUND_COLOR}">' + \
               formatted_search_result.html[query_found.start():query_found.end()] + \
               '</span>' + \
               formatted_search_result.html[query_found.end():]

        yield FormattedSearchResult(filename=search_result.filename, html=html)
