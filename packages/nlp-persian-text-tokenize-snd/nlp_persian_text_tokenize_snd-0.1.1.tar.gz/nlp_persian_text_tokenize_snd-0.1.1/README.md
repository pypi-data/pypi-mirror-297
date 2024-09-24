# کتابخانه Tokenize برای زبان فارسی

این کتابخانه بخشی از پروژه NLP است که با استفاده از آن میتوان یک متن فارسی را به جملات خاص تقسیم و جملات را به کلمات تقسیم کرد..

## نصب

برای نصب این کتابخانه کافیه از دستور زیر استفاده کنید: 

```bash
pip install nlp-persian-text-tokenize-snd==0.1.1
```

## نحوه پیاده‌سازی

برای استفاده از کتابخانه، می‌توانید از کد نمونه زیر استفاده کنید:

```python
# -*- coding: utf-8 -*-
from pht.tokenizer.TokenizerManager import TokenizerManager

content = 'این یک متن تست فارسی است. آیا درست کار میکند؟ بیاید ببینیم!'
sen = TokenizerManager(content)
print(sen.tokenizing())
```