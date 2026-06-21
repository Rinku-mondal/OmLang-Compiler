# 🕉️ OMlang-Compiler

**OMlang-Compiler** is a powerful, minimalist, and culturally-inspired programming language compiler engine. It converts simple English instructions into optimized runtime logic. This core compiler runs flawlessly as a Cross-Platform Command Line Interface (CLI) across Windows CMD, Linux Bash, macOS Terminal, and Android Termux.

## 🚀 Core Features
- **Identity Banner:** Displays a stylized initialization header on runtime boot.
- **Cross-Compilation:** Instantly transpile your Om code down into clean, native Python scripts.
- **Clean Block Syntax:** Uses an elegant, brackets-free `end` layout inspired by Ruby.
- **Global CLI Support:** Install it once and use the native `om` terminal tool from any directory.

---

## 🛠️ Cross-Platform Installation & Setup

Anyone downloading this repository from GitHub can install the compiler globally as a system CLI command using the following native steps:

### Step 1: Clone the Repository
```bash
git clone https://github.com/Kiran-mondal/OMlang-Compiler.git
cd OMlang-Compiler
pip install -e .
om run workspace.om
om build workspace.om --target python
```
```ruby
# Variable Management
set power = 108
set multiplier = 2

# Calculations
set total = power * multiplier

# Conditional Scopes
if total > 200
    show total
else
    show 0
end

# Loops / Iterators
repeat 3
    show 7
end
```
---

### 💡 What Else Do You Need to Make This Work?
For the `pip install -e .` command to magically set up the `om` command inside Windows CMD, Linux, or Termux, you just need to make sure the **`setup.py`** file we discussed earlier is also uploaded to your `OMlang-Compiler` repository. 

Here is the exact `setup.py` layout to keep in your directory:

```python
from setuptools import setup

setup(
    name="om-lang",
    version="1.2.0",
    py_modules=["om"],
    entry_points={
        'console_scripts': [
            'om=om:cli',
        ],
    },
)
