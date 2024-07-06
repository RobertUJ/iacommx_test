""" Module for database utility functions. """
import re


def _to_snake_case(camel_str: str):
    """
    Convert camel case string to snake_case string.

      Args:

        camel_str (str, required): CamelCase string to be converted.
    """
    """ Si termina con vocal, se agrega una s al final, si termina con consonante se 
    agrega excepto si es una z, si terminal con z se cambia por ces."""

    final_letter = camel_str[-1]
    if final_letter in "aeiou":
        camel_str += "s"
    elif final_letter == "z":
        camel_str = f"{camel_str[:-1]}ces"
    else:
        camel_str += "es"

    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()
