import graphene
from document_manager import DocumentManager
# from spacy.tokens import doc
# from spacy.tokens import span
# from spacy.tokens import token


class Token(graphene.ObjectType):
    orth = graphene.String()

    @graphene.resolve_only_args
    def resolve_orth(self):
        return self.orth_


class Span(graphene.ObjectType):
    def __init__(self):
        graphene.ObjectType.__init__(self)

    text = graphene.String()

    @graphene.resolve_only_args
    def resolve_text(self):
        return self.text

    span = graphene.Field(
        lambda: Span,
        start=graphene.Int(),
        end=graphene.Int()
    )

    @graphene.resolve_only_args
    def resolve_span(self, start=None, end=None):
        if start is None and end is None:
            raise ValueError('Start and end may not both be {}'.format(start))

        if start is None and end is not None:
            return self[:end]

        if start is not None and end is None:
            return self[start:]

        return self[start:end]


class Document(graphene.ObjectType):
    def __init__(self):
        graphene.ObjectType.__init__(self)

    token = graphene.Field(
        Token,
        i=graphene.NonNull(graphene.Int)
    )

    @graphene.resolve_only_args
    def resolve_token(self, i):
        return self[i]

    span = graphene.Field(
        Span,
        start=graphene.Int(),
        end=graphene.Int()
    )

    @graphene.resolve_only_args
    def resolve_span(self, start=None, end=None):
        if start is None and end is None:
            return self[:]

        if start is None and end is not None:
            return self[:end]

        if start is not None and end is None:
            return self[start:]

        return self[start:end]


def make_schema(document_manager: DocumentManager):
    class Query(graphene.ObjectType):
        hello = graphene.String(description='A typical hello world')

        def resolve_hello(self, args, context, info):
            return 'World'

        document = graphene.Field(
            Document,
            name=graphene.NonNull(graphene.String)
        )

        @graphene.resolve_only_args
        def resolve_document(self, name):
            return document_manager.get_document(name)

        valid_document_names = graphene.List(graphene.String)

        @graphene.resolve_only_args
        def resolve_valid_document_names(self):
            return document_manager.get_document_names()

    return graphene.Schema(query=Query, auto_camelcase=False)
