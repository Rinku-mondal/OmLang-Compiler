import sys
import os
import re

OM_VERSION = "v2.0.0-Master"

def smart_input(prompt=""):
    """Automatically converts user input into text or numbers"""
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
        """Transpiles Om code into a final and powerful Python code"""
        py_code = []
        indent = 0

        for idx, line in enumerate(self.lines):
            # Handle empty lines or comments
            if not line or line.startswith('#'):
                py_code.append("    " * indent + line)
                continue

            # Token analysis (supports all types of mathematical and logical symbols)
            tokens = re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'|[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?|\+|-|\*|/|=|<|>|==|!=|<=|>=', line)
            if not tokens:
                continue

            cmd = tokens[0]

            # 1. Om language's signature 'show' keyword (Output)
            if cmd == "show":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"print({expr})")

            # 2. Conditional block (if)
            elif cmd == "if":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"if {expr}:")
                indent += 1

            # 3. Alternative conditional block (else)
            elif cmd == "else":
                indent -= 1
                py_code.append("    " * indent + "else:")
                indent += 1

            # 4. Loop block (repeat)
            elif cmd == "repeat":
                expr = " ".join(tokens[1:])
                py_code.append("    " * indent + f"for _ in range(int({expr})):")
                indent += 1

            # 5. End of block (end)
            elif cmd == "end":
                indent -= 1
                if indent < 0:
                    print(f"Syntax Error (Line {idx+1}): Unexpected 'end' keyword.")
                    sys.exit(1)

            # 6. Global expressions (Variables, math, input, and Python functions)
            else:
                # Convert input function to smart input
                modified_line = line.replace("input(", "smart_input(").replace("input ", "smart_input ")
                py_code.append("    " * indent + modified_line)

        return "\n".join(py_code)

    def run(self):
        """Run code flawlessly without any banner"""
        py_source = self.transpile_to_python()
        
        # Useful Python built-in functions are provided here for the convenience of new users
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
            'abs': abs
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
    
