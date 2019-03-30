from .directive import JsonSchema
from .version import __version__


def setup(app):
    app.add_directive('jsonschema', JsonSchema)
    app.add_config_value('jsonschema_root_dir', None, 'env')

    return {'version': __version__}
