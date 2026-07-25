# Policy Lens — Agent Rules & Project Standards

## Architecture

- **Backend**: FastAPI (Python 3.11+), SQLAlchemy ORM, PostgreSQL, Redis
- **Admin Dashboard**: React + Vite + TailwindCSS + TypeScript
- **Mobile App**: Expo SDK 55, React Native 0.83, Redux Toolkit
- **Infrastructure**: Docker Compose with health checks

## Project Layout

```
Policy-Lens/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # Versioned API endpoints
│   │   ├── config/         # Database, settings
│   │   ├── models/         # SQLAlchemy ORM models
│   │   └── services/       # Business logic (JWT, OTP, PDF)
│   ├── Dockerfile
│   └── requirements.txt
├── admin-frontend/          # React admin dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── stores/         # Zustand stores
│   │   └── services/       # API clients
│   ├── Dockerfile
│   └── package.json
├── mobile/                  # Expo mobile app
│   ├── src/
│   │   ├── screens/
│   │   ├── navigation/
│   │   ├── redux/          # Redux Toolkit slices
│   │   ├── services/       # API client
│   │   └── contexts/       # Auth, Theme
│   └── package.json
├── docker-compose.yaml
└── .env.example
```

## Coding Standards

### Python (Backend)
- Use `structlog` for all logging. Never use `print()`.
- Use `datetime.now(timezone.utc)` — never `datetime.utcnow()` (deprecated in 3.12).
- Use Pydantic v2 patterns: `@field_validator`, `model_config = {}` (not `class Config:`).
- Use `except Exception:` — never bare `except:`.
- Use `secrets` module for OTP/token generation — never `random`.
- Type-annotate all functions. Use `Generator[Session, None, None]` for `get_db()`.
- Do not log secrets, OTP codes, or tokens in any log level.

### TypeScript (Frontend/Mobile)
- Strict TypeScript: `noUnusedLocals`, `noUnusedParameters` enabled.
- Use `@/` alias for src imports.
- Mobile: Redux Toolkit for state, Zustand for admin frontend.

### Docker
- No `version:` key in docker-compose.yaml (deprecated).
- All services must have health checks.
- Use `depends_on: condition: service_healthy`.
- Use `npm ci` over `npm install` when lock file exists.

## Definition of Done

Before merging any change:
1. Backend imports resolve without errors
2. `python -m pytest` passes
3. `npx tsc --noEmit` passes for admin-frontend
4. `npx tsc --noEmit` passes for mobile
5. `docker compose build` succeeds
6. No bare except, no print(), no datetime.utcnow()
7. All environment variables documented in `.env.example`

## Testing

```bash
# Backend
cd backend && python -m pytest tests/ -v --cov=app

# Admin Frontend
cd admin-frontend && npx tsc --noEmit && npm run build

# Mobile
cd mobile && npx tsc --noEmit

# Docker
docker compose build --no-cache && docker compose up -d && docker compose ps
```
