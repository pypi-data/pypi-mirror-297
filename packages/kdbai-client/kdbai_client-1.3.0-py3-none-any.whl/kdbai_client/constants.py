from enum import Enum


class VdbScopes(Enum):
    """Enum class to define vdb scopes"""

    MetaManaged = 'vdbMetaManaged', 'metaManaged'
    MetaFromRef = 'vdbMetaFromRef', 'metaFromRef'
    NoMeta = 'vdbNoMeta', 'noMeta'
    ALL = 'all', None

    def __new__(cls, value, category):
        """Add category attribute to enum entries"""
        member = object.__new__(cls)
        member._value_ = value
        member.category = category
        return member

p_type_mapping = {
    'bool': 'b',
    'guid': 'g',
    'uint8': 'x',
    'int16': 'h',
    'int32': 'i',
    'int64': 'j',
    'float32': 'e',
    'float64': 'f',
    'bytes': 'C',
    'str': 's',
    'datetime': 'p',
    'timedelta': 'n',
    'datetime64[ns]': 'p',
    'timedelta64[ns]': 'n',
    'char': 'c',
    'float32s': 'E',
    'float64s': 'F',
    'dict': ' '
}

q_type_mapping = dict(
    boolean='b',
    guid='g',
    byte='x',
    short='h',
    int='i',
    long='j',
    real='e',
    float='f',
    string='C',
    symbol='s',
    timestamp='p',
    timespan='n',
    char='c',
    reals='E',
    floats='F'
)
q_type_mapping[' '] = ' '
