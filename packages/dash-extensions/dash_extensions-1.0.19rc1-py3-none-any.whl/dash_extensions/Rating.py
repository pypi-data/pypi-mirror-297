# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Rating(Component):
    """A Rating component.
Rating component based on https://github.com/voronianski/react-star-rating-component

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- activeColor (string; optional):
    This is the color of the icon in the active state.

- count (number; optional):
    The number of Icons to display.

- defaultColor (string; optional):
    This is the color of the icon in the inactive state.

- defaultValue (string; optional):
    Required. This is the value of the rating displayed by default.
    Supply this if your rating is also a readOnly.

- readOnly (boolean; default True):
    This sets the component to be non editable.

- shape (string; optional):
    This is the shape displayed as icon.

- size (string; optional):
    This defines the size of the Icons used.

- spacing (string; optional):
    This defines the fap between the Icons used."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'Rating'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, defaultValue=Component.UNDEFINED, count=Component.UNDEFINED, shape=Component.UNDEFINED, readOnly=Component.UNDEFINED, size=Component.UNDEFINED, spacing=Component.UNDEFINED, activeColor=Component.UNDEFINED, defaultColor=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'activeColor', 'count', 'defaultColor', 'defaultValue', 'readOnly', 'shape', 'size', 'spacing']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'activeColor', 'count', 'defaultColor', 'defaultValue', 'readOnly', 'shape', 'size', 'spacing']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Rating, self).__init__(**args)
