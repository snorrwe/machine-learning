from io import StringIO
import codecs
from glob import glob
import os
import re
import unittest
from parameterized import parameterized
from what_language.src.language import Language
from what_language.src.network import Network


def get_language_name(file_name):
    basename, ext = os.path.splitext(os.path.basename(file_name))
    return basename.split('_')[0]


def load_glob(pattern):
    result = []
    for fname in glob(pattern):
        result.append(Language(codecs.open(fname, encoding='utf-8'),
                               get_language_name(fname)))
    return result


class TestNetwork(unittest.TestCase):

    matthew_languages = load_glob('../data/*_0.txt')
    acts_languages = load_glob('../data/*_1.txt')
    matthew_verses = Network(matthew_languages)
    matthew_verses.train()
    acts_verses = Network(acts_languages)
    acts_verses.train()

    languages = 'English Finnish German Norwegian Polish Swedish'.split()

    @parameterized.expand(languages)
    def test_accuracy(self, lang):
        """Trains and cross-validates with an error of 5%"""
        print('Test for %s' % lang)
        self.compare(self.matthew_verses, '../data/%s_1.txt' % lang)
        self.compare(self.acts_verses, '../data/%s_0.txt' % lang)

    def compare(self, network, file_name):
        misses = 0.0
        hits = 0.0
        with codecs.open(file_name, encoding='utf-8') as f:
            text = f.read()
        for sentence in re.split(r'[\.!\?]', text):
            language = network.predict(StringIO(sentence))
            if language is None:
                continue
            if language.name == get_language_name(file_name):
                hits += 1
            else:
                misses += 1
        total = misses + hits
        self.assertGreater(total, 0)
        self.assertLess(misses,
                        0.05 * total,
                        msg='%s has failed with a miss rate of %f' % (file_name,
                                                                      misses / total))


if __name__ == '__main__':
    unittest.main()
