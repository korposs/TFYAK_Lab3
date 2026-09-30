from compiler.grammar import KEYWORDS


TYPE_KEYWORDS = {
    "String", "int", "long", "double", "float",
    "boolean", "char", "byte", "short",
}


class SyntaxError:
    def __init__(self, fragment, line, col, message):
        self.fragment = fragment
        self.line = line
        self.col = col
        self.message = message

    def __repr__(self):
        return f"Ошибка: строка {self.line}, позиция {self.col}: {self.message} ('{self.fragment}')"


class Parser:
    def __init__(self):
        self.tokens = []
        self.pos = 0
        self.errors = []

    def parse(self, tokens):
        self.tokens = [t for t in tokens if t.type != "WHITESPACE"]
        self.pos = 0
        self.errors = []

        if not self.tokens:
            self._add_error("", 1, 1,
                            "Пустой текст: ожидается объявление record")
            return self.errors

        state = "START"

        while state != "END":
            cur = self._current()

            if state == "START":
                if cur is None:
                    break

                if self._is_record(cur):
                    self._advance()
                    state = "RECORD"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалось ключевое слово 'record'"
                    )
                    self._advance()

            elif state == "RECORD":
                if cur is None:
                    self._add_eof_error(
                        "Ожидался идентификатор имени структуры"
                    )
                    break

                if cur.type == "IDENTIFIER":
                    self._advance()
                    state = "NAME"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидался идентификатор имени структуры"
                    )

                    if self._is_param_start(cur):
                        state = "NAME"
                    else:
                        self._advance()

            elif state == "NAME":
                if cur is None:
                    self._add_eof_error(
                        "Ожидалась открывающая скобка '('"
                    )
                    break

                if cur.type == "LPAREN":
                    self._advance()
                    state = "PARAM_START"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась открывающая скобка '('"
                    )

                    if self._is_param_start(cur):
                        state = "PARAM_START"
                    else:
                        self._advance()

            elif state == "PARAM_START":
                if cur is None:
                    self._add_eof_error(
                        "Ожидался тип параметра или ')'"
                    )
                    break

                if cur.type == "RPAREN":
                    self._advance()
                    state = "LBRACE"
                elif self._is_type(cur):
                    self._advance()
                    state = "PARAM_NAME"
                elif cur.type == "IDENTIFIER":
                    self._handle_missing_type()
                    state = "PARAM_NAME"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидался тип параметра или ')'"
                    )
                    self._advance()

            elif state == "PARAM_NAME":
                if cur is None:
                    self._add_eof_error(
                        "Ожидался идентификатор параметра"
                    )
                    break

                if cur.type == "IDENTIFIER":
                    self._advance()
                    state = "PARAM_END"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидался идентификатор параметра"
                    )

                    if cur.type in {"COMMA", "RPAREN"}:
                        state = "PARAM_END"
                    else:
                        self._advance()

            elif state == "PARAM_END":
                if cur is None:
                    self._add_eof_error(
                        "Ожидалась ',' или ')'"
                    )
                    break

                if cur.type == "COMMA":
                    self._advance()
                    state = "PARAM_START"
                elif cur.type == "RPAREN":
                    self._advance()
                    state = "LBRACE"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась ',' или ')'"
                    )
                    self._advance()

            elif state == "LBRACE":
                if cur is None:
                    self._add_eof_error(
                        "Ожидалась открывающая фигурная скобка '{'"
                    )
                    break

                if cur.type == "LBRACE":
                    self._advance()
                    state = "RBRACE"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась открывающая фигурная скобка '{'"
                    )

                    if cur.type == "RBRACE":
                        state = "AFTER_RBRACE"
                    else:
                        self._advance()

            elif state == "RBRACE":
                if cur is None:
                    self._add_eof_error(
                        "Ожидалась закрывающая фигурная скобка '}'"
                    )
                    break

                if cur.type == "RBRACE":
                    self._advance()
                    state = "AFTER_RBRACE"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась закрывающая фигурная скобка '}'"
                    )

                    if cur.type == "SEMICOLON":
                        state = "AFTER_RBRACE"
                    else:
                        self._advance()

            elif state == "AFTER_RBRACE":
                if cur is None:
                    self._add_eof_error(
                        "Ожидалась точка с запятой ';'"
                    )
                    break

                if cur.type == "SEMICOLON":
                    self._advance()
                    state = "START"
                elif self._is_record(cur):
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась точка с запятой ';' перед следующим объявлением"
                    )
                    state = "START"
                else:
                    self._add_error(
                        cur.lexeme,
                        cur.line,
                        cur.start,
                        "Ожидалась точка с запятой ';'"
                    )
                    self._advance()

        return self.errors

    def _handle_missing_type(self):
        """Восстановление при пропущенном типе параметра."""

        cur = self._current()

        if cur is None:
            return

        self._add_error(
            cur.lexeme,
            cur.line,
            cur.start,
            "Ожидался тип параметра"
        )

        self._advance()

    def _is_type(self, token):
        return (
            token is not None
            and token.type == "KEYWORD"
            and token.lexeme in TYPE_KEYWORDS
        )

    def _is_record(self, token):
        return (
            token is not None
            and token.type == "KEYWORD"
            and token.lexeme == "record"
        )

    def _is_param_start(self, token):
        if token is None:
            return False

        return (
            token.type == "RPAREN"
            or self._is_type(token)
            or token.type == "IDENTIFIER"
        )

    def _current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _advance(self):
        if self.pos < len(self.tokens):
            self.pos += 1

    def _add_error(self, fragment, line, col, message):
        self.errors.append(SyntaxError(fragment, line, col, message))

    def _add_eof_error(self, message):
        if self.tokens:
            last = self.tokens[-1]
            line = last.line
            col = last.end + 1
        else:
            line = 1
            col = 1

        self._add_error("конец строки", line, col, message)