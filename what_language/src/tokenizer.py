from collections import defaultdict
from fractions import Fraction

PUNCTUATION = list(u'~@#$%^&*()_+\'[]“”‘’—<>»«›‹–„/')
SPACES = list(u' \u00A0\n')
STOP_CHARACTERS = list('.?!')


def normalize(distribution):
    sum_values = sum(distribution.values())
    return {key: Fraction(value, sum_values) for key, value in distribution.items()}


def tokenize(io):
    vectors = []
    dist = defaultdict(int)
    characters = set()

    for char in io.read():
        if char in STOP_CHARACTERS:
            if dist:
                vectors.append(normalize(dist))
                dist = defaultdict(int)
        elif char not in SPACES and char not in PUNCTUATION:
            character = char.lower()
            characters.add(character)
            dist[character] += 1
    if dist:
        vectors.append(normalize(dist))
    return vectors, characters
