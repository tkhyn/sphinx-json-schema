# -*- coding: utf-8 -*-


import os.path

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.directives.code import container_wrapper

from .loader import JsonSchemaLoader
from .version import __version__


class JsonSchema(Directive):
    optional_arguments = 1
    has_content = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        assert self.name == 'jsonschema'

        try:
            file_or_url = self.arguments[0]
            if not file_or_url.startswith('http') and not os.path.isabs(file_or_url):
                # file relative to the path of the current rst file
                dname = os.path.dirname(self.state_machine.input_lines.source(0))
                file_or_url = os.path.join(dname, file_or_url)
        except IndexError:
            file_or_url = None

        self.schema = JsonSchemaLoader(
            *((file_or_url,) or (self.content, self.state_machine.input_lines.source(0)))
        )

    def run(self):
        code = self.schema.render()
        literal = nodes.literal_block(code, code)
        literal['language'] = 'json'
        # add a caption
        literal = container_wrapper(self, literal, 'JSON schema' + self.schema.version)
        return [literal]

def setup(app):
    app.add_directive('jsonschema', JsonSchema)
    return {'version': __version__}
