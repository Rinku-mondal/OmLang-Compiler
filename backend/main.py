import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from io import StringIO
from contextlib import redirect_stdout
import builtins
import asyncpg

# Make om-core importable
ROOT = os.path.dirname(os.path.dirname(__file__))
OMCORE = os.path.join(ROOT, "om-core")
if os.path.isdir(OMCORE):
    sys.path.insert(0, os.path.abspath(OMCORE))
else:
    # fallback: repo root
    sys.path.insert(0, os.path.abspath(ROOT))

# Import om-core modules
from lexer import OmLexer  # type: ignore
from parser import OmParser  # type: ignore
from compiler import OmBytecodeCompiler  # type: ignore
from vm import OmVirtualMachine  # type: ignore

app = FastAPI()

# CORS
allow_origins = os.getenv("ALLOW_ORIGINS")
if allow_origins:
    origins = [o.strip() for o in allow_origins.split(",") if o.strip()]
else:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NEON_DSN = os.getenv("NEON_DATABASE_URL")
db_pool: Optional[asyncpg.pool.Pool] = None

@app.on_event("startup")
async def startup():
    global db_pool
    if NEON_DSN:
        db_pool = await asyncpg.create_pool(dsn=NEON_DSN, min_size=1, max_size=10)

@app.on_event("shutdown")
async def shutdown():
    global db_pool
    if db_pool:
        await db_pool.close()

class CompileRequest(BaseModel):
    source: str
    inputs: Optional[List[str]] = []

class CompileResponse(BaseModel):
    success: bool
    bytecode: Optional[list] = None
    constants: Optional[list] = None
    runtime_output: Optional[str] = None
    errors: Optional[str] = None


def run_vm_capture(vm: OmVirtualMachine, inputs: List[str]):
    # Provide inputs via overriding builtins.input and capture stdout
    input_iter = iter(inputs or [])
    orig_input = builtins.input
    builtins.input = lambda prompt="": next(input_iter)
    buf = StringIO()
    try:
        with redirect_stdout(buf):
            vm.run()
    except StopIteration:
        # Not enough inputs provided
        pass
    finally:
        builtins.input = orig_input
    return buf.getvalue()

@app.post("/compile", response_model=CompileResponse)
async def compile_endpoint(req: CompileRequest):
    try:
        # Build AST
        lexer = OmLexer()
        lexer.init(req.source)
        parser = OmParser()
        parser.init(lexer)
        ast = parser.parse()

        # Compile
        compiler = OmBytecodeCompiler()
        compiler.init()
        bytecode, constants = compiler.compile(ast)

        # Run VM and capture output
        vm = OmVirtualMachine()
        vm.init(bytecode, constants)
        runtime_out = run_vm_capture(vm, req.inputs or [])

        # Persist history (optional)
        if db_pool is not None:
            async with db_pool.acquire() as conn:
                try:
                    await conn.execute(
                        "CREATE TABLE IF NOT EXISTS compile_history (id SERIAL PRIMARY KEY, source TEXT, bytecode TEXT, constants TEXT, runtime_output TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT now())"
                    )
                    await conn.execute(
                        "INSERT INTO compile_history (source, bytecode, constants, runtime_output) VALUES ($1,$2,$3,$4)",
                        req.source, repr(bytecode), repr(constants), runtime_out
                    )
                except Exception:
                    # Don't fail compile if DB write fails
                    pass

        return CompileResponse(success=True, bytecode=bytecode, constants=constants, runtime_output=runtime_out)
    except Exception as e:
        return CompileResponse(success=False, errors=str(e))
