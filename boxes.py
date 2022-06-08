import re
import io
from colorama import Fore, Back, Style, init


init()


def _modified_len(x):
    # https://stackoverflow.com/a/14889588
    # At least for the ANSI TTY escape sequence, this works.
    # For backspaces \b or vertical tabs or \r vs \n -- it depends how and where it is printed.
    strip_ANSI_pat = re.compile(r"""
        \x1b     # literal ESC
        \[       # literal [
        [;\d]*   # zero or more digits or semicolons
        [A-Za-z] # a letter
        """, re.VERBOSE).sub

    def strip_ANSI(s):
        return strip_ANSI_pat("", s)

    if isinstance(x, str):
        return len(strip_ANSI(x))
    return len(x)


def _print_to_string(*args, **kwargs):
    with io.StringIO() as output:
        print(*args, file=output, **kwargs)
        content = output.getvalue()
        output.close()
        return content



def print_box(text, title=None, width=60, height=None, border_color=Fore.RESET, text_color=Fore.RESET):
    # width az gelirse en uzun kelimenin 4 fazlası olur.

    global content
    content = ""

    def print(*args, **kwargs):
        global content
        content += _print_to_string(*args, **kwargs)
    
    words = text.split(" ")
    max_word_len = max([_modified_len(word) for word in words])
    if width < max_word_len + 4:
        width = max_word_len + 4

    effective_width = width - 4
    text_lines = [words[0]]
    for word in words[1:]:
        if _modified_len(text_lines[-1]) + 1 + _modified_len(word) <= effective_width:
            text_lines[-1] += " " + word
        else:
            text_lines.append(word)
    
    if height is None:
        height = _modified_len(text_lines) + 4  # by default 2 empty lines
    elif height < _modified_len(text_lines):
        height = _modified_len(text_lines) + 2  # height cannot be less than needed
    
    total_empty_lines = height - _modified_len(text_lines) - 2
    start_empty_lines = total_empty_lines // 2
    end_empty_lines = total_empty_lines - start_empty_lines
    
    empty_line = border_color + "│ " + " " * effective_width + " │" + Fore.RESET
    if title:
        left = (width - _modified_len(title)) // 2
        right = width - _modified_len(title) - left
        print(border_color + "┌" + "─" * (left - 2), title, "─" * (right - 2) + "┐" + Fore.RESET)
    else:
        print(border_color + "┌" + "─" * (width - 2) + "┐" + Fore.RESET)
    print((empty_line + "\n") * start_empty_lines, end="")
    for line in text_lines:
        total = effective_width - _modified_len(line)
        left = total // 2
        right = total - left
        centered_line = " " * left + line + " " * right
        print(border_color + "│ " + text_color + centered_line + border_color + " │" + Fore.RESET)
    print((empty_line + "\n") * end_empty_lines, end="")
    print(border_color + "└" + "─" * (width - 2) + "┘" + Fore.RESET)
    
    return content


class MessageBox:

    def __init__(self, text, title=None, width=60, height=None, border_color=Fore.RESET, text_color=Fore.RESET):
        self.text = text
        self.title = title
        self.width = width
        self.height = height
        self.border_color = border_color
        self.text_color = text_color
        self.content = print_box(self.text, title=self.title, width=self.width, height=self.height, border_color=self.border_color, text_color=self.text_color)

    def print(self):
        print(self.content)

    def __str__(self):
        return self.content


class HorizontalBoxes:

    def __init__(self, *boxes, align="top"):
        assert align in ("top", "bottom", "center")

        self.boxes = boxes
        
        self.boxes_lines = []
        for box in self.boxes:
            box_lines = str(box).splitlines()
            self.boxes_lines.append(box_lines)
        assert _modified_len(self.boxes) == _modified_len(self.boxes_lines)

        # Box içinde yükseklikleri eşit yapalım (gerçi burada zaten eşit):
        for box_idx, box_lines in enumerate(self.boxes_lines):
            max_width = max(_modified_len(line) for line in box_lines)
            for idx, line in enumerate(box_lines):
                box_lines[idx] = line.ljust(max_width)  # padding with spaces
                self.boxes_lines[box_idx] = box_lines
                # for example:
                assert max_width == _modified_len(self.boxes_lines[box_idx][0]) == _modified_len(self.boxes_lines[box_idx][1])
        
        # Bütün boxların yükseklikleri eşit olsun:
        max_height = max(_modified_len(box_lines) for box_lines in self.boxes_lines)
        for idx, box_lines in enumerate(self.boxes_lines):
            width = _modified_len(box_lines[0])
            empty_line = width * " "
            if align == "top":
                empty_lines = (max_height - _modified_len(box_lines)) * [empty_line]
                self.boxes_lines[idx] = box_lines + empty_lines
            elif align == "bottom":
                empty_lines = (max_height - _modified_len(box_lines)) * [empty_line]
                self.boxes_lines[idx] = empty_lines + box_lines
            else:
                num_empty_lines = max_height - _modified_len(box_lines)
                num_top_empty_lines = num_empty_lines // 2
                num_bottom_empty_lines = num_empty_lines - num_top_empty_lines
                top_empty_lines = num_top_empty_lines * [empty_line]
                bottom_empty_lines = num_bottom_empty_lines * [empty_line]
                self.boxes_lines[idx] = top_empty_lines + box_lines + bottom_empty_lines

        # for example:
        assert max_height == _modified_len(self.boxes_lines[0]) == _modified_len(self.boxes_lines[1])

        self.content = ""
        height = _modified_len(self.boxes_lines[0])
        for line_idx in range(height):
            for box_lines in self.boxes_lines:
                self.content += box_lines[line_idx]
            self.content += "\n"

    def print(self):
        print(self.content)

    def __str__(self):
        return self.content


class VerticalBoxes:

    def __init__(self, *boxes, align="left"):
        assert align in ("left", "right", "center")

        self.boxes = boxes
        
        self.boxes_lines = []
        for box in self.boxes:
            box_lines = str(box).splitlines()
            self.boxes_lines.append(box_lines)
        assert _modified_len(self.boxes) == _modified_len(self.boxes_lines)

        # Box içinde yükseklikleri eşit yapalım
        # Gerçi burada zaten eşit, gerek yok...
        
        # Bütün boxların genişlikleri eşit olsun:
        max_width = max(_modified_len(box_lines[0]) for box_lines in self.boxes_lines)
        for box_lines in self.boxes_lines:
            for idx, line in enumerate(box_lines):
                if align == "left":
                    box_lines[idx] = line + (max_width - _modified_len(line)) * " "
                elif align == "right":
                    box_lines[idx] = (max_width - _modified_len(line)) * " " + line
                else:
                    total = max_width - _modified_len(line)
                    left = total // 2
                    right = total - left
                    box_lines[idx] = left * " " + line + right * " "

        self.content = ""
        for box_lines in self.boxes_lines:
            for line in box_lines:
                self.content += line + "\n"

    def print(self):
        print(self.content)

    def __str__(self):
        return self.content
