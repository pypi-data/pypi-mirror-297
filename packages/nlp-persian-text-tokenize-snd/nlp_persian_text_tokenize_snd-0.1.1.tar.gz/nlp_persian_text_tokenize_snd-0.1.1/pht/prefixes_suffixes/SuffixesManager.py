class SuffixesManager:
    _suffixes = ('زاده', '‌تر')

    def __init__(self, content: str):
        self.content = content

    def fixing(self):
        self._fixing_suffixes_content_spaces()
        return self.content

    def _fixing_suffixes_content_spaces(self):
        for _suffix in self._suffixes:
            self.content = (self.content.replace(f' {_suffix} ', f'{_suffix} ')
                            .replace(f'‌{_suffix} ', f'{_suffix} '))
