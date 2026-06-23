# =====================================================================
# MODULE: om-core/compiler.py
# =====================================================================
try:
    from .opcodes import OpCode; from .lexer import TokenType
    from .parser import NumNode, VarNode, AssignNode, ShowNode, BinOpNode, StringNode, InputNode, IfNode, WhileNode
except:
    from opcodes import OpCode; from lexer import TokenType
    from parser import NumNode, VarNode, AssignNode, ShowNode, BinOpNode, StringNode, InputNode, IfNode, WhileNode

class OmBytecodeCompiler:
    def init(self):
        self.bytecode = []; self.constants = []

    def add_constant(self, value):
        if value not in self.constants: self.constants.append(value)
        return self.constants.index(value)

    def compile(self, ast):
        for stmt in ast: self.gen(stmt)
        self.bytecode.append(OpCode.HALT)
        return self.bytecode, self.constants

    def gen(self, node):
        if isinstance(node, NumNode):
            val = float(node.val) if '.' in node.val else int(node.val)
            self.bytecode.extend([OpCode.LOAD_CONST, self.add_constant(val)])
        elif isinstance(node, StringNode):
            self.bytecode.extend([OpCode.LOAD_CONST, self.add_constant(node.val)])
        elif isinstance(node, InputNode):
            self.bytecode.append(OpCode.INPUT)
        elif isinstance(node, VarNode):
            self.bytecode.extend([OpCode.LOAD_VAR, node.name])
        elif isinstance(node, AssignNode):
            self.gen(node.value)
            self.bytecode.extend([OpCode.STORE_VAR, node.name])
        elif isinstance(node, ShowNode):
            self.gen(node.expr)
            self.bytecode.append(OpCode.PRINT)
        
        # NEW: Compile IF statements
        elif isinstance(node, IfNode):
            self.gen(node.condition)
            self.bytecode.extend([OpCode.JUMP_FALSE, 0]) # 0 is a placeholder
            jump_idx = len(self.bytecode) - 1
            for stmt in node.body: self.gen(stmt)
            self.bytecode[jump_idx] = len(self.bytecode) # Patch the placeholder
            
        # NEW: Compile WHILE loops
        elif isinstance(node, WhileNode):
            start_idx = len(self.bytecode)
            self.gen(node.condition)
            self.bytecode.extend([OpCode.JUMP_FALSE, 0])
            jump_idx = len(self.bytecode) - 1
            for stmt in node.body: self.gen(stmt)
            self.bytecode.extend([OpCode.JUMP, start_idx]) # Loop back to start
            self.bytecode[jump_idx] = len(self.bytecode)   # Patch loop exit

        elif isinstance(node, BinOpNode):
            self.gen(node.left)
            self.gen(node.right)
            if node.op == TokenType.PLUS: self.bytecode.append(OpCode.ADD)
            elif node.op == TokenType.MINUS: self.bytecode.append(OpCode.SUB)
            elif node.op == TokenType.MUL: self.bytecode.append(OpCode.MUL)
            elif node.op == TokenType.DIV: self.bytecode.append(OpCode.DIV)
            elif node.op == TokenType.EQ: self.bytecode.append(OpCode.CMP_EQ)
            elif node.op == TokenType.LT: self.bytecode.append(OpCode.CMP_LT)
            elif node.op == TokenType.GT: self.bytecode.append(OpCode.CMP_GT)