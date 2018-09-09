"""
JSON schema loader helpers
"""

from collections import Mapping


def merge(base, to_merge, mode):
    if mode == 'allOf':
        merge_all_of(base, to_merge)
    else:
        raise RuntimeError('Merging mode "%s" is not supported yet' % mode)

def merge_all_of(base, to_merge):
    """
    Merge json schemas assuming an 'allOf' command
    """
    if not base:
        return to_merge

    for key, val in base.items():
        if isinstance(val, Mapping):
            try:
                merge_all_of(val, to_merge[key])
            except KeyError:
                pass
        elif isinstance(val, list):
            try:
                other_val = to_merge[key]
                if not isinstance(other_val, list):
                    raise KeyError
                if key == 'enum':
                    for v in set(val).symmetric_difference(other_val):
                        val.remove(v)
                elif key == 'required':
                    for v in other_val:
                        if v not in val:
                            val.append(v)
            except KeyError:
                base[key] = val
        else:
            # normal update
            try:
                base[key] = to_merge[key]
            except KeyError:
                pass

    for key in set(to_merge.keys()).difference(base.keys()):
        base[key] = to_merge[key]

    return base
