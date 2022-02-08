
try:
    # Python >= 3.8
    from collections.abc import Mapping
except ImportError:
    # Python < 3.8
    from collections import Mapping
