import sys
from parser import Parser

from interpreter import Interpreter
from scanner import Scanner
from scanner_token import Token, TokenType


class Lox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter()

    def run_prompt(self):
        while True:
            try:
                # Print the propytmpt character
                print("> ", end="")
                # Read a line of input from the user
                line = input()
                # If the line is empty, break the loop
                if line == "":
                    break
                # Call the 'run' function with the input line (you'll need to implement the run function)
                self.run(line)
                self.had_error = False
            except EOFError:
                # Break on EOF (Ctrl+D in Unix/Linux, Ctrl+Z in Windows)
                break

    def run_file(self, source):
        with open(source) as file:
            self.run(file.read())
            if self.had_error:
                sys.exit(65)
            if self.had_runtime_error:
                sys.exit(70)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def error(self, token: Token, message: str):  # noqa: F811
        if token.token_type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, error: RuntimeError):  # noqa: F811
        print(f"{error.message}\n[line {error.token.line}]")
        self.had_runtime_error = True

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

    def run(self, source: str):
        self.had_error = False
        scanner = Scanner(source, self.error)
        scanner.scan_tokens()
        # for token in scanner.tokens:
        #     print(token)
        parser = Parser(scanner.tokens, self.error)
        expression = parser.parse()
        if self.had_error:
            return
        print(expression)
        self.interpreter.interpret(expression)


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: scanner.py [script]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
