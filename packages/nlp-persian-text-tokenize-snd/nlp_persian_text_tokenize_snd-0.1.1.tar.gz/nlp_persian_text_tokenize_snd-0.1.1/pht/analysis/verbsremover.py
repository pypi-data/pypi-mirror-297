class VerbsRemover:
    _persian_verbs = (
        'بود', 'داشت', 'برداشت', 'رفت', 'آمد', 'دید', 'گفت', 'شنید', 'خورد', 'نوشت', 'خواند', 'دانست', 'پرید', 'خوابید',
        'ساخت', 'آورد', 'گرفت', 'پخت', 'شست', 'یافت', 'پوشید', 'کشت', 'نشست', 'افتاد', 'پرداخت', 'خندید', 'شست', 'کشید',
        'شناخت', 'کرد', 'شد', 'خرید', 'داد', 'افزود', 'برخاست', 'شود', 'رسید', 'رو', 'خور', 'کن'
    )

    _verb_prefixes = ('می‌', 'نمی‌', 'می', 'نمی')
    _verb_suffixes = {
        'هایش': '',
        'ترین': '',
        'شون': '',
        'ه اند': 'ه‌اند',
        'هایم': '',
        'ه‌ام': '',
        'ه ام': '',
        'ی‌ها': '',
        'ی ها': '',
        'یم': 'یم',
        'ید': 'ید',
        'ند': 'ند',
        'دن': 'دن',
        'ان': '',
        'تر': '',
        'ها': '',
        'ات': '',
        'اش': '',
        'م': '',
        'ی': '',
        'ن': ''
    }

    _connectives_words = (
    'و', 'یا', 'اما', 'زیرا', 'بنابراین', 'اگرچه', 'هرچند', 'چون', 'که', 'برای', 'بر', 'علاوه', 'با',
    'به', 'اگر', 'مگر', 'در', 'حتی', 'چنانچه', 'همچنین')

    def __init__(self, text_content: str):
        self.content = text_content

    @staticmethod
    def past_verbs(_verb: str) -> list:
        return [f'{_verb}م', f'{_verb}ی', f'{_verb}', f'{_verb}یم', f'{_verb}ید', f'{_verb}ند']

    def is_connecting_word(self, word: str) -> bool:
        return word in self._connectives_words

    def get_past_verbs(self) -> tuple:
        data = []
        for verb in self._persian_verbs:
            data += self.past_verbs(verb)

        return tuple(data)

    def is_verb(self, word: str) -> bool:
        return self.get_stemmed(word) in self._persian_verbs

    def get_stemmed(self, word: str, dep: bool = False) -> str:
        new_word = self._get_single_stemmed(word, dep=dep)

        if dep:
            _words = new_word.split("‌")
            if len(_words) > 1:
                for _word in _words:
                    if not self.is_verb(_word):
                        return _word
        return new_word

    def _get_single_stemmed(self, word: str, dep: bool) -> str:
        new_word = word
        prefix = ""
        for pre in self._verb_prefixes:
            if word.startswith(pre) or word.startswith(f'‌{pre}'):
                prefix = pre
                new_word = word[len(pre):]
                break

        _pr = ((prefix + "‌") if not dep else '')
        for ex, replacer in self._verb_suffixes.items():
            if new_word.endswith(ex):
                _len = -len(ex)
                return _pr + (new_word if _len == 0 else (new_word[:_len] + replacer))
            elif new_word.endswith(f"‌{ex}"):
                return _pr + (new_word[:-(len(ex) + 1)]) + replacer

        return new_word if dep else word

    def filter_verbs(self):
        current_words = self.content.split()
        new_words = []

        for current_word in current_words:
            if not self.is_verb(current_word):
                new_words.append(current_word)

        return " ".join(new_words)
