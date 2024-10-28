from typing import TextIO
import sys
import os


def define_ast(output_dir: str, base_name: str, types: list[str]):
    print(f"Output dir: {output_dir}")
    print(f"Abstract Syntax Tree: {base_name}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    path = output_dir + "/" + base_name + ".py"
    with open(path, "w") as file:
        file.write("from abc import ABC, abstractmethod\n\n")
        file.write(f"class {base_name}(ABC):\n")
        file.write("    @abstractmethod\n")
        file.write("    def accept(self, visitor):\n")
        file.write("        pass\n")

        define_visitor(file, base_name, types)

        print(f"Types: {types}")
        for type in types:
            print(f"Type: {type}")
            class_name = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            print(f"Class name: {class_name}")
            print(f"Fields: {fields}")
            define_type(file, base_name, class_name, fields)

        file.write("\n")


def define_type(file: TextIO, base_name: str, class_name: str, fields: str):
    file.write(f"\n\nclass {class_name}({base_name}):\n")
    # parameters = fields.split(", ")
    # parameters = [parameter.split(" ")[1] for parameter in parameters]
    parameters = ", ".join([field.split(" ")[1] for field in fields.split(", ")])
    file.write(f"    def __init__(self, {parameters}):\n")
    for field in fields.split(", "):
        name = field.split(" ")[1]
        file.write(f"        self.{name} = {name}\n")
    file.write("\n")
    file.write("    def accept(self, visitor):\n")
    file.write(f"        return visitor.visit_{class_name}(self)\n")


def define_visitor(file: TextIO, base_name: str, types: list[str]):
    file.write("\n\nclass Visitor(ABC):\n")
    for type in types:
        type_name = type.split(":")[0].strip()
        file.write("    @abstractmethod\n")
        file.write(f"    def visit_{type_name}(self, {base_name.lower()}):\n")
        file.write("        pass\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_ast <output directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    define_ast(
        output_dir,
        "Expr",
        [
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Object value",
            "Unary    : Token operator, Expr right",
        ],
    )
