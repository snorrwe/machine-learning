import codecs
import os
from glob import glob
from io import StringIO
from what_language.src.network import Network
from what_language.src.language import Language

HERE = os.path.dirname(os.path.realpath(__file__))


def get_language_name(file_name):
    basename, ext = os.path.splitext(os.path.basename(file_name))
    return basename.split('_')[0]


def load_glob(pattern):
    result = []
    for fname in glob(pattern):
        result.append(Language(codecs.open(fname, encoding='utf-8'),
                               get_language_name(fname)))
    return result


def main():
    matthew_languages = load_glob('%s/../data/*_0.txt' % HERE)
    acts_languages = load_glob('%s/../data/*_1.txt' % HERE)
    languages = matthew_languages + acts_languages
    assert languages, "Languages can't be empty!"
    network = Network(languages)
    network.train()
    while 1:
        sentence = input("Gimme a sentence, bitch")
        io = StringIO(sentence)
        result = network.predict(io)
        print('\n%s\n' % result.name)


if __name__ == '__main__':
    main()
