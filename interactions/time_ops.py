def _int_or_zero(piece: str) -> int:
    if piece is None:
        return 0
    try:
        return int(piece)
    except ValueError:
        return 0


def parse_time(time_str: str) -> int:
    seconds: int = 0
    for piece in time_str.split():
        if piece[-1] == 's':
            seconds += _int_or_zero(piece[:-1])
        elif piece[-1] == 'm':
            seconds += _int_or_zero(piece[:-1]) * 60
        elif piece[-1] == 'h':
            seconds += _int_or_zero(piece[:-1]) * 60 * 60
        elif piece[-1] == 'd':
            seconds += _int_or_zero(piece[:-1]) * 60 * 60 * 24
    return seconds
