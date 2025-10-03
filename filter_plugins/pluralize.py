
# Modified version of https://github.com/audreyr/jinja2_pluralize

def pluralize(value, arg='s', arg2=None):
    """A Jinja2 filter that returns a plural suffix if the value is not 1.

    This filter is adapted from Django's `pluralize` filter. It returns a
    plural suffix if the given value is not 1. The default suffix is 's'.

    Examples:
        - `{{ 1 | pluralize }}` will output nothing.
        - `{{ 2 | pluralize }}` will output 's'.
        - `{{ 2 | pluralize('es') }}` will output 'es'.
        - `{{ 1 | pluralize('y', 'ies') }}` will output 'y'.
        - `{{ 2 | pluralize('y', 'ies') }}` will output 'ies'.

    Args:
        value (int or list): The value to check for pluralization. Can be an
            integer or a list.
        arg (str, optional): The suffix to use for the plural case. If `arg2`
            is provided, this will be the suffix for the singular case.
            Defaults to 's'.
        arg2 (str, optional): The suffix to use for the plural case when a
            different suffix is needed for the singular case. Defaults to None.

    Returns:
        str: The plural or singular suffix based on the value.
    """
    if arg2 is not None:
        singular_suffix = arg
        plural_suffix = arg2
    else:
        singular_suffix = ''
        plural_suffix = arg

    try:
        if int(value) != 1:
            return plural_suffix
    except ValueError:  # Invalid string that's not a number.
        pass
    except TypeError:  # Value isn't a string or a number; maybe it's a list?
        try:
            if len(value) != 1:
                return plural_suffix
        except TypeError:  # len() of unsized object.
            pass
    return singular_suffix


class FilterModule(object):
    """A class to provide the pluralize filter to Ansible."""

    def filters(self):
        """Returns a dictionary of filters.

        Returns:
            dict: A dictionary mapping filter names to filter functions.
        """
        return {
            'pluralize': pluralize
        }
