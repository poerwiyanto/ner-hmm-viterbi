"""
    File name: ner_parser.py
    Author: Poerwiyanto.
    Date created: 4/26/2019
    Date last modified: 4/26/2019
    Python version: 3.7.1
"""
from html.parser import HTMLParser
import re


class NERParser(HTMLParser):
    def __init__(self):
        # Invoke the __init__ of HTMLParser class.
        HTMLParser.__init__(self)

        # Initialize entities, tag, and tokens.
        self.entities = []
        self.tag = None
        self.tokens = []

    def get_result(self):
        """Reset and return entities and tokens."""
        entities = self.entities
        self.entities = []

        tokens = self.tokens
        self.tokens = []

        return (entities, tokens)

    def handle_data(self, data):
        if self.tag:
            entity = self.tag
            tokens = data.split()
        else:
            # Tag untagged tokens as other.
            entity = 'other'
            tokens = re.findall(r'[0-9A-Za-z\-]+', data.lower())
        self.entities += [entity for _ in range(len(tokens))]
        self.tokens += tokens

    def handle_endtag(self, tag):
        # Remove entity.
        self.tag = None

    def handle_starttag(self, tag, attrs):
        # Set entity to starttag.
        self.tag = tag
