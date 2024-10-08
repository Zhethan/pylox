from scanner_token import Token, TokenType
from typing import Callable


class Scanner:

    KEYWORDS = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str, error: Callable):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.error = error

    def scan_tokens(self) -> list:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        match c:
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '{': self.add_token(TokenType.LEFT_BRACE)
            case '}': self.add_token(TokenType.RIGHT_BRACE)
            case ',': self.add_token(TokenType.COMMA)
            case '.': self.add_token(TokenType.DOT)
            case '-': self.add_token(TokenType.MINUS)
            case '+': self.add_token(TokenType.PLUS)
            case ';': self.add_token(TokenType.SEMICOLON)
            case '*': self.add_token(TokenType.STAR)
            case '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)  # noqa: E701
            case '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('*'):
                    while (self.peek() != '*' or self.peek_next() != '/') and not self.is_at_end():
                        if self.peek() == '\n':
                            self.line += 1
                        self.advance()

                    if self.is_at_end():
                        # Handle unterminated comment
                        self.error(self.line, "Unterminated block comment.")
                    else:
                        self.advance()  # Consume the '*'
                        self.advance()  # Consume the '/'
                elif self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t': pass
            case '\n': self.line += 1
            case '"': self.string()
            case _:
                if self.isdigit(c):
                    self.number()
                elif self.isalpha(c):
                    self.identifier()
                else:
                    self.error(self.line, f"Unexpected character: |{c}|")

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if (self.source[self.current] != expected):
            return False
        self.current += 1
        return True
    

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.isalnum(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        if text in self.KEYWORDS:
            self.add_token(self.KEYWORDS[text])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error("Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.isdigit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.isdigit(self.peek_next()):
            self.advance()
            while self.isdigit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(
            self.source[self.start:self.current]))

    def isdigit(self, c: str) -> bool:
        return c >= '0' and c <= '9'

    def isalpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def isalnum(self, c: str) -> bool:
        return self.isalpha(c) or self.isdigit(c)

    def advance(self) -> str:
        self.current += 1
        print(f"Current: {self.current}")
        print(f"Source: {self.source[self.current - 1]}")
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
