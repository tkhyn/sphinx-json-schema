from unittest import TestCase

from sphinx_json_schema.helpers import merge_all_of


class AllOfTestCase(TestCase):

    def test_merge_properties(self):
        base = {
            'required': ['A'],
            'properties' : {
                'A': {
                    'type': 'string',
                    'enum': ['x', 'y']
                },
                'B': {
                    'type': 'string'
                }
            }
        }

        to_merge = {
            'required': ['C'],
            'properties' : {
                'A': {
                    'type': 'string',
                    'enum': ['x']
                },
                'C': {
                    'type': 'string'
                }
            }
        }

        merge_all_of(base, to_merge)

        self.assertDictEqual(base, {
            'required': ['A', 'C'],
            'properties' : {
                'A': {
                    'type': 'string',
                    'enum': ['x']
                },
                'B': {
                    'type': 'string'
                },
                'C': {
                    'type': 'string'
                }
            }
        })
