# PolicyLens

PolicyLens is a full-stack platform for summarizing healthcare policies, extracting eligibility criteria, checking eligibility, and enabling AI-driven question answering. It includes:

- **Backend**: FastAPI service with MongoDB, Redis, and Ollama-powered RAG
- **Admin Dashboard**: React + Tailwind admin UI
- **Mobile**: Expo / React Native client with full policy browsing + eligibility + uploads

## 🧱 Architecture

- **FastAPI** backend with async MongoDB (Motor) and Redis
- **Ollama** powering summarization (Gemma3) and reasoning / Q&A (Llama 3.2)
- **RAG pipeline**: PDF → text extraction → chunking → embeddings → vector store (FAISS) → LLM
- **Docker Compose** orchestrates backend, MongoDB, Redis, Ollama, and Admin frontend

## 🚀 Quick Start (Docker)

1. Copy one of the pre-defined env files for the environment you want to run (development/test/production):

```bash
cp backend/.env.development backend/.env
```

> You can also use `backend/.env.test` or `backend/.env.production` depending on your workflow.

2. (Optional) For the admin dashboard and mobile client, copy their env templates as well:

```bash
cp admin-frontend/.env.example admin-frontend/.env
cp mobile/.env.example mobile/.env
```

> Both apps read their base API URL from env vars (`VITE_API_BASE_URL` and `EXPO_PUBLIC_API_BASE_URL`).

2. Start the stack:

```bash
docker-compose up --build
```

3. Access services:

- Backend API: `http://localhost:8000/api`
- OpenAPI docs: `http://localhost:8000/api/docs`
- Admin dashboard: `http://localhost:3000`
- Mobile (Expo): `http://localhost:19000` (use Expo Go or web)

## 🧠 LLM Setup

The backend uses Ollama. Ensure Ollama is running and models are installed:

```bash
ollama pull gemma3:4b-it-q4_K_M
ollama pull llama3.2:3b-instruct-q4_K_M
```

## 🗂️ Backend Structure

- `backend/app/main.py` — FastAPI app entrypoint
- `backend/app/routers/` — API routers
- `backend/app/services/` — business logic
- `backend/app/vector_store/` — FAISS vector search

## ✅ API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/verify-otp`
- `POST /api/auth/refresh`

### Policies
- `GET /api/policies`
- `GET /api/policies/{id}`
- `POST /api/policies/check-eligibility`
- `POST /api/policies/ask`

### Uploads
- `POST /api/uploads/pdf`
- `GET /api/uploads/my`
- `DELETE /api/uploads/{id}`
- `POST /api/uploads/publish`

### Admin
- `GET /api/admin/dashboard`
- `GET /api/admin/policies`
- `POST /api/admin/policy`
- `PUT /api/admin/policy/{id}`
- `DELETE /api/admin/policy/{id}`
- `GET /api/admin/pending`
- `POST /api/admin/approve/{id}`
- `POST /api/admin/reject/{id}`

## 🧩 Notes

- Admin endpoints require JWT auth with an admin user (set `is_admin` in MongoDB user doc).
- Uploading a PDF triggers extraction and summary generation; publishing creates a policy draft.
- Eligibility checks & QA rely on RAG with stored embeddings.

---

This repo provides the core backend + admin web UI for PolicyLens. Mobile clients can be added under `mobile/` as a separate Expo app.
