from xml.etree.ElementTree import Element, SubElement, tostring

import nltk
from nltk.tokenize import *

from api.nltk.wordsanalyzer import WordsAnalyzer
from nltk.stem import WordNetLemmatizer


class SentenceTreeBuilder:
    @staticmethod
    def build_text_xml(text):
        """
        Usage example: print(tostring(SentenceTreeBuilder.build_text_xml("Alex is a student.")))
        """
        root = Element('annotated-string')
        sentences = sent_tokenize(text)
        for actual_sentence in sentences:
            chile = SubElement(root, 'sentence')
            __class__._build_sentence_xml(actual_sentence, chile)
        return root

    @staticmethod
    def _build_sentence_xml(actual_sentence, xmlSentence):
        wordnet_lemmatizer = WordNetLemmatizer()
        words = nltk.pos_tag(word_tokenize(actual_sentence))

        for word in words:
            try:
                wordBaseForm = wordnet_lemmatizer.lemmatize(word=word[0], pos=word[1][0]).lower()
            except:
                wordBaseForm = wordnet_lemmatizer.lemmatize(word=word[0]).lower()

            child = SubElement(xmlSentence, 'word')
            child.text = word[0]
            child.set('partOfSpeech', word[1])
            child.set('baseForm', wordBaseForm)

            if words[1] in ['NNP', 'NNPS'] or WordsAnalyzer.is_punctuation(word[1]):
                continue
            if not WordsAnalyzer.is_word_valid(wordBaseForm):
                raise InvalidWordException("Invalid word:{w}".format(w=word))

            synonyms, definitions = WordsAnalyzer.get_synonyms_of_word_and_definitions(wordBaseForm)

            synonymNumber = 1
            for synonym in synonyms:
                child.set("s" + str(synonymNumber), synonym)
                synonymNumber += 1

            definitionNumber = 1
            for definition in definitions:
                child.set("d" + str(definitionNumber), definition)
                definitionNumber += 1


class InvalidWordException(Exception):
    pass

if __name__ == "__main__":
    #print(WordNetLemmatizer().lemmatize("She has apples"))
    print(tostring(element=SentenceTreeBuilder.build_text_xml("I am your chief"), encoding="unicode"))