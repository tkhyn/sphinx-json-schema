"""
A jsonschema loader / merger
"""

import os
import json
from jsonpointer import resolve_pointer
import requests
from collections import OrderedDict
import re

from .mergers import merge


ORDER = ['$ref', 'description', 'oneOf', 'anyOf', 'type', 'required', 'properties', "dependencies",
         '$xor', '$or']


class JsonSchemaLoader(object):

    def __init__(self, file, content=None):
        self.file = file

        if content:
            self.schema = self._load_internal(content)
        else:
            filename, pointer = self._splitpointer(file)
            self._load_external(filename)
            if pointer:
                self.schema = resolve_pointer(self.schema, pointer)

        self.version = self.schema.pop('$schema', '')
        if self.version:
            try:
                self.version = ' (%s)' % re.match(
                    r'http://json-schema.org/(draft-\d\d)/schema#', self.version
                ).groups()[0]
            except AttributeError:
                self.version = ''

    def _load_internal(self, text):
        if text is None or len(text) == 0:
            raise RuntimeError(
                "json-schema directive requires either filename, http url or inline content"
            )
        self.schema = self.ordered_load('\n'.join(text))

    def _load_external(self, file_or_url):
        if file_or_url.startswith('http'):
            text = requests.get(file_or_url)
            self.schema = self.ordered_load(text.content)
        else:
            # will raise an exception if file is not found
            with open(file_or_url) as file:
                self.schema = self.ordered_load(file)

    def _splitpointer(self, path):
        val = path.split('#', 1)
        if len(val) == 1:
            val.append(None)
        return val

    def ordered_load(self, stream):

        # creates an ordered dictionary from a list of pairs
        def object_pairs_hook(pairs):
            d = {}
            for i, (key, value) in enumerate(pairs):
                if key == '$ref':
                    d.clear()
                    d['$ref'] = value
                    d.update(JsonSchemaLoader(
                        os.path.join(
                            os.path.dirname(stream if type(stream) == 'str' else self.file), value
                        )
                    ).schema)
                    break
                elif key in ['allOf', 'oneOf', 'anyOf']:
                    # value is a list of dictionaries, they should be merged
                    for dd in value:
                        merge(d, dd, key)
                else:
                    d[key] = value

            # order the output
            ordered = OrderedDict()
            for k in ORDER:
                try:
                    ordered[k] = d[k]
                except KeyError:
                    pass

            for k in set(d.keys()).difference(ORDER):
                ordered[k] = d[k]

            return ordered

        if type(stream) == str:
            result = json.loads(stream, object_pairs_hook=object_pairs_hook)
        else:
            stream.seek(0)
            result = json.load(stream, object_pairs_hook=object_pairs_hook)

        return result

    def render(self):
        return json.dumps(self.schema, indent=2)

