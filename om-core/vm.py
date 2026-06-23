# =====================================================================
# PRODUCTION MODULE: vm.py (BINARY VM EXECUTION ENGINE)
# =====================================================================
import struct
import json
import sys
from opcodes import OpCode

class OmBinaryVirtualMachine:
    def init(self, omb_filepath):
        self.filepath = omb_filepath
        self.stack = []
        self.registers = {}
        self.pc = 0
        self.bytecode = bytearray()
        self.constants = []
        
        self._load_binary_image()

    def _load_binary_image(self):
        """Parses low-level binary headers and populates virtual CPU memory."""
        with open(self.filepath, 'rb') as f:
            # Read the 6-byte header signature (2 bytes magic + 4 bytes length)
            header = f.read(6)
            if len(header) < 6:
                print("VM Error: Corrupted binary file header layout.")
                sys.exit(1)
                
            magic, constants_len = struct.unpack('2sI', header)
            if magic != b'OM':
                print("VM Error: Invalid binary execution image signature.")
                sys.exit(1)

            # Extract the constants pool block
            constants_data = f.read(constants_len)
            self.constants = json.loads(constants_data.decode('utf-8'))

            # The remainder of the file contains the raw, direct execution instructions
            self.bytecode = bytearray(f.read())

    def run(self):
        """Natively processes linear bytecode instructions at hardware speeds."""
        while self.pc < len(self.bytecode):
            op = self.bytecode[self.pc]
            
            if op == OpCode.HALT:
                break
            # ... (Keep your lightning fast VM execution stack switch logic here) ...
            
            self.pc += 1