def get_symbol(decimal: int) -> chr:
    if decimal < 10:
        return str(decimal)

    if decimal < 36:
        return chr(97 + decimal - 10)

    return chr(65 + decimal - 36)


def shorten_url(pk: int) -> str:
    short_url = ""
    quotient = pk

    while quotient >= 62:
        quotient = quotient // 62
        remainder = quotient % 62
        short_url += get_symbol(remainder)

    short_url += get_symbol(quotient)
    return short_url
