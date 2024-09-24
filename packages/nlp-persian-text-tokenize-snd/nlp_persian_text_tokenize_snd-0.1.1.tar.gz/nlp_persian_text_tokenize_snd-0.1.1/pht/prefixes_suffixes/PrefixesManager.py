class PrefixesManager:
    _prefixes = ('بی', 'می', 'نمی', 'بر')

    def __init__(self, content: str):
        self.content = content

    def fixing(self):
        self._fixing_negative_prefixes_spaces()
        return self.content

    def _fixing_negative_prefixes_spaces(self):
        for _prefix in self._prefixes:
            self.content = self.content.replace(f' {_prefix} ', f' {_prefix}‌')
