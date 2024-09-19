"""
Config for EDeA Pydantic dataclasses.
"""


class PydanticConfig:
    # don't allow adding arbitrary extra fields that we didn't define
    extra = "forbid"
    # don't validate our defaults, we can't run the validation because of our
    # computed fields using @property and @setter
    validate_all = False
