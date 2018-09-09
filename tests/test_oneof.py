from unittest import TestCase

from sphinx_json_schema.mergers import merge_or


class OneOfTestCase(TestCase):

    def test_merge_oneof(self):
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
            "required": ["A", "B", "C"],
            "properties": {
                "A": {
                    "type": "integer",
                    "minimum": 0
                },
                "B": {
                    "type": "string",
                    "enum": ["I", "J", "K", "L"]
                },
                "C": {
                  "type": "boolean",
                  "const": True
                }
            }
        }

        merged = merge_or(one, two, True)

        self.assertDictEqual(merged, {
            "type": "object",
            "required": ["A", "B"],
            "properties" : {
                "A": {
                    "type": "integer",
                    "minimum": 0
                },
                "B": {
                    "type": "string",
                    "enum": ["I", "J", "K", "L"]
                }
            },
            "$xor": [
                {},
                {
                    "required": ["C"],
                    "properties": {
                        "C": {
                            "type": "boolean",
                            "const": True
                        }
                    }
                }
            ]
        })
