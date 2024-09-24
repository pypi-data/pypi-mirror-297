from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nlp_persian_text_tokenize_snd',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'nlp_date_normalization_snd',
    ],
    author='Nasser Khaledi',
    author_email='foray00227@gmail.com',
    description='This library is designed to tokenize Persian texts.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/7cloner/NLP-Persian-Text-Tokenize-SND',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
