from xml.etree.ElementTree import Element, SubElement, tostring
from nltk.tokenize import *
from ChatbotTextProcessing.TextProcessing.api.postProcessing.answers import AnswerType, RandomAnswerGenerator
from nltk.stem import WordNetLemmatizer
from profanity import profanity
from ChatbotTextProcessing.TextProcessing.api.nltk.wordsanalyzer import WordsAnalyzer
import nltk
import wikipedia


class AnswerSchema:
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.unknown_words = []
        self.proper_names = []
        self.aggressive_vocabulary_filter = False

    def build_sentence_xml(self):
        random_answer_generator = RandomAnswerGenerator()

        root = Element('sentence')
        child_raw_answer = SubElement(root, 'raw')
        child_annotated_answer = SubElement(root, 'annotated')

        if self.raw_input is None or len(self.raw_input) < 1:
            raw_sentence = random_answer_generator.get_answer(AnswerType.empty_sentence)
            child_raw_answer.text = raw_sentence
            child_annotated_answer.text = raw_sentence
            return root
        elif self.aggressive_vocabulary_filter:
            raw_sentence = random_answer_generator.get_answer(AnswerType.vocabulary_aggressive_sentence)
            child_raw_answer.text = raw_sentence
            child_annotated_answer.text = raw_sentence
            return root
        elif self.unknown_words is not None and len(self.unknown_words) > 0:
            generated_answer = random_answer_generator.get_answer(AnswerType.unknown_word_sentence)
            raw_sentence = generated_answer + self.unknown_words[0]
            child_raw_answer.text = raw_sentence
            child_annotated_answer.text = generated_answer
            self.build_annotated_sentence(child_annotated_answer, raw_sentence, unknown_words=True)
        else:
            raw_sentence = self.raw_input
            child_raw_answer.text = raw_sentence
            child_annotated_answer.text = self.build_annotated_sentence(child_annotated_answer, raw_sentence,
                                                                        proper_names=True)

        return root

    def build_annotated_sentence(self, root, raw_sentence, proper_names=False, unknown_words=False):
        if unknown_words:
            child_unknown_word = SubElement(root, 'raw-bot-output')
            child_unknown_word.text = self.unknown_words[0]
            return raw_sentence

        if proper_names:
            words = nltk.pos_tag(word_tokenize(self.raw_input))
            for word in words:
                if word[0] in self.proper_names:
                    wiki = wikipedia.page(word[0])
                    child_proper_name = SubElement(root, 'link')
                    child_proper_name.set('ref', wiki.url)
                    child_proper_name.text = word[0]

            annotated_sentence = ""
            for word in words:
                annotated_sentence += word[0] + " "

            return annotated_sentence

        return ""


class SentenceProcessor:
    @staticmethod
    def process_sentence(sentence):
        answer_schema = AnswerSchema(sentence)

        wordnet_lemmatizer = WordNetLemmatizer()

        words = nltk.pos_tag(word_tokenize(sentence))

        if sentence is None or len(sentence) < 1:
            xml_response = answer_schema.build_sentence_xml()
            print(tostring(xml_response))

        # now we check the errors and correct them if possible --- Lucian's module

        # now we check for aggressive vocabulary
        if profanity.contains_profanity(sentence):
            answer_schema.aggressive_vocabulary_filter = True

        # now we check for incorrect words and proper names
        for word in words:
            if word[1] in ['NNP', 'NNPS']:
                answer_schema.proper_names.append(word[0])
                continue

            try:
                word_base_form = wordnet_lemmatizer.lemmatize(word=word[0], pos=word[1][0]).lower()
            except:
                word_base_form = wordnet_lemmatizer.lemmatize(word=word[0]).lower()

            if not WordsAnalyzer.is_word_valid(word_base_form):
                answer_schema.unknown_words.append("\"" + word_base_form + "\"")

        xml_response = answer_schema.build_sentence_xml()
        print(tostring(xml_response))

SentenceProcessor.process_sentence('I am not smart')
