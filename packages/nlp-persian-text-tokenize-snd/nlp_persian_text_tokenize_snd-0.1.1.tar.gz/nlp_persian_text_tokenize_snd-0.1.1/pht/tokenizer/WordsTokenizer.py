from typing import List
import re


class WordsTokenizer:

    def tokenizing_sentence(self, sentence: str) -> List[str]:
        normal_words = self._first_breaking_level(sentence)

        return normal_words

    @staticmethod
    def _clear_word(part: str) -> List[str]:
        words = []
        current_word = ""
        if re.match(r'[^\w\u200c]+', part):
            if current_word:
                words.append(current_word)
                current_word = ""

            if part.strip():
                words.append(part.strip())
        else:
            current_word += part

        if current_word:
            words.append(current_word)
        return words

    def _first_breaking_level(self, sentence: str) -> List[str]:
        normal_words = sentence.split(" ")
        words = []

        for normal_word in normal_words:
            split_words = re.split(r'([^\w\u200c]+)', normal_word)
            _current_words = []
            for split_word in split_words:
                _current_words += self._clear_word(split_word)
            words += _current_words

        return words
