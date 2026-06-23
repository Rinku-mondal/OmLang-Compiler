import sys
import os
import math
import time

OM_VERSION = "v3.3.0-English-Core-Libs"

# =====================================================================
# 1. THE LEXER (Strictly English Keywords & Standard Identifiers)
# =====================================================================
class TokenType:
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    
    # Keywords
    SHOW = "show"
    INPUT = "input"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    END = "end"
    WHILE = "while"
    REPEAT = "repeat"
    FN = "fn"
    OBJECT = "object"
    RETURN = "return"
    
    # Operators & Punctuations
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","
    EQ = "=="
    NEQ = "!="
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="

ENGLISH_KEYWORDS = {
    "show": TokenType.SHOW,
    "input": TokenType.INPUT,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "else": TokenType.ELSE,
    "end": TokenType.END,
    "while": TokenType.WHILE,
    "repeat": TokenType.REPEAT,
    "fn": TokenType.FN,
    "object": TokenType.OBJECT,
    "return": TokenType.RETURN
}

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line})"

class OmLexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line_num = 1
        self.current_char = self.text[0] if text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char == '\n':
                self.line_num += 1
                self.advance()
                continue
            if self.current_char.isspace():
                self.advance()
                continue

            if self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            if self.current_char in ('"', "'"):
                quote = self.current_char
                self.advance()
                val = ""
                while self.current_char is not None and self.current_char != quote:
                    val += self.current_char
                    self.advance()
                if self.current_char is None:
                    print(f"Lexer Error (Line {self.line_num}): Unterminated string literal.")
                    sys.exit(1)
                self.advance()
                return Token(TokenType.STRING, val, self.line_num)

            if self.current_char.isdigit() or self.current_char == '.':
                val = ""
                while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                    val += self.current_char
                    self.advance()
                return Token(TokenType.NUMBER, val, self.line_num)

            # Strictly parsing standard ASCII English alphanumeric sequences
            if self.current_char.isalpha() or self.current_char == '_':
                val = ""
                while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                    val += self.current_char
                    self.advance()
                
                # Enforce clean case-insensitivity on standard keywords
                lower_val = val.lower()
                t_type = ENGLISH_KEYWORDS.get(lower_val, TokenType.IDENTIFIER)
                return Token(t_type, val if t_type == TokenType.IDENTIFIER else lower_val, self.line_num)

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ, "==", self.line_num)
                return Token(TokenType.ASSIGN, "=", self.line_num)
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NEQ, "!=", self.line_num)
                print(f"Lexer Error (Line {self.line_num}): Unknown token structure '!'")
                sys.exit(1)
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE, "<=", self.line_num)
                return Token(TokenType.LT, "<", self.line_num)
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE, ">=", self.line_num)
                return Token(TokenType.GT, ">", self.line_num)

            mapping = {
                '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MUL,
                '/': TokenType.DIV,  '(': TokenType.LPAREN, ')': TokenType.RPAREN,
                ',': TokenType.COMMA
            }
            if self.current_char in mapping:
                t = Token(mapping[self.current_char], self.current_char, self.line_num)
                self.advance()
                return t

            print(f"Lexer Error (Line {self.line_num}): Invalid character '{self.current_char}'")
            sys.exit(1)

        return Token(TokenType.EOF, None, self.line_num)

# =====================================================================
# 2. THE PARSER (Assembles trees & supports explicit Library Calls)
# =====================================================================
class ASTNode: pass
class ProgramNode(ASTNode):
    def __init__(self, body): self.body = body
class ShowNode(ASTNode):
    def __init__(self, exprs): self.exprs = exprs
class AssignNode(ASTNode):
    def __init__(self, name, value): self.name = name; self.value = value
class BinOpNode(ASTNode):
    def __init__(self, left, op, right): self.left = left; self.op = op; self.right = right
class VarNode(ASTNode):
    def __init__(self, name): self.name = name
class NumNode(ASTNode):
    def __init__(self, val): self.val = val
