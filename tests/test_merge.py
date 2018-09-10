"""
Multiple nested merge of different types
"""


from unittest import TestCase
from copy import deepcopy

from sphinx_json_schema.mergers import merge_and, merge_or


class MergeTestCase(TestCase):

    def test_merge_allOf_oneOf(self):

        base = {
            "type": "object",
            "required": ["A", "B"],
            "properties": {
                "A": {
                    "type": "integer"
                },
                "B": {
                    "type": "string",
                    "enum": ["a", "b", "c"]
                }
            }
        }

        sch_xor = merge_or(
            deepcopy(base),
            merge_and(base, {
                "type": "object",
                "required": ["X"],
                "properties": {
                    "X": {
                        "type": "boolean",
                        "const": True
                    }
                }
            }), True
        )

        self.assertDictEqual(
            sch_xor,
            {
                "type": "object",
                "required": ["A", "B"],
                "properties": {
                    "A": {
                        "type": "integer"
                    },
                    "B": {
                        "type": "string",
                        "enum": ["a", "b", "c"]
                    }
                },
                "$xor": [
                    {}, {
                        "required": ["X"],
                        "properties": {
                            "X": {
                                "type": "boolean",
                                "const": True
                            }
                        }
                    }
                ]
            }
        )

        schema = merge_and(
            sch_xor,
            {
                "type": "object",
                "required": ["C"],
                "properties": {
                    "B": {
                        "enum": ["c"]
                    },
                    "C": {
                        "type": "string"
                    }
                }
            }
        )

        self.assertDictEqual(
            schema,
            {
                "type": "object",
                "required": ["A", "B", "C"],
                "properties": {
                    "A": {
                        "type": "integer"
                    },
                    "B": {
                        "type": "string",
                        "enum": ["c"]
                    },
                    "C": {
                        "type": "string"
                    }
                },
                "$xor": [
                    {}, {
                        "required": ["X"],
                        "properties": {
                            "X": {
                                "type": "boolean",
                                "const": True
                            }
                        }
                    }
                ]
            }
        )
