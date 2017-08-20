import glob
from spacy.tokens.doc import Doc
from typing import NamedTuple, Optional, Dict
import spacy
import time


class StoredDocument(NamedTuple):
    name: str
    path: str
    doc: Optional[Doc]


class DocumentManager:

    def __init__(self):
        self.nlp = None
        self.documents: Dict[str, StoredDocument] = {}

        for path in glob.glob('data/*.txt'):
            name = path.split('/')[-1]

            self.documents[name] = StoredDocument(
                name,
                path,
                None
            )

    def get_document_names(self):
        return [doc.name for doc in self.documents.values()]

    def get_document(self, name):
        if name not in self.documents:
            raise KeyError('{} is not the name of a stored document'.format(name))

        if self.documents[name].doc is None:
            document = self.documents[name]
            processed_doc = self.load_file_and_process_doc(document.path)

            self.documents[name] = StoredDocument(
                document.name,
                document.path,
                processed_doc
            )

        return self.documents[name].doc

    def load_file_and_process_doc(self, path):

        with open(path, 'r', encoding='utf-8') as file:
            if self.nlp is None:
                print('Loading spacy')
                self.nlp = spacy.load('en')
                print('Loaded spacy')

            text = file.readline()
            now = time.time()
            doc = self.nlp(text)
            print('Det tog {} sekunder'.format(time.time() - now))
            print('Teksten indeholder {} ord'.format(doc.__len__()))
            return doc
