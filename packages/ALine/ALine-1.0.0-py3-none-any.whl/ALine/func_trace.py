from .main import settrace, Int_, Bool_, Tuple_, List_
from inspect import getsourcelines, getmembers, signature
from .color import Style
from typing import Callable
from .error import PrintModeNotFoundError


s = Style()


main_func_name: str = ''
def analyse(in_call: bool = True, set_line: tuple = (-1, -1), print_infos: list[str] = ['default']):
    """
    Print logs from callable lines to debug
    :param in_call: Print logs from called functions. If ``false``, only the current function was logged.
    :param print: ``list['line', 'default', 'variables', 'annotation', 'event', 'filename', 'function']``
    :return: Callable
    """

    def analyse_decorator(func):
        # Permet de récupérer la fonction liée au décorateur

        def get_infos(frame, event: str, arg):
            """
            Fonction appellé à chaque ligne pour loguer celle-ci.
            :param frame:
            :param event: L'évènement actuellement executé
            :param arg: les arguments retournés
            :return:
            """
            global main_func_name

            line = frame.f_lineno
            code = frame.f_code
            func_name = code.co_name

            immutable_in_call: Bool_ = Bool_(in_call) # gère si de mauvais types sont entré en paramètre
            immutable_set_line: Tuple_ = Tuple_(set_line) # gère si de mauvais types sont entré en paramètre
            immutable_print: List_ = List_(print_infos)

            # Si la fonction principale n'est pas enregistré
            if not main_func_name:
                main_func_name = func_name

            # Si on ne demande que la fonction principale et que le nom de la fonction actuellement exec est différente que celle setup en premier
            if not immutable_in_call.bool_ and main_func_name != func_name:
                return get_infos

            # Si on définit une ligne à dépasser pour commencer à loguer et que cette ligne n'a pas encore été dépassé
            if immutable_set_line.tuple_[0] != -1 and line < immutable_set_line.tuple_[0]:
                return get_infos

            if immutable_set_line.tuple_[1] != -1 and line > immutable_set_line.tuple_[1]:
                return

            PrintInfos(frame, event, arg, immutable_print, func)# On print les informations

            return get_infos  # Continuer le traçage

        def wrapper(*args, **kwargs):
            global main_func_name

            settrace(get_infos) # On lance le tracking du module sys

            result = func(*args, **kwargs) # On execute la fonction de base

            settrace(None) # On arrête le tracking

            main_func_name = None # On reset la fonction principale pour ne pas rentrer en conflict au prochain appel
            return result

        return wrapper

    return analyse_decorator


class PrintInfos:

    def __init__(self, frame, event: str, arg, print_infos: List_, func: Callable):
        self.frame = frame
        self.event = event
        self.arg = arg
        self.func: Callable = func
        self.line = frame.f_lineno
        self.code = frame.f_code
        self.func_name = self.code.co_name
        self.filename = self.code.co_filename
        self.variables = frame.f_locals
        self.func_members: list = getmembers(func)

        self.print: List_ = print_infos

        source_lines, starting_line = getsourcelines(frame.f_code)  # On récupère toutes les lignes du code
        self.sourceLine = source_lines[self.line - starting_line].strip()  # On obtient le contenue de la ligne actuellement exec

        self.result = ''
        self.funcs = {
            'line': self.__line,
            'default': self.__default,
            'variables': self.__local_variables,
            'annotation': self.__func_annotations,
            'event': self.__event,
            'filename': self.__filename,
            'function': self.__function

        }

        self.__select_print_mode()

    def __print_infos(self) -> None:
        print(self.result)

    def __select_print_mode(self):

        for mode in self.print.list_:
            mode = mode.lower()

            if mode in self.funcs.keys():
                self.funcs[mode]()

            else:
                raise PrintModeNotFoundError(mode)

        print('\n' + self.result)

    def __line(self) -> None:
        """
        Add the line number
        :return: str
        """
        self.result += f"Ligne: {s.color_arg(self.line, s.YELLOW, s.BOLD)}\n"

    def __event(self) -> None:
        """
        Add the frame event
        :return:
        """
        self.result += f"Event: {s.color_arg(self.event, s.BLUE, s.SURROUND)}\n"

    def __filename(self) -> None:
        """
        Add filename
        :return:
        """
        self.result += f"{s.ITALICS}(file {self.filename}){s.DEFAULT}\n"

    def __function(self) -> None:
        """
        Add function name
        """
        self.result += f"Function : {s.color_arg(self.func_name, s.RED)}\n"


    def __local_variables(self) -> None:
        """
        Add local variables from function
        :return:
        """
        x = '\n    '
        self.result += f"Variables :\n    {x.join(f'{s.color_arg(key, s.PINK)}  >>>  {s.color_arg(value, s.HIGHLIGHT_WHITE, s.BLACK)} ({s.color_arg(type(value), s.LIGHT_GREEN)})' for key, value in self.variables.items())}"

    def __func_annotations(self) -> None:
        """
        Add function annotations arguments
        :return:
        """
        if self.func_members[0][1]:
            x = '\n    '.join([f'{s.color_arg(key, s.LIGHT_PURPLE)} ({s.color_arg(value, s.LIGHT_GREEN)})' for key, value in self.func_members[0][1].items()])
        else:
            x = s.color_arg("EMPTY", s.HIGHLIGHT_LIGHT_RED, s.BLACK)


        self.result += f"Annotations arguments :\n    {x}\n"


    def __default(self) -> None:
        """
        Add default parameters
        :return:
        """
        self.result += (f"Event: {s.color_arg(self.event, s.BLUE, s.SURROUND)}, "
                        f"Ligne: {s.color_arg(self.line, s.YELLOW, s.BOLD)}, "
                        f"Function : {s.color_arg(self.func_name, s.RED)}, "
                        f"{s.ITALICS}(file {self.filename}){s.DEFAULT}\n")

        self.result += f"Content line : {s.color_arg(self.sourceLine, s.LIGHT_GREY)}\n"

        if self.event == 'return':
            self.result += f"Return : {s.color_arg(self.arg, s.GREEN)}, Type : {s.color_arg(type(self.arg), s.LIGHT_GREEN)}\n"




