# =====================================================================
# MODULE: om-core/compiler.py (WITH STRING SUPPORT)
# =====================================================================
try:
    from .opcodes import OpCode
    from .lexer import TokenType
    from .parser import NumNode, VarNode, AssignNode, ShowNode, BinOpNode, StringNode
except (ImportError, ValueError):
    from opcodes import OpCode
    from lexer import TokenType
    from parser import NumNode, VarNode, AssignNode, ShowNode, BinOpNode, StringNode

class OmBytecodeCompiler:
    def init(self):
        self.bytecode = []
        self.constants = []

    def add_constant(self, value):
        if value not in self.constants:
            self.constants.append(value)
        return self.constants.index(value)

    def compile(self, ast):
        for stmt in ast:
            self.gen(stmt)
        self.bytecode.append(OpCode.HALT)
        return self.bytecode, self.constants

    def gen(self, node):
        if isinstance(node, NumNode):
            val = float(node.val) if '.' in node.val else int(node.val)
            const_idx = self.add_constant(val)
            self.bytecode.extend([OpCode.LOAD_CONST, const_idx])
            
        elif isinstance(node, StringNode): # <-- NEW
            const_idx = self.add_constant(node.val)
            self.bytecode.extend([OpCode.LOAD_CONST, const_idx])
            
        elif isinstance(node, VarNode):
            self.bytecode.extend([OpCode.LOAD_VAR, node.name])
            
        elif isinstance(node, AssignNode):
            self.gen(node.value)
            self.bytecode.extend([OpCode.STORE_VAR, node.name])
            
        elif isinstance(node, ShowNode):
            self.gen(node.expr)
            self.bytecode.append(OpCode.PRINT)
            
        elif isinstance(node, BinOpNode):
            self.gen(node.left)
            self.gen(node.right)
            if node.op == TokenType.PLUS: self.bytecode.append(OpCode.ADD)
            elif node.op == TokenType.MINUS: self.bytecode.append(OpCode.SUB)
            elif node.op == TokenType.MUL: self.bytecode.append(OpCode.MUL)
            elif node.op == TokenType.DIV: self.bytecode.append(OpCode.DIV)