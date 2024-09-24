from .SentencesTokenizer import SentencesTokenizer
from .WordsTokenizer import WordsTokenizer


class TokenizerManager(SentencesTokenizer, WordsTokenizer):

    def tokenizing(self):
        sentences = self.break_sentences()
        sentences_words = []

        for sentence in sentences:
            sentences_words.append(self.tokenizing_sentence(sentence))

        return sentences_words
