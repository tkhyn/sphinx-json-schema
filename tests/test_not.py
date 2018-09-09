from unittest import TestCase

from sphinx_json_schema.mergers import merge_and


class NotTestCase(TestCase):

    def test_merge_not(self):
        one = {
            "type": "object",
            "required": ["A", "B"],
            "properties": {
                "A": {
                    "type": "integer",
                    "minimum": 0
                },
                "B": {
                    "type": "string",
                    "enum": ["I", "J", "K", "L"]
                }
            }
        }

        two = {
            "type": "object",
            "required": ["A"],
            "properties": {
                "A": {
                    "type": "integer",
                    "minimum": 0
                }
            }
        }

        three = {
            "type": "object",
            "properties": {
                "B": {
                    "type": "string",
                    "enum": ["L"]
                }
            }
        }

        merged = merge_and(one, two, True)
        merged = merge_and(merged, three, True)

        self.assertDictEqual(merged, {
            "type": "object",
            "required": ["B"],
            "properties" : {
                "B": {
                    "type": "string",
                    "enum": ["I", "J", "K"]
                }
            }
        })
