#!/usr/env/python3

from urllib import request
import os


def download_to_file(url, directory='./data', filename='download.txt'):
    web_response = request.urlopen(url)
    web_content = web_response.read().decode('utf-8')

    if not os.path.isdir(directory):
        os.mkdir(directory)
    full_filename = os.path.join(directory, filename)

    with open(full_filename, mode='w', encoding='utf-8') as f:
        f.write(web_content)
    print('Downloaded and saved the content of {} to {}'.format(url, full_filename))
    return f

federalist_file = download_to_file('https://www.gutenberg.org/cache/epub/1404/pg1404.txt', filename='federalist.txt')


import time

import spacy
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.tokens.span import Span

print('Load the English language models.')
nlp = spacy.load('en')


def make_doc(in_file_path) -> Doc:
    with open(in_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        now = time.time()
        doc = nlp(text)
        print('Det tog {} sekunder'.format(time.time() - now))
        print('Teksten indeholder {} ord'.format(len(list(doc))))

        return doc


doc = make_doc(federalist_file.name)


from collections import Counter
from typing import List, Tuple
keywords = Counter()

# On probability: The lower the value, the less likely is the word to occur ≈ the more
# significant is its occurence. (gleaned from
# https://github.com/explosion/spaCy/commit/ff9ff6f3fa1fe15191233796e669028a31936dee)

def most_significant_words(doc: Doc, count: int = 35,
                           probability: int = -8) -> List[Tuple[str, int]]:
    for chunk in doc:
        # probablity value -8 is arbitrarily selected threshold
        if nlp.vocab[chunk.lemma_].prob < probability:
            keywords[chunk.lemma_] += 1

    return keywords.most_common(count)


def most_significant_verbs(doc: Doc, count: int = 35,
                           probability: int = -8) -> List[Tuple[str, int]]:
    for token in doc:
        if token.pos_ == 'VERB' and nlp.vocab[token.lemma_].prob < probability:
            keywords[token.lemma_] += 1

    return keywords.most_common(count)


def most_significant_noun_phrases(doc: Doc, count: int = 35,
                                  probability: int = -8) -> List[Tuple[str, int]]:
    for chunk in doc.noun_chunks:
        if nlp.vocab[chunk.lemma_].prob < probability:
            keywords[chunk.lemma_] += 1

    return keywords.most_common(count)

