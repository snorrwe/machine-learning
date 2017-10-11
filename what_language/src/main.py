from what_language.src.network import Network
from what_language.tests.test_cross_validation import load_glob


def main():
    matthew_languages = load_glob('../data/*_0.txt')
    acts_languages = load_glob('../data/*_1.txt')
    languages = matthew_languages + acts_languages
    network = Network(languages)
    network.train()
    while 1:
        sentence = input("Gimme a sentence, bitch")
        result = network.predict(sentence)
        print('\n%s\n' % result)


if __name__ == '__main__':
    main()
