from xml.etree.ElementTree import Element, SubElement, tostring
from wordsanalyzer import *
from nltk.tokenize import *
import nltk
import re
from nltk.sem.drt import *
from nltk import load_parser
from nltk.stem import WordNetLemmatizer
from autocorrect import *

class SentenceTreeBuilder:
    parser = load_parser('./././././drt.fcfg', logic_parser=nltk.sem.drt.DrtParser())
    @staticmethod
    def build_text_xml(text):
        """
        Usage example: print(tostring(SentenceTreeBuilder.build_text_xml("Alex is a student.")))
        """
        root = Element('annotated-string')
        sentences = sent_tokenize(text)
        list_anaphora = []
        for i in range(len(sentences)):
            sentences[i] = AutoCorrect.suggest(sentences[i])
        print(sentences)
        for sent in sentences:
            words = word_tokenize(sent)
            words = [x for x in words if  WordsAnalyzer.is_punctuation(x) == 0]
            list_anaphora.append(words)
        drs_list = []
        try:
            for sentence in list_anaphora:
                trees = list(__class__.parser.parse(sentence))
                if len(trees) > 0:
                    drs_list.append(trees[0].label()['SEM'].simplify())
            drs_sum = ""
            read_dexpr = nltk.sem.DrtExpression.fromstring
            for drs in drs_list:
                drs_expr = read_dexpr(str(drs))
                drs_sum += str(drs_expr) + " + "
            drs_sum = drs_sum[:-3]
            drs_sum = read_dexpr(drs_sum)
            #print(drs_sum.simplify())
            anaphora_rezolved = drs_sum.simplify().resolve_anaphora()
            anaphora_rezolved = str(anaphora_rezolved)
            index_after_var_list = anaphora_rezolved.find('],[')

            content = anaphora_rezolved[index_after_var_list+3:-2]
            list_variables_mapped_to_words = content.split(', ')
            #print(list_variables_mapped_to_words)
            pattern = "\(*(\w+)\((\w+)\)*( = \(\w+ = (\[\w+(,\w+)*\])\))?\)*"
            list_tuple_word_var_variable_can_be_replaced_with = []
            for elem in list_variables_mapped_to_words:
                matcher = re.match(pattern, elem)
                print(matcher)
                if matcher == None:
                    continue
                group_for_pronoun_only = None
                if matcher.group(4) is not None:
                    group_for_pronoun_only = matcher.group(4)
                list_tuple_word_var_variable_can_be_replaced_with.append((matcher.group(1), matcher.group(2),group_for_pronoun_only))
        except Exception:
            list_tuple_word_var_variable_can_be_replaced_with = []

        for actual_sentence in sentences:
            chile = SubElement(root, 'sentence')
            __class__._build_sentence_xml(actual_sentence, chile,list_tuple_word_var_variable_can_be_replaced_with)
        return root

    @staticmethod
    def _build_sentence_xml(actual_sentence, xmlSentence, list_tuple_word_var_variable_can_be_replaced_with):
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
            if len(list_tuple_word_var_variable_can_be_replaced_with)>0 and list_tuple_word_var_variable_can_be_replaced_with[0][0] == word[0]:
                child.set('anaphora_var', list_tuple_word_var_variable_can_be_replaced_with[0][1])
                if list_tuple_word_var_variable_can_be_replaced_with[0][2] != None:
                    child.set('anaphora_can_replace', list_tuple_word_var_variable_can_be_replaced_with[0][2]) 
                del list_tuple_word_var_variable_can_be_replaced_with[0]
            child.set('part-of-speech', word[1])
            if words[1] in ['NNP', 'NNPS'] or WordsAnalyzer.is_punctuation(word[1]):
                continue

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
    print(tostring(element=SentenceTreeBuilder.build_text_xml("Joe owns a dog. He marries Joe. It barks."), encoding="unicode"))