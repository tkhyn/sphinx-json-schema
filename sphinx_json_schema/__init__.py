from .directive import JsonSchema
from .version import __version__


def setup(app):
    app.add_directive('json-schema', JsonSchema)
    app.add_config_value('json_schema_root_dir', None, 'env')

    return {'version': __version__}
