import sys
import os
import re

OM_VERSION = "v1.2.0-Production"
OM_BANNER = f"""
=========================================
      🕉️  OM PROGRAMMING LANGUAGE  🕉️
   {OM_VERSION} | Production Ready Core
=========================================
"""

class OmCompiler:
    def __init__(self, filename):
        self.filename = filename
        self.lines = []
        self.load_file()

    def load_file(self):
        if not self.filename.endswith('.om'):
            print(OM_BANNER)
            print("Error: Om compiler only supports '.om' files.")
            sys.exit(1)
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.lines = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print(OM_BANNER)
            print(f"Error: File '{self.filename}' not found.")
            sys.exit(1)

    def transpile_to_python(self):
        """Core logic to transpile Om code into backend Python"""
        py_code = []
        indent = 0

        for idx, line in enumerate(self.lines):
            if not line or line.startswith('#'):
                py_code.append("    " * indent + line)
                continue

            # Tokenizer to separate words, numbers, and logical operators
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*|\d+(?:\.\d+)?|\+|-|\*|/|=|<|>|==|!=', line)
            if not tokens:
                continue

            cmd = tokens[0]

            # Variable assignment: set x = 10
            if cmd == "set" and len(tokens) >= 4 and tokens[2] == "=":
                var_name = tokens[1]
                expr = "".join(tokens[3:])
                py_code.append("    " * indent + f"{var_name} = {expr}")

            # Print output to screen: show x
            elif cmd == "show":
                expr = "".join(tokens[1:])
                py_code.append("    " * indent + f"print({expr})")

            # Condition: if x > 5
            elif cmd == "if":
                expr = "".join(tokens[1:])
                py_code.append("    " * indent + f"if {expr}:")
                indent += 1

            # Alternative condition: else
            elif cmd == "else":
                indent -= 1
                py_code.append("    " * indent + "else:")
                indent += 1

            # Loop/Repetition: repeat 5
            elif cmd == "repeat":
                expr = "".join(tokens[1:])
                py_code.append("    " * indent + f"for _ in range(int({expr})):")
                indent += 1

            # End of block: end
            elif cmd == "end":
                indent -= 1
                if indent < 0:
                    print(OM_BANNER)
                    print(f"Syntax Error (Line {idx+1}): Unexpected 'end' statement used.")
                    sys.exit(1)
            else:
                # Hybrid execution (direct code processing)
                py_code.append("    " * indent + line)

        return "\n".join(py_code)

    def run(self):
        """Run the .om file directly"""
        print(OM_BANNER)
        print("-> Engine Status: Active")
        print("-" * 41)
        
        py_source = self.transpile_to_python()
        try:
            exec(py_source, {})
            print("-" * 41)
            print("🎉 Execution Completed Successfully!")
        except Exception as e:
            print("-" * 41)
            print(f"Runtime Error: {e}")

    def transpile_only(self, target):
        """Export raw code of another language"""
        if target == "python":
            base_name = os.path.splitext(self.filename)[0]
            output_file = f"{base_name}.py"
            code = self.transpile_to_python()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            print(OM_BANNER)
            print(f"🎉 Transpiled successfully to Python: {output_file}")
        else:
            print(f"Error: {target} support is coming soon.")

def cli():
    """Control the compiler's Command Line Interface (CLI)"""
    if len(sys.argv) < 3:
        print(OM_BANNER)
        print("Om CLI Usage:")
        print("  python om.py run <filename.om>")
        print("  python om.py build <filename.om> --target python")
        return

    action = sys.argv[1]
    filename = sys.argv[2]
    
    compiler = OmCompiler(filename)

    if action == "run":
        compiler.run()
    elif action == "build" and len(sys.argv) == 5 and sys.argv[3] == "--target":
        compiler.transpile_only(sys.argv[4])
    else:
        print("Invalid CLI command configuration.")

if __name__ == "__main__":
    cli()
          
