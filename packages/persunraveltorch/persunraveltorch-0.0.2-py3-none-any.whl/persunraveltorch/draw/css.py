from ._read_template import _read_template


__all__ = [
    'LIGHT_SCHEME',
    'DARK_SCHEME',
    'LIGHT_DARK_SCHEME',
    'POLYLINE'
]


#: :class:`str`: CSS styles for <polyline> elements.
POLYLINE = _read_template( "polyline.css" )

#: :class:`str`: CSS styles for a light color scheme.
LIGHT_SCHEME = _read_template( "light-scheme.css" )

#: :class:`str`: CSS styles for a dark color scheme.
DARK_SCHEME = _read_template( "dark-scheme.css" )

#: :class:`str`: CSS styles combining light and dark schemes with media query.
LIGHT_DARK_SCHEME = (
    LIGHT_SCHEME +
    " @media (prefers-color-scheme: dark) { " +
    DARK_SCHEME +
    " }"
)
