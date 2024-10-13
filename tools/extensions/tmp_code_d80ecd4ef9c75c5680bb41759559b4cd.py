
import unittest

def occurance_substring(main_string, sub_string):
    positions = []
    start = 0
    while True:
        start = main_string.find(sub_string, start)
        if start == -1:
            break
        positions.append(start)
        start += len(sub_string)
    
    if not positions:
        return None
    
    return (sub_string, positions[0], len(positions))

class TestOccuranceSubstring(unittest.TestCase):
    def test_multiple_occurrences(self):
        self.assertEqual(occurance_substring(' programming,  language', ''), ('', 0, 2))
    
    def test_single_occurrence(self):
        self.assertEqual(occurance_substring('hello world', 'world'), ('world', 6, 1))
    
    def test_no_occurrence(self):
        self.assertIsNone(occurance_substring('hello world', ''))
    
    def test_empty_main_string(self):
        self.assertIsNone(occurance_substring('', ''))
    
    def test_empty_sub_string(self):
        self.assertEqual(occurance_substring('hello world', ''), ('', 0, 12))  # Every position is a match
    
    def test_sub_string_longer_than_main_string(self):
        self.assertIsNone(occurance_substring('short', 'longerstring'))
    
    def test_sub_string_at_end(self):
        self.assertEqual(occurance_substring('hello world', 'world'), ('world', 6, 1))
    
    def test_sub_string_at_start(self):
        self.assertEqual(occurance_substring('hello world', 'hello'), ('hello', 0, 1))
    
    def test_sub_string_with_special_characters(self):
        self.assertEqual(occurance_substring('hello!@#world', '!@#'), ('!@#', 5, 1))
    
    def test_sub_string_with_spaces(self):
        self.assertEqual(occurance_substring('hello world hello', 'hello'), ('hello', 0, 2))

if __name__ == '__main__':
    unittest.main()
