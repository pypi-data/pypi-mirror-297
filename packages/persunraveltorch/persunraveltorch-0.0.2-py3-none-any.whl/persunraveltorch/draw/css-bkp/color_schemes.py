from .._read_template import _read_template


__all__ = [ 'LIGHT_SCHEME',
            'DARK_SCHEME',
            'LIGHT_DARK_SCHEME'
           ]


LIGHT_SCHEME = _read_template( "light-scheme.css" )

DARK_SCHEME = _read_template( "dark-scheme.css" )

LIGHT_DARK_SCHEME = (
    LIGHT_SCHEME +
    " @media (prefers-color-scheme: dark) { " +
    DARK_SCHEME +
    " }"
)
