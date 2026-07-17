# 🔤 OmLang Compiler

A complete compiler and runtime environment for the **OmLang** programming language, featuring both a command-line interface and a full-stack web application.

![Language: Python](https://img.shields.io/badge/Python-91.1%25-blue?style=flat)
![Language: JavaScript](https://img.shields.io/badge/JavaScript-8.1%25-yellow?style=flat)
![Docker Support](https://img.shields.io/badge/Docker-Supported-2496ED?style=flat)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Contributing](#contributing)

---

## Overview

OmLang Compiler is a full-stack application that compiles and executes OmLang source code. It includes:

- **om-core**: The core compiler and virtual machine (Python)
- **backend**: FastAPI-based REST service for compilation (Python)
- **frontend**: Modern Next.js web interface (JavaScript/React)

The project transforms a CLI compiler into a scalable web application with persistent history tracking.

---

## ✨ Features

- ✅ **Full Language Compiler** - Lexical analysis, parsing, and bytecode generation
- ✅ **Virtual Machine** - Execute compiled bytecode with runtime output capture
- ✅ **REST API** - FastAPI backend with /compile endpoint
- ✅ **Web Interface** - Clean, modern Next.js frontend
- ✅ **History Persistence** - Optional PostgreSQL integration via Neon
- ✅ **CORS Support** - Configurable cross-origin resource sharing
- ✅ **Docker Ready** - Container deployment support

---

## 📁 Project Structure

```
OmLang-Compiler/
├── om-core/                   # Core compiler and VM (Python)
│   ├── lexer.py              # Tokenization
│   ├── parser.py             # AST generation
│   ├── compiler.py           # Bytecode compilation
│   └── vm.py                 # Virtual machine execution
│
├── backend/                   # FastAPI backend (Python)
│   ├── main.py               # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── README.md             # Backend setup guide
│
├── frontend/                  # Next.js frontend (JavaScript)
│   ├── pages/
│   ├── components/
│   ├── package.json
│   └── README.md             # Frontend setup guide
│
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Quick Start

#### 1. **Backend Setup**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

#### 2. **Frontend Setup**

```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:3000`

#### 3. **Configure Environment**

In your browser, set the API URL to point to your backend:
- Local development: `http://localhost:8000`
- Production: Your backend deployment URL

---

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│   Next.js       │
│   Frontend      │──┐
└─────────────────┘  │
                     │ HTTP Request
                     ├─────────────────→ ┌──────────────────┐
                     │                   │  FastAPI Backend │
                     │                   │  /compile        │
                     │                   └────────┬─────────┘
                     │                            │
                     │                            │ Uses
                     │                            ▼
                     │                   ┌──────────────────┐
                     │                   │   om-core        │
                     │                   │ • Compiler       │
                     │                   │ • VM             │
                     │                   └────────┬─────────┘
                     │                            │
                     │                            │ Optionally
                     │                            ▼
                     │                   ┌──────────────────┐
                     │                   │  Neon Postgres   │
                     │                   │  (History)       │
                     │                   └──────────────────┘
                     │
  ◄──────────────────┘ HTTP Response
```

### Backend Components

| Component | Purpose |
|-----------|---------|
| **FastAPI** | Async HTTP framework for REST endpoints |
| **om-core** | Language compiler and bytecode VM |
| **asyncpg** | Async PostgreSQL driver for history tracking |
| **CORS Middleware** | Cross-origin request handling |

### Frontend Components

| Component | Purpose |
|-----------|---------|
| **Next.js Pages Router** | Lightweight routing and SSR |
| **React Components** | Interactive UI elements |
| **API Client** | Communicate with backend /compile |
| **Code Editor** | Source code input interface |

---

## 📦 Environment Variables

### Backend (`backend/.env`)

```env
# Database (optional)
NEON_DATABASE_URL=postgresql://user:pass@host/db

# CORS Configuration
ALLOW_ORIGINS=http://localhost:3000,https://yourdomain.com
```

If `ALLOW_ORIGINS` is not set, all origins are allowed (useful for development).

### Frontend (`frontend/.env.local`)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Important**: Only the backend should have database credentials. Never expose `NEON_DATABASE_URL` to the frontend.

---

## 🌐 Deployment

### Deploy Backend

**Option 1: Render.com**
1. Connect your GitHub repository
2. Create new Web Service pointing to `backend/` directory
3. Set environment variables (NEON_DATABASE_URL, ALLOW_ORIGINS)
4. Deploy

**Option 2: Railway.app**
1. Create new project from GitHub
2. Add PostgreSQL plugin
3. Set Python version in `Procfile`
4. Deploy

**Option 3: Fly.io**
```bash
fly launch --dockerfile Dockerfile
fly secrets set NEON_DATABASE_URL=...
fly deploy
```

**Option 4: Docker Locally**
```bash
docker build -t omlang-backend ./backend
docker run -p 8000:8000 \
  -e NEON_DATABASE_URL="..." \
  -e ALLOW_ORIGINS="..." \
  omlang-backend
```

### Deploy Frontend

**Vercel (Recommended)**
1. Import repository into Vercel
2. Set Root Directory to `frontend`
3. Set `NEXT_PUBLIC_API_URL` environment variable
4. Deploy

```bash
# Or deploy via CLI
npm i -g vercel
cd frontend
vercel --prod
```

---

## 📡 API Reference

### POST `/compile`

Compile and execute OmLang source code.

**Request:**
```json
{
  "source": "print('Hello, OmLang!')",
  "inputs": ["optional", "stdin", "inputs"]
}
```

**Response:**
```json
{
  "success": true,
  "bytecode": [...],
  "constants": [...],
  "runtime_output": "Hello, OmLang!\n",
  "errors": []
}
```

**Error Response:**
```json
{
  "success": false,
  "errors": ["Syntax error at line 1: unexpected token"],
  "runtime_output": ""
}
```

---

## 🛠️ Development Notes

### om-core Improvements

The core compiler is untouched to maintain compatibility. For future refactoring:
- Convert `init()` methods to `__init__()`
- Convert `repr()` to `__repr__()`
- Add type hints for better IDE support

### Database Integration

- Compile history is **optional** and requires a Neon PostgreSQL database
- History is automatically written after successful compilation
- Failed compilations are logged but don't block the response

### CORS Configuration

- **Development**: Leave `ALLOW_ORIGINS` empty to allow all origins
- **Production**: Explicitly list allowed frontend domains
- Example: `https://app.example.com,https://www.example.com`

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

---

## 📋 Roadmap

- [ ] Add unit tests for om-core
- [ ] Implement GitHub Actions for CI/CD
- [ ] Add syntax highlighting in web editor
- [ ] Export compilation history as JSON
- [ ] Performance optimizations for large programs
- [ ] Documentation for OmLang language spec

---

## 📄 License

This project is open source. Check the LICENSE file for details.

---

## 🆘 Support

For issues and questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and example code

---

## 👨‍💻 Author

**Kiran Mondal**  
[GitHub](https://github.com/Kiran-mondal) | [Repository](https://github.com/Kiran-mondal/OmLang-Compiler)

---

**Last Updated**: 2026  
**Status**: Active Development
