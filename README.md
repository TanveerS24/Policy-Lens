# DentalSchemes India

A mobile-first + web admin platform for aggregating dental health schemes across India.

## Features

- **Scheme Aggregation**: Browse and search dental health schemes (state + national)
- **Eligibility Checking**: AI-powered eligibility engine with rule-based checking
- **Document Upload**: Upload policy documents (PDF, images) for AI analysis
- **AI Summarization**: Get AI-generated summaries of policy coverage, exclusions, waiting periods
- **Authentication**: Secure JWT-based authentication with OTP verification
- **Admin Panel**: Full-featured admin dashboard for managing schemes and users

## Architecture

### Backend (FastAPI + Python)
- REST API with JWT authentication (RS256)
- PostgreSQL database with SQLAlchemy ORM
- Redis for caching and session management
- AI integration (Claude/OpenAI) for document summarization

### Mobile App (React Native + Expo)
- Cross-platform mobile app (iOS/Android)
- Redux for state management
- React Native Paper for UI components
- File upload and camera integration

### Admin Frontend (React + TypeScript)
- Modern React with TypeScript
- TanStack Query for data fetching
- Zustand for state management
- Tailwind CSS for styling
- Lucide icons

## Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/      # API endpoints
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── config/      # Configuration
│   └── requirements.txt
├── mobile/               # React Native mobile app
│   ├── src/
│   │   ├── screens/     # App screens
│   │   ├── navigation/ # Navigation setup
│   │   ├── redux/       # State management
│   │   └── services/    # API services
│   └── package.json
├── admin-frontend/       # React admin panel
│   ├── src/
│   │   ├── pages/       # Admin pages
│   │   ├── components/  # Shared components
│   │   └── stores/      # State stores
│   └── package.json
└── docker-compose.yaml
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Using Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Mobile Development

```bash
cd mobile

# Install dependencies
npm install

# Start Expo
npx expo start
```

### Admin Frontend Development

```bash
cd admin-frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/request-otp` - Request OTP
- `POST /api/v1/auth/verify-otp` - Verify OTP
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Schemes
- `GET /api/v1/schemes` - List schemes
- `GET /api/v1/schemes/:id` - Get scheme details
- `POST /api/v1/schemes/:id/eligibility` - Check eligibility

### Documents
- `GET /api/v1/documents` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/:id/summary` - Get AI summary

### Admin
- `POST /api/v1/admin/login` - Admin login
- `GET /api/v1/admin/dashboard` - Dashboard stats
- `GET /api/v1/admin/schemes` - Manage schemes
- `GET /api/v1/admin/users` - Manage users
- `GET /api/v1/admin/audit-logs` - View audit logs

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dentalschemes
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=your-anthropic-key
SMS_API_KEY=your-sms-api-key
```

### Admin Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
