from typing import Any
class Style:

    def __init__(self):
        """
        Setup the Style class for use colors and more
        """
        pass


    def __set_style(self, color: int):
        return f"\033[{color}m"

    def color_arg(self, arg: Any, *color: str) -> str:
        """
        Color any args from the param "color".
        EX : color_arg("My arg", BLUE, BOLD, ITALICS)

        :param color: Property from "Style" class.
        :param arg: Any
        :return: A sting like "\033[5mMY ARG\033[0m
        """
        return f"{''.join(color)}{arg}{self.DEFAULT}"


    @property
    def DEFAULT(self) -> str:
        return self.__set_style(0)

    @property
    def BOLD(self) -> str:
        return self.__set_style(1)

    @property
    def BOLD_ITALICS(self) -> str:
        return self.__set_style(4)

    @property
    def ITALICS(self) -> str:
        return self.__set_style(3)

    @property
    def CROSS(self) -> str:
        return self.__set_style(27)

    @property
    def SURROUND(self) -> str:
        return self.__set_style(51)

    @property
    def BLACK(self) -> str:
        return self.__set_style(30)

    @property
    def LIGHT_RED(self) -> str:
        return self.__set_style(31)

    @property
    def LIGHT_GREEN(self) -> str:
        return self.__set_style(32)

    @property
    def LIGHT_PURPLE(self) -> str:
        return self.__set_style(34)

    @property
    def LIGHT_PINK(self) -> str:
        return self.__set_style(95)

    @property
    def LIGHT_BLUE(self) -> str:
        return self.__set_style(36)

    @property
    def LIGHT_GREY(self) -> str:
        return self.__set_style(37)

    @property
    def PINK(self) -> str:
        return self.__set_style(35)

    @property
    def GREY(self) -> str:
        return self.__set_style(90)

    @property
    def RED(self) -> str:
        return self.__set_style(91)

    @property
    def GREEN(self) -> str:
        return self.__set_style(92)

    @property
    def YELLOW(self) -> str:
        return self.__set_style(93)

    @property
    def BLUE(self) -> str:
        return self.__set_style(94)

    @property
    def CYAN(self) -> str:
        return self.__set_style(96)

    @property
    def BROWN(self) -> str:
        return self.__set_style(33)

    @property
    def HIGHLIGHT_BLACK(self) -> str:
        return self.__set_style(40)

    @property
    def HIGHLIGHT_LIGHT_RED(self) -> str:
        return self.__set_style(41)

    @property
    def HIGHLIGHT_LIGHT_GREEN(self) -> str:
        return self.__set_style(42)

    @property
    def HIGHLIGHT_BROWN(self) -> str:
        return self.__set_style(43)

    @property
    def HIGHLIGHT_PURPLE(self) -> str:
        return self.__set_style(44)

    @property
    def HIGHLIGHT_PINK(self) -> str:
        return self.__set_style(45)

    @property
    def HIGHLIGHT_LIGHT_BLUE(self) -> str:
        return self.__set_style(46)

    @property
    def HIGHLIGHT_LIGHT_GREY(self) -> str:
        return self.__set_style(47)

    @property
    def HIGHLIGHT_GREY(self) -> str:
        return self.__set_style(100)

    @property
    def HIGHLIGHT_RED(self) -> str:
        return self.__set_style(101)

    @property
    def HIGHLIGHT_GREEN(self) -> str:
        return self.__set_style(102)

    @property
    def HIGHLIGHT_YELLOW(self) -> str:
        return self.__set_style(103)

    @property
    def HIGHLIGHT_BLUE(self) -> str:
        return self.__set_style(104)

    @property
    def HIGHLIGHT_LIGHT_PINK(self) -> str:
        return self.__set_style(105)

    @property
    def HIGHLIGHT_CYAN(self) -> str:
        return self.__set_style(106)

    @property
    def HIGHLIGHT_WHITE(self) -> str:
        return self.__set_style(107)