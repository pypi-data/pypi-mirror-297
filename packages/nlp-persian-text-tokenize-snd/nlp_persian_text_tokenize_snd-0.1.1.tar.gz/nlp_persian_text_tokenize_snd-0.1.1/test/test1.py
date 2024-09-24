from pht.tokenizer.TokenizerManager import TokenizerManager

article_content = ""
with open('article.txt', 'r', encoding='utf-8') as file:
    article_content += file.read()

sen = TokenizerManager(article_content)
print(sen.tokenizing())