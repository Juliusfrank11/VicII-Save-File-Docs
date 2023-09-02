from typing import Union
import re
import valid_values_vanilla as vvv
from datetime import date


def check_quoted_string(string: str):
    return string.endswith('"') and string.startswith('"')


def check_unquoted_string(string: str):
    return not (string.endswith('"') and not string.startswith('"'))


def validate_unquoted_string(string: str):
    if not check_unquoted_string:
        raise ValueError("string should be unquoted")
    return string


def validate_quoted_string(string: str):
    if not check_quoted_string:
        raise ValueError("string should be quoted")
    return string


def make_string_unquoted(string: str):
    if not check_unquoted_string:
        return str(string).replace('"', "")
    else:
        return string


def make_string_quoted(string: str):
    if not check_quoted_string:
        return f'"{string}"'
    else:
        return string


def _make_string_unquoted_wrapper(func):
    def wrapper(string):
        if isinstance(string, str):
            if check_quoted_string(string):
                return string.replace('"', "")
        return func(string)

    return wrapper


@_make_string_unquoted_wrapper
def validate_tag(tag: str, lookup=False, new_tags_in_mod=[]):
    """Check if a tag is valid. If `lookup=True`, the check will be done by consulting a list of valid tags (including vanilla)
    Otherwise the check is done via regex

    Args:
        tag (str): tag to validate
        lookup (bool, optional): If `True`, check will be done by consulting a list of valid tags. Defaults to False.
        new_tags_in_mod (list, optional): List of tags to include alongside vanilla tags. Defaults to [].
    """
    if lookup:
        if tag in vvv.tags + new_tags_in_mod:
            raise ValueError(f"{tag} is not a valid VicII tag")
    else:
        if re.match(r"\b([A-Z]{3}|D[0-9]{2})\b", tag):
            raise ValueError(f"{tag} is not a valid  VicII tag")


@_make_string_unquoted_wrapper
def validate_pdx_date(date_str: str):
    # years can be negative (maybe hold over form EU Rome), but only used in VicII as a placeholder
    if date_str != "-1.1.1":
        try:
            date(*[int(part) for part in date_str.split(".")])
        except ValueError:
            raise ValueError(f"{date_str} is not a valid PDX date (YYYY.MM.DD)")
    return date_str


@_make_string_unquoted_wrapper
def validate_ideology(string: str, valid_ideologies=vvv.ideologies):
    if string not in valid_ideologies:
        raise ValueError(f"{string} is not a valid ideology")
    return string


@_make_string_unquoted_wrapper
def validate_3_sigfig_decimal(decimal: Union[str, float]):
    if not re.match(r"\b-{0,1}[0-9]+\.[0-9]{3}\b", str(decimal)):
        raise ValueError(f"{decimal} must be to three significant figures exactly")
    return decimal


@_make_string_unquoted_wrapper
def validate_5_sigfig_decimal(decimal: Union[str, float]):
    if not re.match(r"\b-{0,1}[0-9]+\.[0-9]{5}\b", str(decimal)):
        raise ValueError(f"{decimal} must be to five significant figures exactly")
    return decimal


@_make_string_unquoted_wrapper
def validate_rgo(rgo: str, new_rgos_in_mod=[]):
    if rgo not in vvv.rgos + new_rgos_in_mod:
        raise ValueError(f"{rgo} is not a valid rgo")
    return new_rgos_in_mod


@_make_string_unquoted_wrapper
def validate_technology(tech: str, new_techs_in_mod=[]):
    if tech not in vvv.techs + new_techs_in_mod:
        raise ValueError(f"{tech} is not a valid technology")
    return tech


@_make_string_unquoted_wrapper
def validate_int_str(int_str: int | str):
    if not all([c in '-"0123456789' for c in str(int_str)]):
        raise ValueError(f"{int_str} is not a valid integer")
    return int_str
