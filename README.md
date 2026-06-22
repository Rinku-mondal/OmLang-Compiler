#                 🕉️ OmLang-Compiler
  ![OMlang Version](https://img.shields.io/badge/version-v2.0.0--Master-blue.svg?style=flat-square)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-FFD43B.svg?style=flat-square&logo=python&logoColor=blue)
![Supported OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux%20%7C%20Termux-blueviolet.svg?style=flat-square)
![Terminal Support](https://img.shields.io/badge/Terminal-CMD%20%7C%20PowerShell%20%7C%20Bash-lightgrey.svg?style=flat-square&logo=gnometerminal)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-success.svg?style=flat-square)

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
git clone https://github.com/Kiran-mondal/OmLang-Compiler.git
cd OmLang-Compiler
pip install -e .
```
## 🚀 Om Language Syntax & Function Guide
To keep the Om language completely simple and clean, the following keywords and built-in functions are used:
### 1. Core Keywords
| Keyword | Description | Example |
|---|---|---|
| **show** | Used to display any text or output on the screen (Signature Feature). | show "Hello, World!" 
 show total |
| **input** | Used to take dynamic input from the user in the terminal. | age = input("Enter age: ") |
| **if** | Used to start a conditional block. | if score >= 80 |
| **else** | Used to run alternative code if the condition is false. | else |
| **repeat** | Used to loop or repeat code a specific number of times. | repeat 5 |
| **end** | Used to terminate any conditional block (if-else) or loop (repeat). | end |
### 2. Smart Built-in Functions
Our language directly supports these useful Python functions in the backend:
 * **len(variable)** : Used to find the total number of characters or length of a text.
   * *Example:* show len("Om") (will show output 2)
 * **round(variable)** : Used to round a decimal number to its nearest integer.
   * *Example:* show round(10.6) (will show output 11)
 * **abs(variable)** : Used to convert any negative number into a positive number (Absolute Value).
   * *Example:* show abs(-5) (will show output 5)
 * **str(), int(), float()** : Used to explicitly change data types (Type Casting) when needed.
### 3. Mathematical & Logical Symbols (Operators)
 * **Math Operators:** + (Addition), - (Subtraction), * (Multiplication), / (Division).
 * **Logical Operators:** == (Equal to), != (Not equal to), >, <, >=, <=.

