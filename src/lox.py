import sys
from scanner import Scanner


class Lox:

    def __init__(self):
        self.had_error = False

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

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True

    def run(self, source: str):
        self.had_error = False
        scanner = Scanner(source, self.error)
        scanner.scan_tokens()
        for token in scanner.tokens:
            print(token)


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv) > 2:
        print("Usage: scanner.py [script]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
