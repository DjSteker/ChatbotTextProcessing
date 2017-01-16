from enum import Enum
import random


class RandomAnswerGenerator:
    def __init__(self):
        self.answers_by_type = {}
        self.initialize_answers_map()

    def initialize_answers_map(self):
        self.answers_by_type = {}
        empty_string_answers = ["I don't know what to say"]
        unknown_words_answer = ["My guts tell me that the answer to that is"]
        aggressive_vocabulary_answers = ["I will not answer to that"]

        self.answers_by_type["empty_sentence"] = empty_string_answers
        self.answers_by_type["unknown_word_sentence"] = unknown_words_answer
        self.answers_by_type["vocabulary_aggressive_sentence"] = aggressive_vocabulary_answers

    def get_answer(self, answer_type):
        if answer_type is None:
            return "N.A."

        if self.answers_by_type[answer_type.name] is not None and len(self.answers_by_type[answer_type.name]) > 0:
            answers_list = self.answers_by_type[answer_type.name]
            rand_ind = random.randint(0, len(answers_list) - 1)
            return answers_list[rand_ind]

        return "N.A."


class AnswerType(Enum):
    empty_sentence = 1
    vocabulary_aggressive_sentence = 2
    unknown_word_sentence = 3
