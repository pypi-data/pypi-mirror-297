try:
    from pydantic.v1 import *  # noqa: F403
    from pydantic.v1 import ConstrainedStr, utils  # noqa: F401
except ImportError:
    from pydantic import *  # noqa: F403


class NonEmptyStr(ConstrainedStr):
    min_length: int = 1
