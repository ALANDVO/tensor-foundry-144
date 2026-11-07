# tensor-foundry-144

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


> Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote.

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173 and proxied to the backend at http://localhost:8000.

## Testing

### Backend tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend tests

```bash
cd frontend
npm test
```

### Frontend build

```bash
cd frontend
npm run build
```

## Features

- FastAPI backend with health check, config, and mode endpoints
- React frontend with Vite, TypeScript, and Vitest
- Mode selector (off, lite, standard, ultra)
- Configuration management with persistence
- CORS enabled for local development

Maintainer: Alan Vo <alanvo@gmail.com>

---

Alan Vo · [alanvo.net](https://alanvo.net)
