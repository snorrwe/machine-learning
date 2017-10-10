from what_language.tokenizer import tokenize


class Language(object):
    def __init__(self, io, name):
        self.name = name
        self.vectors, self.characters = tokenize(io)
