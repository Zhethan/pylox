from Expr import Expr, Visitor
from scanner_token import Token, TokenType


class Interpreter(Visitor):
    def visit_Binary(self, expr: Expr) -> object:
        left: object = self.evaluate(expr.left)
        right: object = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError("Operands must be two numbers or two strings for +")
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        if expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        if expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        if expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        if expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        if expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        if expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        raise RuntimeError("Invalid binary operator")

    def visit_Grouping(self, expr):
        return self.evaluate(expr.expression)

    def visit_Literal(self, expr):
        return expr.value

    def visit_Unary(self, expr: Expr) -> object:
        right: object = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        if expr.operator.token_type == TokenType.BANG:
            return not right
        raise RuntimeError("Invalid unary operator")

    def evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def is_truthy(self, obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator: Token, operand: object):
        if isinstance(operand, float):
            return
        raise RuntimeError(f"Operand must be a number for {operator}")

    def check_number_operands(self, operator: Token, left: object, right: object):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RuntimeError(f"Operands must be numbers for {operator}")

    class RuntimeError(RuntimeError):
        def __init__(self, message: str, token: Token):
            super().__init__(message)
            self.token = token

    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            print(value)
        except self.RuntimeError as e:
            print(f"{e.token} {e.message}")

    def stringify(self, obj: object) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)
