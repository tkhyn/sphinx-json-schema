from .directive import JsonSchema
from .version import __version__


def setup(app):
    app.add_directive('jsonschema', JsonSchema)
    return {'version': __version__}
