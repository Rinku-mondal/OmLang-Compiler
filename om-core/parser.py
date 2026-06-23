# =====================================================================
# MODULE: om-core/parser.py
# =====================================================================
import sys
try: from .lexer import TokenType
except: from lexer import TokenType

class AssignNode:
    def init(self, name, value): self.name = name; self.value = value
class ShowNode:
    def init(self, expr): self.expr = expr
class BinOpNode:
    def init(self, left, op, right): self.left = left; self.op = op; self.right = right
class NumNode:
    def init(self, val): self.val = val
class VarNode:
    def init(self, name): self.name = name
class StringNode:
    def init(self, val): self.val = val
class InputNode: pass

# NEW NODES
class IfNode:
    def init(self, condition, body): self.condition = condition; self.body = body
class WhileNode:
    def init(self, condition, body): self.condition = condition; self.body = body

class OmParser:
    def init(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            print(f"Syntax Error: Expected '{token_type}', found '{self.current_token.type}'")
            sys.exit(1)

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token.type == TokenType.SHOW:
            self.consume(TokenType.SHOW)
            return ShowNode(self.comparison())
        elif self.current_token.type == TokenType.IF:
            self.consume(TokenType.IF)
            condition = self.comparison()
            body = self.block()
            return IfNode(condition, body)
        elif self.current_token.type == TokenType.WHILE:
            self.consume(TokenType.WHILE)
            condition = self.comparison()
            body = self.block()
            return WhileNode(condition, body)
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.consume(TokenType.IDENTIFIER)
            self.consume(TokenType.ASSIGN)
            return AssignNode(name, self.comparison())
        else:
            print(f"Syntax Error: Invalid token '{self.current_token.value}'")
            sys.exit(1)

    def block(self):
        self.consume(TokenType.LBRACE)
        stmts = []
        while self.current_token.type not in (TokenType.RBRACE, TokenType.EOF):
            stmts.append(self.statement())
        self.consume(TokenType.RBRACE)
        return stmts

    def comparison(self):
        node = self.expr()
        if self.current_token.type in (TokenType.EQ, TokenType.LT, TokenType.GT):
            op = self.current_token.type
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.expr())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.type
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token.type
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        t = self.current_token
        if t.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumNode(t.value)