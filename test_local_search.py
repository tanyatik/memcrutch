import unittest
from local_search import grep_search_results_iterator, SearchResult


class TestLocalSearch(unittest.TestCase):
    def test_grep_search_results_iterator(self):
        test_grep_stdout = b"""
/Users/tanyatik/cheatnotes//test_note_1.md-# Paragraph three
/Users/tanyatik/cheatnotes//test_note_1.md-
/Users/tanyatik/cheatnotes//test_note_1.md:Thee paragrath three recursion
/Users/tanyatik/cheatnotes//subdir/subdir2/test_note_4.md:This is test note with even more recursion
/Users/tanyatik/cheatnotes//subdir/subdir2/test_note_4.md-
--
--
/Users/tanyatik/cheatnotes//subdir/test_note_3.md-LALALA
/Users/tanyatik/cheatnotes//subdir/test_note_3.md:This is test recursive note to test recursion
/Users/tanyatik/cheatnotes//subdir/test_note_3.md-
/Users/tanyatik/cheatnotes//subdir/test_note_3.md-LALALA"""

        search_results = list(grep_search_results_iterator(test_grep_stdout))

        self.assertEqual(search_results[0], SearchResult(filename='/Users/tanyatik/cheatnotes//test_note_1.md', markdown=b'\n# Paragraph three\n\nThee paragrath three recursion'))
        self.assertEqual(search_results[1], SearchResult(filename='/Users/tanyatik/cheatnotes//subdir/subdir2/test_note_4.md', markdown=b'This is test note with even more recursion\n'))
        self.assertEqual(search_results[2], SearchResult(filename='/Users/tanyatik/cheatnotes//subdir/test_note_3.md', markdown=b'LALALA\nThis is test recursive note to test recursion\n\nLALALA'))
