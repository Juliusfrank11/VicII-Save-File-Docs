from typing import Union
import re
import valid_values_vanilla as vvv
from datetime import date


def check_quoted_string(string: str):
    return string.endswith('"') and string.startswith('"')


def check_unquoted_string(string: str):
    return not (string.endswith('"') and string.startswith('"'))


def make_string_unquoted(func):
    def wrapper(string):
        if isinstance(string, str):
            if check_quoted_string(string):
                return string.replace('"', "")
        return func(string)

    return wrapper


@make_string_unquoted
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


@make_string_unquoted
def validate_pdx_date(date_str: str):
    try:
        date(*[int(part) for part in date_str.split(".")])
    except ValueError:
        raise ValueError(f"{date_str} is not a valid PDX date (YYYY.MM.DD)")


@make_string_unquoted
def validate_ideology(string: str, valid_ideologies=vvv.ideologies):
    if string not in valid_ideologies:
        raise ValueError(f"{string} is not a valid ideology")


@make_string_unquoted
def validate_3_sigfig_decimal(decimal: Union[str, float]):
    if not re.match(r"\b-{0,1}[0-9]+\.[0-9]{3}\b", str(decimal)):
        raise ValueError(f"{decimal} must be to three significant figures exactly")


@make_string_unquoted
def validate_5_sigfig_decimal(decimal: Union[str, float]):
    if not re.match(r"\b-{0,1}[0-9]+\.[0-9]{5}\b", str(decimal)):
        raise ValueError(f"{decimal} must be to five significant figures exactly")


@make_string_unquoted
def validate_rgo(rgo: str, new_rgos_in_mod=[]):
    if rgo not in vvv.rgos + new_rgos_in_mod:
        raise ValueError(f"{rgo} is not a valid rgo")


@make_string_unquoted
def validate_technology(tech: str, new_techs_in_mod=[]):
    if tech not in vvv.techs + new_techs_in_mod:
        raise ValueError(f"{tech} is not a valid technology")
