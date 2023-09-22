from yacut import constants as const


def length_symbol_validate(short_id: str) -> bool:
    if len(short_id) > 16:
        return False

    for i in short_id:
        if i not in const.LETTER_AND_DIGITS:
            return False
    return True
