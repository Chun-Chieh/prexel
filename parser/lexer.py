"""
Code in this class is based on https://ruslanspivak.com/lsbasi-part6/
"""
from prexel.parser.token import Token
from prexel.regex import REGEX


class Lexer:
    """
     ____________ 
    |   Lexer    |
    |------------|
    |text        |
    |position    |
    |current     |
    |marker_found|
    |____________|

    """
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current = self.text[self.position]
        self.marker_found = False

    def step(self):
        self.position += 1
        if self.position >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.position]

    def skip_whitespace(self):
        while self.current is not None and self.current.isspace():
            self.step()

    def element(self):
        string = ""
        while self.current is not None and not self.current.isspace():
            string += self.current
            self.step()
        return string

    def get_token(self):
        while self.current is not None:
            if self.current.isspace():
                self.skip_whitespace()
                continue
            elif self.current == "|":
                self.step()
                if not self.marker_found:
                    self.marker_found = True
                    return Token(Token.PREXEL_MARKER, "|")
                else:
                    continue
            else:
                element = self.element()

                # Skip incorrect aggregation token format
                if element in ("<<>", "<>>", "<>", "<<>>"):
                    continue

                # Check element against some regex

                if REGEX["class_name"].match(element):
                    self.step()
                    return Token(Token.CLASS_NAME, element)

                if REGEX["inheritance"].match(element):
                    self.step()
                    return Token(Token.INHERITANCE, element)

                aggregation = REGEX["aggregation"].match(element)

                if aggregation:
                    # Optional groupings returned from regex
                    # <>(* or digit)---(name)---(* or digit)-->
                    left_multi, name, right_multi = aggregation.groups()

                    values = {
                        "left_multi": left_multi,
                        "name": name,
                        "right_multi": right_multi
                    }

                    self.step()
                    return Token(Token.AGGREGATION, values)

                if REGEX["method_signature"].match(element):
                    self.step()
                    return Token(Token.METHOD, element)
                else:
                    self.step()
                    return Token(Token.FIELD, element)