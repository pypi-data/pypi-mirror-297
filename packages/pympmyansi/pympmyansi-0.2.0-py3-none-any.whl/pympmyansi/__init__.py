import sys


# TODO figure out how to do this in a way that enables ide autocompletion
# i cant figure out the enum
codes = {
    'fg_black':        "\033[0;30m",
    'fg_red':          "\033[0;31m",
    'fg_green':        "\033[0;32m",
    'fg_brown':        "\033[0;33m",
    'fg_blue':         "\033[0;34m",
    'fg_purple':       "\033[0;35m",
    'fg_cyan':         "\033[0;36m",
    'fg_light_gray':   "\033[0;37m",
    'fg_dark_gray':    "\033[1;30m",
    'fg_light_red':    "\033[1;31m",
    'fg_light_green':  "\033[1;32m",
    'fg_yellow':       "\033[1;33m",
    'fg_light_blue':   "\033[1;34m",
    'fg_light_purple': "\033[1;35m",
    'fg_light_cyan':   "\033[1;36m",
    'fg_light_white':  "\033[1;37m",
    'fg_bright_black': "\033[1;90m",
    'fg_bright_red':   "\033[0;91m",
    'fg_bright_green': "\033[0;92m",
    'fg_bright_brown': "\033[0;93m",
    'fg_bright_blue':  "\033[0;94m",
    'fg_brght_purple': "\033[0;95m",
    'fg_bright_cyan':  "\033[0;96m",
    'fg_bright_light_gray':  "\033[0;97m",
    'fg_bright_dark_gray':   "\033[1;90m",
    'fg_bright_light_red':   "\033[1;91m",
    'fg_bright_light_green': "\033[1;92m",
    'fg_bright_yellow':      "\033[1;93m",
    'fg_bright_light_blue':  "\033[1;94m",
    'fg_bright_light_purple': "\033[1;95m",
    'fg_bright_light_cyan':  "\033[1;96m",
    'fg_bright_light_white': "\033[1;97m",
    'bg_black':        "\033[0;30m",
    'bg_red':          "\033[0;31m",
    'bg_green':        "\033[0;32m",
    'bg_brown':        "\033[0;33m",
    'bg_blue':         "\033[0;34m",
    'bg_purple':       "\033[0;35m",
    'bg_cyan':         "\033[0;36m",
    'bg_light_gray':   "\033[0;37m",
    'bg_dark_gray':    "\033[1;30m",
    'bg_light_red':    "\033[1;31m",
    'bg_light_green':  "\033[1;32m",
    'bg_yellow':       "\033[1;33m",
    'bg_light_blue':   "\033[1;34m",
    'bg_light_purple': "\033[1;35m",
    'bg_light_cyan':   "\033[1;36m",
    'bg_light_white':  "\033[1;37m",
    'bg_bright_black':        "\033[0;90m",
    'bg_bright_red':          "\033[0;91m",
    'bg_bright_green':        "\033[0;92m",
    'bg_bright_brown':        "\033[0;93m",
    'bg_bright_blue':         "\033[0;94m",
    'bg_bright_purple':       "\033[0;95m",
    'bg_bright_cyan':         "\033[0;96m",
    'bg_bright_light_gray':   "\033[0;97m",
    'bg_bright_dark_gray':    "\033[1;90m",
    'bg_bright_light_red':    "\033[1;91m",
    'bg_bright_light_green':  "\033[1;92m",
    'bg_bright_yellow':       "\033[1;93m",
    'bg_bright_light_blue':   "\033[1;94m",
    'bg_bright_light_purple': "\033[1;95m",
    'bg_bright_light_cyan':   "\033[1;96m",
    'bg_bright_light_white':  "\033[1;97m",
    'bold':         "\033[1m",
    'faint':        "\033[2m",
    'italic':       "\033[3m",
    'underline':    "\033[4m",
    'blink':        "\033[5m",
    'negative':     "\033[7m",
    'crossed':      "\033[9m",
    'end':          "\033[0m",
}


def pymp(input: str, code: str) -> str:
    """Returns a string enclosed within the necessary ANSI escape codes.

    Args:
        input (str): The input string.
        color (str): The desired code.

    Returns:
        str
    """
    if not sys.stdout.isatty():
        return input
    else:
        return codes[code] + input + codes['end']


def pymp256(input: str, color: int, fgorbg: str = 'fg'):
    """"""
    if not sys.stdout.isatty():
        return input
    if color < 0 or color > 255:
        raise Exception("Invalid color!")
    else:
        if fgorbg == 'fg':
            return "\033[38;5;" + \
                str(color) + 'm' + input + codes['end']  # type: ignore
        else:
            return "\033[48;5;" + \
                str(color) + 'm' + input + codes['end']  # type: ignore


def pymprgb(input: str, rgb: tuple[int, int, int], fgorbg: str):
    """"""
    if not sys.stdout.isatty():
        return input
    for x in rgb:
        if x < 0 or x > 255:
            raise Exception("Invalid color!")
    else:
        tempstr = str(rgb[0]) + ";" + str(rgb[1]) + ";" + \
            str(rgb[2]) + "m"
        if fgorbg == 'fg':
            return "\033[38;2;" + tempstr + input + codes['end']
        else:
            return "\033[48;2;" + tempstr + input + codes['end']
