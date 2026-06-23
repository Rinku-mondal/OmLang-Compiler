# =====================================================================
# MODULE: main.py (PRODUCTION CLI ENGINE DRIVER)
# =====================================================================
import sys
import os

from opcodes import OpCode
from lexer import OmLexer, TokenType
from parser import OmParser
from compiler import OmBytecodeCompiler
from vm import OmVirtualMachine

def execute_file_pipeline(filepath):
    if not os.path.exists(filepath):
        print(f"System Error: File target location '{filepath}' could not be resolved.")
        sys.exit(1)
    if not filepath.endswith('.om') and not filepath.endswith('.omb'):
        print("System Error: The Om engine only executes native '.om' or compiled '.omb' files.")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"System Error: Unable to read file content safely. Details: {e}")
        sys.exit(1)

    lexer = OmLexer(source_code)
    parser = OmParser(lexer)
    ast = parser.parse()

    compiler = OmBytecodeCompiler()
    bytecode, constants = compiler.compile(ast)

    vm = OmVirtualMachine(bytecode, constants)
    vm.run()

def show_help_menu():
    print("==================================================")
    print("          The Om Language Standalone CLI          ")
    print("==================================================")
    print("Usage Rules:")
    print("  om run <filename.om>   | Compiles and runs a script file")
    print("  om version             | Displays system version data")
    print("==================================================")

# This is the function pip hooks into directly
def main_entry():
    if len(sys.argv) < 2:
        show_help_menu()
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "version":
        print("Om Language Compiler Environment: Standalone-v4.0.0-Bytecode-VM")
    elif command == "run":
        if len(sys.argv) < 3:
            print("CLI Error: Missing file target. Syntax target: om run <filename.om>")
            sys.exit(1)
        target_file = sys.argv[2]
        execute_file_pipeline(target_file)
    else:
        print(f"CLI Error: Unknown operation token '{command}' entered.")
        show_help_menu()

# Allows running via python main.py directly as well
if name == "main":
    main_entry()