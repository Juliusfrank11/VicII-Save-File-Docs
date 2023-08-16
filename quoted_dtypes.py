from validators import (
    validate_pdx_date,
    validate_tag,
    validate_3_sigfig_decimal,
    validate_5_sigfig_decimal,
    validate_ideology,
    validate_rgo,
    validate_technology,
    validate_int_str,
    check_quoted_string,
)


class PDXVariable(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"


class PDXDate(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_pdx_date(value)


class Tag(str):
    def __init__(self, value, lookup=False, new_tags_in_mod=[]):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_tag(value, lookup, new_tags_in_mod)


class ThreeSigFigDecimal(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_3_sigfig_decimal(value)


class FiveSigFigDecimal(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_5_sigfig_decimal(value)


class Int(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        assert validate_int_str(value)


class Ideology(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_ideology(value)


class RGO(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_rgo(value)


class Technology(str):
    def __init__(self, value):
        assert check_quoted_string(value), "Should be encased in double quotes"
        validate_technology(value)