class StringNode(ASTNode):
    def __init__(self, val): self.val = val
class InputNode(ASTNode): pass
class CallNode(ASTNode):
    def __init__(self, name, args): self.name = name; self.args = args

class IfNode(ASTNode):
    def __init__(self, condition, body, o_elifs, o_else):
        self.condition = condition; self.body = body
        self.elifs = o_elifs; self.else_body = o_else

class OmParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg):
        print(f"Syntax Error (Line {self.current_token.line}): {msg}")
        sys.exit(1)

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, found {self.current_token.type}")

    def parse(self):
        body = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.statement()
            if stmt: body.append(stmt)
        return ProgramNode(body)

    def statement(self):
        t = self.current_token
        if t.type == TokenType.SHOW:
            self.consume(TokenType.SHOW)
            exprs = [self.expr()]
            while self.current_token.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
                exprs.append(self.expr())
            return ShowNode(exprs)
            
        elif t.type == TokenType.IF:
            return self.parse_if_block()
            
        elif t.type == TokenType.IDENTIFIER:
            name = t.value
            self.consume(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.expr())
                    while self.current_token.type == TokenType.COMMA:
                        self.consume(TokenType.COMMA)
                        args.append(self.expr())
                self.consume(TokenType.RPAREN)
                return CallNode(name, args)
                
            self.consume(TokenType.ASSIGN)
            val = self.expr()
            return AssignNode(name, val)
            
        elif t.type in (TokenType.END, TokenType.ELIF, TokenType.ELSE):
            return None
        else:
            self.error(f"Unexpected base command pattern '{t.value}'")

    def parse_if_block(self):
        self.consume(TokenType.IF)
        cond = self.expr()
        if_body = []
        elifs = []
        else_body = []

        while self.current_token.type not in (TokenType.END, TokenType.ELIF, TokenType.ELSE, TokenType.EOF):
            s = self.statement()
            if s: if_body.append(s)

        while self.current_token.type == TokenType.ELIF:
            self.consume(TokenType.ELIF)
            elif_cond = self.expr()
            elif_body = []
            while self.current_token.type not in (TokenType.END, TokenType.ELIF, TokenType.ELSE, TokenType.EOF):
                s = self.statement()
                if s: elif_body.append(s)
            elifs.append((elif_cond, elif_body))

        if self.current_token.type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            while self.current_token.type not in (TokenType.END, TokenType.EOF):
                s = self.statement()
                if s: else_body.append(s)

        self.consume(TokenType.END)
        return IfNode(cond, if_body, elifs, else_body)

    def expr(self):
        return self.comparison()

    def comparison(self):
        node = self.arithmetic()
        ops = (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE)
        if self.current_token.type in ops:
            op = self.current_token.value
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.arithmetic())
        return node

    def arithmetic(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.current_token.value
            self.consume(self.current_token.type)
            node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        t = self.current_token
        if t.type == TokenType.NUMBER:
            self.consume(TokenType.NUMBER)
            return NumNode(t.value)
        elif t.type == TokenType.STRING:
            self.consume(TokenType.STRING)
            return StringNode(t.value)
        elif t.type == TokenType.INPUT:
            self.consume(TokenType.INPUT)
            if self.current_token.type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                self.consume(TokenType.RPAREN)
            return InputNode()
        elif t.type == TokenType.IDENTIFIER:
            name = t.value
            self.consume(TokenType.IDENTIFIER)
            if self.current_token.type == TokenType.LPAREN:
                self.consume(TokenType.LPAREN)
                args = []
                if self.current_token.type != TokenType.RPAREN:
                    args.append(self.expr())
                    while self.current_token.type == TokenType.COMMA:
                        self.consume(TokenType.COMMA)
                        args.append(self.expr())
                self.consume(TokenType.RPAREN)
                return CallNode(name, args)
            return VarNode(name)
        elif t.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.expr()
            self.consume(TokenType.RPAREN)
            return node
        self.error(f"Unexpected math or string factor '{t.value}'")

# =====================================================================
# 3. CODE GENERATOR
# =====================================================================
class OmGenerator:
    def __init__(self):
        self.indent_level = 0

    def generate(self, node):
        if isinstance(node, ProgramNode):
            return "\n".join(self.generate(s) for s in node.body)
        
        spacing = "    " * self.indent_level
        
        if isinstance(node, ShowNode):
            args = ", ".join(self.generate(e) for e in node.exprs)
            return f"{spacing}print({args})"
            
        elif isinstance(node, AssignNode):
            return f"{spacing}{node.name} = {self.generate(node.value)}"
            
        elif isinstance(node, InputNode):
            return "smart_input()"
            
        elif isinstance(node, CallNode):
            args = ", ".join(self.generate(a) for a in node.args)
            return f"{spacing}{node.name}({args})"
            
        elif isinstance(node, BinOpNode):
            return f"({self.generate(node.left)} {node.op} {self.generate(node.right)})"
            
        elif isinstance(node, VarNode):
            return node.name
            
        elif isinstance(node, NumNode):
            return node.val
            
        elif isinstance(node, StringNode):
            return f'"{node.val}"'
            
        elif isinstance(node, IfNode):
            lines = [f"{spacing}if {self.generate(node.condition)}:"]
            self.indent_level += 1
            for s in node.body: lines.append(self.generate(s))
            self.indent_level -= 1
            
            for cond, body in node.elifs:
                lines.append(f"{spacing}elif {self.generate(cond)}:")
                self.indent_level += 1
                for s in body: lines.append(self.generate(s))
                self.indent_level -= 1
                
            if node.else_body:
                lines.append(f"{spacing}else:")
                self.indent_level += 1
                for s in node.else_body: lines.append(self.generate(s))
                self.indent_level -= 1
                
            return "\n".join(lines)

# =====================================================================
# 4. RUNTIME ENVIRONMENT & ENGLISH SYSTEM LIBRARIES
# =====================================================================
def smart_input(prompt=""):
    val = input(prompt)
    try:
        if '.' in val: return float(val)
        return int(val)
    except ValueError:
        return val

class OmCompiler:
    def __init__(self, filename):
        self.filename = filename
        self.source_text = ""
        self.load_file()

    def load_file(self):
        if not self.filename.endswith('.om'):
            print("Error: Om compiler only supports '.om' files.")
            sys.exit(1)
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.source_text = f.read()
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

    def run(self):
        lexer = OmLexer(self.source_text)
        parser = OmParser(lexer)
        ast = parser.parse()
        
        generator = OmGenerator()
        py_source = generator.generate(ast)
        
        # English-exclusive global context with clean library spaces
        global_context = {
            'print': print,
            'smart_input': smart_input,
            'int': int, 'float': float, 'str': str, 'len': len,
            'round': round, 'abs': abs,
            
            # --- Library: om_math ---
            'om_math_sqrt': math.sqrt,
            'om_math_pow': math.pow,
            'om_math_abs': math.fabs,
            'om_math_pi': lambda: math.pi,
            
            # --- Library: om_sys ---
            'om_sys_platform': lambda: sys.platform,
            'om_sys_cwd': os.getcwd,
            
            # --- Library: om_time ---
            'om_time_now': time.time,
            'om_time_sleep': time.sleep
        }
        
        start_time = time.perf_counter()
        try:
            exec(py_source, global_context)
        except Exception as e:
            print(f"Runtime Error: {e}")
            
        end_time = time.perf_counter()
        execution_ms = (end_time - start_time) * 1000
        print(f"\n----------------------------------------\nOMlang Runtime: {execution_ms:.2f} ms\n----------------------------------------")

def cli():
    if len(sys.argv) < 3 or sys.argv[1] != "run":
        print("Om CLI Usage: om run <filename.om>")
        return
    compiler = OmCompiler(sys.argv[2])
    compiler.run()

if __name__ == "__main__":
    cli()
            
