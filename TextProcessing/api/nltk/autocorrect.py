import enchant
from wordfreq import word_frequency


class AutoCorrect:
    wordDict = None

    @staticmethod
    def initDict():
        if AutoCorrect.wordDict is None:
            AutoCorrect.wordDict = enchant.Dict('en_US')

    @staticmethod
    def suggest(sentence):
        AutoCorrect.initDict()
        words = sentence.split()
        suggestions = []
        foundError = False
        for word in words:
            if AutoCorrect.wordDict.check(word) == False:
                foundError = True
                try:
                    corrections = AutoCorrect.wordDict.suggest(word)
                    corrections = sorted(zip(corrections, [word_frequency(w, 'en') for w in corrections]), key=lambda x:x[1], reverse=True)
                    suggestions.append(corrections[0][0])
                except IndexError:
                    raise SuggestionNotFoundException
            else:
                suggestions.append(word)
       
        return ' '.join(suggestions)


class SuggestionNotFoundException(Exception):
    pass
