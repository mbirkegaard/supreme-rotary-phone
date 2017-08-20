import spacy

from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.tokens.span import Span
import time

raw_text_file = './data/aristot.pol_eng.txt'
pickled_doc_path = './data/aristot.pol.pickle'

nlp = spacy.load('en')
print('LOADED THE SHIT')


def make_doc(in_file_path) -> Doc:
    with open(in_file_path, 'r', encoding='utf-8') as file:
        text = file.readline()
        now = time.time()
        doc = nlp(text)
        print('Det tog {} sekunder'.format(time.time() - now))
        print('Teksten indeholder {} ord'.format(len(list(doc))))

        return doc

doc = make_doc(raw_text_file)

from typing import List, Union


def concordance(tokens_or_spans: List[Union[Token, Span]], context_length=5):
    cnd_list = []
    for token_or_span in tokens_or_spans:
        if isinstance(token_or_span, Token):
            start = max(token_or_span.i - context_length, 0)
            end = min(token_or_span.i + context_length + 1, len(token_or_span.doc))
        else:
            start = max(token_or_span.start - context_length, 0)
            end = min(token_or_span.end + context_length + 1, len(token_or_span.doc))

        cnd_list.append((token_or_span, token_or_span.doc[start:end]))

    for t, context in cnd_list:
        print('++++++++++++++++++++++++++++++')
        print('{}'.format(format_token_or_span(t)))
        print(context)

    return cnd_list


def find_tokens(doc, lemma_, pos_=None):
    return [token for token in doc
            if token.lemma_ == lemma_ and (pos_ is None or token.pos_ == pos_)]


def find_entities(doc, ent_label_=None):
    lst = []
    for span in doc.ents:
        if ent_label_ is None or span.label_ == ent_label_:
            if span.end - span.start == 1:
                lst.append(doc[span.start])
            else:
                lst.append(span)

    return lst


def count_entity_labels(doc):
    from collections import Counter
    return Counter([ent.label_ for ent in doc.ents])




def format_span(span: Span):
    return '{}, ENT_LABEL: {}'.format(span, span.label_)


def format_token(token: Token):
    return '{}, lemma: {}, POS: {}, ENT_TYPE: {}'.format(token.orth_,
                                                                     token.lemma_,
                                                                     token.pos_,
                                                                     token.ent_type_,
                                                                     )
def format_token_or_span(token_or_span):
    if isinstance(token_or_span, Token):
        return format_token(token_or_span)
    else:
        return format_span(token_or_span)

things = find_entities(doc, ent_label_='GPE')
cnd_list = concordance(things)


# for entry in count_entity_labels(doc).most_common():
#     print(entry)



