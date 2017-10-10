import unittest
from io import StringIO
import string
from what_language.language import Language

LANGUAGE_DATA = u'''
abcdefghijklmnopqrstuvwxyz.
ABCDEFGHIJKLMNOPQRSTUVWXYZ.
\u00A0.
!~@#$%^&*()_+'?[]“”‘’—<>»«›‹–„/.
ïëéüòèöÄÖßÜøæåÅØóąłżŻśęńŚćźŁ.
'''


class LanguageTests(unittest.TestCase):

    def setUp(self):
        self.special_characters = LANGUAGE_DATA.split('\n')
        self.language_io = StringIO(LANGUAGE_DATA)
        self.language = Language(self.language_io, 'English')

    def test_values(self):
        """Sum of values in a vector equals one"""
        for vecor in self.language.vectors:
            self.assertEqual(1, sum(vecor.values()))

    def test_character_set(self):
        """returns characters that is a unique set of characters used"""
        chars = list(string.ascii_lowercase) + list(set(u'ïëéüòèöäößüøæååóąłżżśęńśćź'))
        self.assertListEqual(sorted(chars),
                             sorted(self.language.characters))


if __name__ == '__main__':
    unittest.main()
