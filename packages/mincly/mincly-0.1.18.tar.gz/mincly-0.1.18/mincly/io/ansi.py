import shutil as _shutil
import typing as _t
import sys as _sys
from mincly.io.common import Io as _Io, Writer as _Writer


class AnsiTerminalWriter(_Writer):
    """
    For ANSI compliant terminals, everything outputed to this terminal is stored
    and can be cleared and overwritten at any type. For it to work properly,
    this must be the only source of printed content. If, for some reason, this
    writer cannot determine the running terminal's size, this writer will never
    clear any lines.
    """

    def __init__(
        self,
        add_newline_to_prints: bool = False,
        always_flush: bool = True,
        output_stream: _t.Literal["stdout", "stderr"] = "stdout",
    ) -> None:
        self._last_printed_content: str = ""
        self._print_end = "\n" if add_newline_to_prints else ""
        self._print_flush = always_flush
        self._output_stream = _sys.stdout if output_stream == "stdout" else _sys.stderr
        self._width: _t.Optional[int]
        self._height: _t.Optional[int]
        try:
            terminal_size = _shutil.get_terminal_size()
            self._width, self._height = terminal_size.columns, terminal_size.lines
        except OSError:
            self._width, self._height = None, None

    @property
    def width(self):
        if self._width is None:
            return None
        return _shutil.get_terminal_size().columns

    @property
    def height(self):
        if self._height is None:
            return None
        return _shutil.get_terminal_size().lines

    def write(self, message: str):
        """
        Prints message to terminal. Avoid using ANSI control sequence characters
        in `value`
        """
        if self._width is not None:
            self._last_printed_content += message + self._print_end
        print(
            message,
            end=self._print_end,
            flush=self._print_flush,
            file=self._output_stream,
        )

    def clear_last_n_lines(self, n: int):
        """
        Clears last `n` lines in terminal. Does not change internal printed
        content, you may use this method to rectify content printed outside this
        class.
        """
        if n < 1:
            return
        n = min(n, self.height or 0)
        clear_string = "\033[2K"
        if n > 1:
            clear_string += "\033[A\033[2K" * (n - 1)
        print(clear_string, end="", flush=True, file=self._output_stream)

    def clear(self):
        """
        Clears all content that this class printed. Does not account for printed
        content from other sources
        """
        if self._last_printed_content == "":
            return
        terminal_width = self.width

        if terminal_width is None:
            return

        printed_lines = self._last_printed_content.split("\n")
        number_of_lines_in_terminal = 0
        for printed_line in printed_lines:
            number_of_lines_in_terminal += 1
            remaining_string = printed_line
            while len(remaining_string) > terminal_width:
                number_of_lines_in_terminal += 1
                remaining_string = remaining_string[terminal_width:]
        self.clear_last_n_lines(number_of_lines_in_terminal)
        self._last_printed_content = ""


class AnsiTerminalIo(AnsiTerminalWriter, _Io):
    """
    For ANSI compliant terminals, everything outputed to this terminal is stored
    and can be cleared and overwritten at any type. For it to work properly,
    this must be the only source of printed content.

    `read()` method is counted towards printed content for the purposes of
    `clear`ing the terminal.
    """

    def read(self) -> str:
        """
        Retrieves input using Python's builtin `input` method. Takes into
        account the user's input and newline character (ENTER) for the next call
        to `clear()`.
        """
        user_input = input()
        self._last_printed_content += user_input + "\n"
        return user_input
