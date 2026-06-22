import sys
import os
import re
import math

OM_VERSION = "v2.7.1-Object-Oriented-Fixed"

def smart_input(prompt=""):
    """Automatically converts user input into text or numerical types."""
    val = input(prompt)
    try:
        if '.' in val:
            return float(val)
        return int(val)
    except ValueError:
        return val

class OmCompiler:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.load_file()

    def load_file(self):
        if not self.filename.endswith('.om'):
            print("Error: Om compiler only supports '.om' files.")
            sys.exit(1)
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.lines = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

    def transpile_to_python(self):
        """Transpiles OM source code into executable Python code with unique native functions and Objects."""
        py_code = []
        indent = 0
        in_object_block = False

        for idx, line in enumerate(self.lines):
            # Handle empty lines or comments
            if not line or line.startswith('#'):
                py_code.append("    " * indent + line)
                continue

            # FIXED TOKENIZER: Multi-character operators (==, !=, <=, >=) are checked first to prevent syntax splitting
            tokens = re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'|==|!=|<=|>=|[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?|\+|-|\*|/|=|<|>', line)
            if not tokens:
                continue

            cmd = tokens[0]

            # 1. Output handling (show)
            if cmd == "show":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"print({expr})")

            # 2. Object Blueprint Block Definition
            elif cmd == "object":
                if len(tokens) < 2:
                    print(f"Syntax Error (Line {idx+1}): Object class name is missing.")
                    sys.exit(1)
                obj_name = tokens[1]
                py_code.append("    " * indent + f"class {obj_name}:")
                indent += 1
                in_object_block = True

            # 3. Custom Functions & Object Methods (fn)
            elif cmd == "fn":
                if len(tokens) < 2:
                    print(f"Syntax Error (Line {idx+1}): Function name is missing.")
                    sys.exit(1)
                func_name = tokens[1]
                
                if in_object_block:
                    if func_name == "setup":
                        func_name = "__init__"
                    args_list = ["self"] + tokens[2:]
                    args = ", ".join(args_list)
                else:
                    args = ", ".join(tokens[2:])
                    
                py_code.append("    " * indent + f"def {func_name}({args}):")
                indent += 1

            # 4. Conditionals (if)
            elif cmd == "if":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"if {expr}:")
                indent += 1

            # 5. Multi-conditionals (elif)
            elif cmd == "elif":
                indent -= 1
                if indent < 0:
                    print(f"Syntax Error (Line {idx+1}): Unexpected 'elif' keyword.")
                    sys.exit(1)
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"elif {expr}:")
                indent += 1

            # 6. Alternative block (else)
            elif cmd == "else":
                indent -= 1
                if indent < 0:
                    print(f"Syntax Error (Line {idx+1}): Unexpected 'else' keyword.")
                    sys.exit(1)
                py_code.append("    " * indent + "else:")
                indent += 1

            # 7. Fixed Loops (repeat)
            elif cmd == "repeat":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"for _ in range(int({expr})):")
                indent += 1

            # 8. Dynamic Loops (while)
            elif cmd == "while":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"while {expr}:")
                indent += 1

            # 9. Function Return Handling
            elif cmd == "return":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"return {expr}")

            # 10. Scope terminator (end)
            elif cmd == "end":
                indent -= 1
                if indent < 0:
                    print(f"Syntax Error (Line {idx+1}): Unexpected 'end' keyword.")
                    sys.exit(1)
                if indent == 0:
                    in_object_block = False

            # 11. Global expressions, Variable assignments & Object assignments
            else:
                modified_line = line.replace("input(", "smart_input()").replace("input ", "smart_input ")
                
                if in_object_block and indent > 1 and "=" in tokens:
                    eq_idx = tokens.index("=")
                    if eq_idx == 1:
                        modified_line = f"self.{tokens[0]} = " + " ".join(tokens[2:])
                
                py_code.append("    " * indent + modified_line)

        if indent != 0:
            print("Syntax Error: Missing 'end' keyword somewhere in your code.")
            sys.exit(1)

        return "\n".join(py_code)

    def run(self):
        """Executes OM code with its own unique native libraries and objects injected."""
        py_source = self.transpile_to_python()
        
        global_context = {
            'print': print,
            'input': smart_input,
            'smart_input': smart_input,
            'int': int,
            'float': float,
            'str': str,
            'len': len,
            'range': range,
            'round': round,
            'abs': abs,
            
            # --- OMlang Unique Native Library Functions ---
            'om_root': math.sqrt,
            'om_power': math.pow,
            'om_pi': math.pi,
            'om_system_os': os.name,
            'om_current_dir': os.getcwd
        }
        try:
            exec(py_source, global_context)
        except Exception as e:
            print(f"Runtime Error: {e}")

    def transpile_only(self, target):
        if target == "python":
            base_name = os.path.splitext(self.filename)[0]
            output_file = f"{base_name}.py"
            code = self.transpile_to_python()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)

def cli():
    if len(sys.argv) < 3:
        print("Om CLI Usage:")
        print("  om run <filename.om>")
        print("  om build <filename.om> --target python")
        return

    action = sys.argv[1]
    filename = sys.argv[2]
    
    compiler = OmCompiler(filename)

    if action == "run":
        compiler.run()
    elif action == "build" and len(sys.argv) == 5 and sys.argv[3] == "--target":
        compiler.transpile_only(sys.argv[4])

if __name__ == "__main__":
    cli()
        
