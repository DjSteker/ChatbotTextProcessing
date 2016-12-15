from nltk.corpus import words as nltk_words
from nltk.corpus import wordnet as wn


class WordsAnalyzer:
    @staticmethod
    def get_base_word(lemmatizer, word):
        return lemmatizer.lemmatize(word)

    @staticmethod
    def is_word_valid(word):
        try:
            dictionary = dict.fromkeys(nltk_words.words(), None)
            x = dictionary[word]
            return True
        except KeyError:
            return False

    @staticmethod
    def get_synonyms_of_word_and_definitions(non_proper_word):
        synonyms = set()
        definitions = []
        for synset in wn.synsets(non_proper_word):
            # for item in synset.lemma_names:
            definitions.append(synset.definition())
            lemmas = synset.lemmas()
            for l in lemmas:
                synonyms.add(l.name())
        # print (synonyms, definitions)
        return synonyms, definitions

    @staticmethod
    def is_punctuation(punctuation):
        if punctuation in ['.', ',', '?', '!', '...']:
            return True
        return False
