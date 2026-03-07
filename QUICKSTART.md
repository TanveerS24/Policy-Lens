# Quick Start Guide - Healthcare Policy Intelligence Platform

Get up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB
- Redis
- Ollama

## 1. Start Local Services (5 min)

### Terminal 1: MongoDB
```bash
mongod --dbpath ./data/db
```

### Terminal 2: Redis
```bash
redis-server
```

### Terminal 3: Ollama
```bash
ollama serve
# In another terminal, pull models:
ollama pull gemma3:4b-it-q4_K_M
ollama pull llama3.2:3b-instruct-q4_K_M
```

## 2. Backend Setup (3 min)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Start FastAPI server
python -m uvicorn app.main:app --reload
```

**Backend ready** at `http://localhost:8000`
- API docs: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 3. Mobile Setup (2 min)

```bash
cd mobile

# Install dependencies
npm install

# Start Expo
npm start

# Open in browser or scan QR code with Expo Go app
```

## 4. Test the System

### Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "Password123"
  }'
```

Response will include OTP (check server logs):
```
OTP for john@example.com: 123456
```

### Verify OTP

```bash
curl -X POST http://localhost:8000/api/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user_id": "...",
  "email": "john@example.com",
  "role": "client"
}
```

### Get Policies

```bash
curl -X GET http://localhost:8000/api/policies \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 5. Key Endpoints

### Authentication
- `POST /auth/register` - Register user, sends OTP
- `POST /auth/verify-otp` - Verify OTP and create account
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh access token

### Policies
- `GET /policies` - List all policies
- `GET /policies/{id}` - Get policy details
- `POST /policies/check-eligibility/me` - Check if user is eligible
- `POST /policies/ask` - Ask AI question about policy

### Uploads
- `POST /uploads/pdf` - Upload policy PDF
- `GET /uploads/my` - Get user's uploads
- `POST /uploads/{id}/publish` - Request admin approval

### Admin
- `POST /admin/policy` - Create new policy
- `GET /admin/uploads/pending` - Get pending uploads
- `POST /admin/uploads/{id}/approve` - Approve upload
- `POST /admin/uploads/{id}/reject` - Reject upload

## 6. Sample Data

### Create a Test Policy

```bash
curl -X POST http://localhost:8000/api/admin/policy \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Citizens Health Insurance",
    "short_description": "Comprehensive health coverage for seniors",
    "summary": "This policy provides comprehensive health insurance coverage for citizens aged 60 and above with subsidized premiums.",
    "eligibility_criteria": {
      "minimum_age": 60,
      "maximum_age": 100,
      "income_requirement": "No income limit"
    },
    "covered_benefits": ["Hospitalization", "Surgery", "Medicines", "Diagnostic tests"],
    "important_notes": ["30-day waiting period for non-emergency procedures"],
    "category": "Senior Citizen",
    "state": "Tamil Nadu"
  }'
```

## 7. File Structure

```
PolicyLens/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Entry point
│   │   ├── config/            # Settings & security
│   │   ├── database/          # MongoDB connection
│   │   ├── models/            # Data models
│   │   ├── schemas/           # API schemas
│   │   ├── routers/           # API routes
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utilities
│   │   └── vector_store/      # FAISS storage
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── mobile/                     # React Native app
│   ├── App.js                 # Entry point
│   ├── app.json               # Expo config
│   ├── src/
│   │   ├── screens/           # App screens
│   │   ├── components/        # Reusable components
│   │   ├── store/             # Redux store
│   │   ├── config/            # Configuration
│   │   └── utils/             # Utilities
│   └── package.json           # Dependencies
│
└── README.md                  # Full documentation
```

## 8. Common Commands

### Backend Development

```bash
# Run with auto-reload
python -m uvicorn app.main:app --reload

# Run with specific host/port
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest tests/

# Generate documentation
python -m pydoc -w app
```

### Mobile Development

```bash
# Start development server
npm start

# Clear cache and restart
npm start -- -c

# Install dependencies
npm install

# Format code
npm run format

# Lint code
npm run lint
```

### Database

```bash
# Connect to MongoDB
mongosh

# View databases
show dbs

# Use database
use policy_lens

# View collections
show collections

# Query data
db.policies.find()
db.users.find()
```

### Redis

```bash
# Connect
redis-cli

# Check connection
ping

# View keys
KEYS *

# Get value
GET key_name
```

## 9. Troubleshooting

### MongoDB Connection Failed
```bash
# Start MongoDB if not running
mongod --dbpath ./data/db

# Or check if process exists
ps aux | grep mongod
```

### Redis Connection Failed
```bash
# Start Redis if not running
redis-server

# Check status
redis-cli ping
```

### Ollama Models Not Found
```bash
# Pull models
ollama pull gemma3:4b-it-q4_K_M
ollama pull llama3.2:3b-instruct-q4_K_M

# List available models
ollama list
```

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### API Calls Failing from Mobile
- Check if backend is running: `http://localhost:8000/api/health`
- Verify API_URL in mobile config matches backend URL
- Check CORS configuration in backend settings
- Ensure both are on same network

## 10. Next Steps

### For Backend Development
1. Implement email service for OTP sending
2. Add PDF processing pipeline
3. Implement vector embeddings
4. Add comprehensive error handling
5. Write unit tests

### For Mobile Development
1. Implement all screen components
2. Add form validation
3. Implement image handling
4. Add offline capability with AsyncStorage
5. Write mobile tests

### For Deployment
1. Setup Docker containers
2. Configure CI/CD pipeline
3. Deploy to cloud (AWS/GCP/Azure)
4. Setup monitoring and logging
5. Configure SSL/TLS certificates

## 11. Documentation

- **README.md** - Full project documentation
- **IMPLEMENTATION_GUIDE.md** - Detailed implementation steps
- **API Docs** - Available at `/api/docs` when backend is running
- **Code Comments** - Inline documentation throughout codebase

## 12. Additional Resources

- FastAPI: https://fastapi.tiangolo.com/
- React Native: https://reactnative.dev/
- Redux Toolkit: https://redux-toolkit.js.org/
- MongoDB: https://docs.mongodb.com/
- Ollama: https://ollama.ai/

## 13. Key Contacts

For issues, questions, or support:
- Create GitHub issues
- Check existing documentation
- Review code comments
- Run tests for examples

---

**That's it!** You now have:
✅ Backend API running on port 8000  
✅ MongoDB storing data  
✅ Redis for caching  
✅ Ollama LLMs available  
✅ Mobile app ready to connect  

Start building! 🚀
