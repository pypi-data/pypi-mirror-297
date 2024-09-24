from typing import List
from date_normalization.datenormalization import DateNormalization
from ..prefixes_suffixes.PrefixesManager import PrefixesManager
from ..prefixes_suffixes.SuffixesManager import SuffixesManager
from ..analysis.verbsremover import VerbsRemover
import re


class SentencesTokenizer:
    _farsi_characters = (
        'ا', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'ژ',
        'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 'م',
        'ن', 'و', 'ه', 'ی'
    )

    def __init__(self, content):
        self.content = content
        self.verbs_manager = VerbsRemover(self.content)

    def break_sentences(self):
        self.content = (self.content.strip()
                        .replace('\n', '.')
                        .replace('؟', '?').replace('؛', ';'))
        self.content = (DateNormalization()).normalization_text(self.content)
        self._check_unhandled_sentences()
        self._extract_hide_sentences()
        self.content = self._check_sentences(self.content)

        self._fixing_prefixes()
        self._fixing_suffixes()
        self.content = re.sub(r'\s+', ' ', self.content).strip()
        sentences = re.split(r'([.!?;])\s*', self.content)
        sentences = [item for item in sentences if item]
        sentences = self._checkout_hide_sentences(sentences)

        return sentences

    def _is_hide_sentences(self, text: str) -> bool:
        if not text.endswith('.'):
            text = re.sub(r'[^\w\s]', '', text)
            words = text.split()
            if len(words) <= 2 or not self.verbs_manager.is_verb(words[len(words) - 1]):
                return False
        return True

    def _extract_hide_sentences(self):
        matches = re.findall(r'\(([^)]+)\)', self.content)
        if len(matches):
            counter = 0
            for match in matches:
                if self._is_hide_sentences(match):
                    counter += 1
                    key = f'HH_{counter}_HH'
                    self.content = self.content.replace(f'({match})', key)
                    founded_items = list(re.finditer(rf'\b{key}\b', self.content))
                    if len(founded_items):
                        match_replacer = re.search(r'[.!?;]', self.content[founded_items[0].end():])
                        if match_replacer:
                            dot_position = match_replacer.start() + founded_items[0].end()
                            self.content = self.content[:dot_position + 1] + match + self.content[dot_position + 1:]
                            self.content = self.content.replace(key, '')

    @staticmethod
    def _checkout_hide_sentences(sentences: List[str]) -> list:
        sentences_len = len(sentences)
        best_sentences = []
        for position in range(sentences_len):
            sentence = sentences[position]
            if sentence not in ['.', '!', '?', ';', '', '\n']:
                _symbol = ''
                if position + 1 <= sentences_len - 1:
                    _s = sentences[position + 1]
                    if _s in ['.', '!', '?', ';']:
                        _symbol = sentences[position + 1]
                best_sentences.append(sentence + _symbol)
        return best_sentences

    def _check_sentences(self, sentence: str) -> str:
        if sentence.startswith('.'):
            return self._check_sentences(sentence[1:])
        else:
            _sens = list(re.finditer(r'\b[.]\b', sentence))
            if len(_sens):
                _sen = _sens[0]
                check_before = sentence[_sen.start() - 1] in self._farsi_characters
                check_after = sentence[_sen.start() + 1] in self._farsi_characters
                if check_before or check_after:
                    return self._check_sentences(sentence[:_sen.start()] + ". " + sentence[_sen.end():])
        return sentence

    def _check_unhandled_sentences(self):
        verbs = self.verbs_manager.get_past_verbs()
        for verb in verbs:
            matches = list(re.finditer(rf'\s{verb}\s', self.content))
            for match in matches:
                search_content = self.content[match.end():]
                match_replacer = re.search(r'\s', search_content)
                if match_replacer:
                    next_word = search_content[:match_replacer.end()].strip()
                    if not self.verbs_manager.is_connecting_word(next_word):
                        self.content = self.content[:match.end() - 1] + '.' + self.content[match.end() - 1:]
                else:
                    self.content = self.content[:match.end() - 1] + '.' + self.content[match.end() - 1:]

    def _fixing_prefixes(self):
        self.content = PrefixesManager(self.content).fixing()

    def _fixing_suffixes(self):
        self.content = SuffixesManager(self.content).fixing()
