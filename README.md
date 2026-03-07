# Healthcare Policy Intelligence Platform

A production-ready AI-powered healthcare policy intelligence platform with FastAPI backend, MongoDB database, RAG architecture, local LLMs via Ollama, and React Native mobile application.

## Project Overview

This platform helps users understand healthcare policies using AI summarization and eligibility checking. The system supports both client and admin roles with distinct feature sets.

### Key Features

**For Clients:**
- Browse and search healthcare policies
- Check eligibility for policies
- Ask AI questions about policies
- Upload new policies for admin approval
- View personal profile and uploads

**For Admins:**
- Manage all policies (create, edit, delete)
- Review and approve/reject user uploads
- Monitor platform activity
- User management

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database with Motor async driver
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation using Python type hints
- **Redis**: For OTP and session management
- **JWT**: Authentication with access and refresh tokens
- **Ollama**: Local LLM inference
- **LangChain/LlamaIndex**: RAG framework
- **PyMuPDF**: PDF text extraction
- **FAISS**: Vector database for embeddings
- **bcrypt**: Password hashing

### Mobile
- **React Native + Expo**: Cross-platform mobile app
- **Redux Toolkit**: State management
- **React Navigation**: Navigation framework
- **Axios**: HTTP client
- **NativeWind**: Tailwind CSS for React Native

### LLM Models
- **Gemma 3 (4B)**: Policy summarization and eligibility extraction
- **Llama 3.2 (3B)**: Eligibility reasoning and Q&A

## Project Structure

```
PolicyLens/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   │   ├── settings.py
│   │   │   └── security.py
│   │   ├── database/
│   │   │   └── mongodb.py
│   │   ├── models/
│   │   │   └── database_models.py
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   ├── routers/
│   │   │   ├── auth_routes.py
│   │   │   ├── policy_routes.py
│   │   │   ├── upload_routes.py
│   │   │   ├── user_routes.py
│   │   │   └── admin_routes.py
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── ollama_service.py
│   │   │   ├── summary_service.py
│   │   │   ├── eligibility_service.py
│   │   │   ├── rag_service.py
│   │   │   └── notification_service.py
│   │   ├── utils/
│   │   │   ├── logger.py
│   │   │   ├── otp_service.py
│   │   │   └── token_service.py
│   │   └── vector_store/
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic/ (for migrations)
│
├── mobile/
│   ├── App.js
│   ├── app.json
│   ├── package.json
│   ├── src/
│   │   ├── store/
│   │   │   ├── index.js
│   │   │   ├── authSlice.js
│   │   │   ├── policiesSlice.js
│   │   │   └── uploadsSlice.js
│   │   ├── screens/
│   │   │   ├── auth/
│   │   │   │   ├── LoginScreen.js
│   │   │   │   ├── RegisterScreen.js
│   │   │   │   └── OTPVerificationScreen.js
│   │   │   ├── client/
│   │   │   │   ├── HomeScreen.js
│   │   │   │   ├── PoliciesScreen.js
│   │   │   │   ├── PolicyDetailsScreen.js
│   │   │   │   ├── UploadScreen.js
│   │   │   │   ├── MyUploadsScreen.js
│   │   │   │   └── ProfileScreen.js
│   │   │   └── admin/
│   │   │       ├── AdminDashboardScreen.js
│   │   │       ├── AdminPoliciesScreen.js
│   │   │       └── AdminUploadsScreen.js
│   │   ├── components/
│   │   │   └── ui/
│   │   │       └── index.js
│   │   ├── config/
│   │   │   └── api.js
│   │   └── utils/
│   ├── assets/
│   └── babel.config.js

└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- MongoDB running locally
- Redis running locally
- Ollama installed with models pulled
- Expo CLI (`npm install -g expo-cli`)

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create .env file from example:**
   ```bash
   cp .env.example .env
   ```

3. **Setup Ollama models:**
   ```bash
   ollama pull gemma3:4b-it-q4_K_M
   ollama pull llama3.2:3b-instruct-q4_K_M
   ```

4. **Start Ollama server:**
   ```bash
   ollama serve
   ```

5. **Start MongoDB (if not already running):**
   ```bash
   mongod
   ```

6. **Start Redis (if not already running):**
   ```bash
   redis-server
   ```

7. **Run the backend server:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000/api`
- API Documentation: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Mobile Setup

1. **Install dependencies:**
   ```bash
   cd mobile
   npm install
   ```

2. **Start Expo:**
   ```bash
   npm start
   ```

3. **Run on emulator or device:**
   - Press `a` for Android
   - Press `i` for iOS
   - Scan QR code with Expo Go app

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/verify-otp` - OTP verification and account creation
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### Policies
- `GET /policies` - List policies with filters
- `GET /policies/{id}` - Get policy details
- `POST /policies/check-eligibility/me` - Check eligibility for current user
- `POST /policies/check-eligibility/other` - Check eligibility for someone else
- `POST /policies/ask` - Ask AI question about policy

### Uploads
- `POST /uploads/pdf` - Upload policy PDF
- `GET /uploads/my` - Get user's uploads
- `DELETE /uploads/{id}` - Delete upload
- `POST /uploads/{id}/publish` - Publish upload for admin review

### Admin
- `POST /admin/policy` - Create policy
- `PUT /admin/policy/{id}` - Update policy
- `DELETE /admin/policy/{id}` - Delete policy
- `GET /admin/uploads/pending` - Get pending uploads
- `POST /admin/uploads/{id}/approve` - Approve upload
- `POST /admin/uploads/{id}/reject` - Reject upload

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `GET /users/notifications` - Get notifications

## Database Schema

### Collections

#### users
```json
{
  "_id": ObjectId,
  "name": String,
  "email": String (unique),
  "password_hash": String,
  "age": Integer,
  "gender": String,
  "state": String,
  "income": Integer,
  "role": "admin" | "client",
  "is_active": Boolean,
  "created_at": DateTime,
  "updated_at": DateTime
}
```

#### policies
```json
{
  "_id": ObjectId,
  "title": String (unique),
  "short_description": String,
  "summary": String,
  "eligibility_criteria": Object,
  "covered_benefits": [String],
  "important_notes": [String],
  "category": String,
  "state": String,
  "created_by": String (user_id),
  "embeddings": [Float],
  "is_active": Boolean,
  "created_at": DateTime,
  "updated_at": DateTime
}
```

#### uploads
```json
{
  "_id": ObjectId,
  "user_id": String,
  "pdf_path": String,
  "pdf_filename": String,
  "summary": String,
  "eligibility": Object,
  "status": "pending" | "approved" | "rejected",
  "rejection_reason": String,
  "created_at": DateTime,
  "approved_at": DateTime,
  "approved_by": String (user_id)
}
```

#### notifications
```json
{
  "_id": ObjectId,
  "user_id": String | null,
  "title": String,
  "message": String,
  "type": String,
  "is_read": Boolean,
  "created_at": DateTime
}
```

## Environment Variables

### Backend (.env)
```
# MongoDB
MONGO_URI=mongodb://localhost:27017/policy_lens
MONGO_DB_NAME=policy_lens

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_SUMMARIZATION_MODEL=gemma3:4b-it-q4_K_M
OLLAMA_REASONING_MODEL=llama3.2:3b-instruct-q4_K_M

# API
CORS_ORIGINS=["http://localhost:3000","http://localhost:8081","*"]
ENVIRONMENT=development
DEBUG=True

# File Upload
MAX_UPLOAD_SIZE=50000000
UPLOADS_DIR=./uploads
ALLOWED_EXTENSIONS=["pdf"]

# Logging
LOG_LEVEL=INFO
```

## Key Features Implementation

### 1. Policy Summarization
- Extract text from PDF using PyMuPDF
- Split into chunks for embedding
- Call Gemma3 to generate:
  - Title
  - Short description
  - Detailed summary
  - Eligibility criteria
  - Covered benefits
  - Important notes

### 2. Eligibility Checking
- Retrieve user profile from database
- Call Llama3.2 with user profile and policy criteria
- Get structured eligibility result:
  - Eligible: true/false
  - Reason: explanation
  - Missing requirements: list
  - Confidence score

### 3. RAG-based Q&A
- Retrieve relevant policy chunks using embeddings
- Send chunks + question to Llama3.2
- Generate context-aware answers
- Track confidence score

### 4. Authentication Flow
1. User registers with email and password
2. OTP sent to email (configurable)
3. User verifies OTP
4. Account created
5. JWT tokens issued (access + refresh)
6. Tokens stored in secure storage (mobile)

### 5. Admin Approval Workflow
1. User uploads PDF
2. System extracts and processes content
3. Admin reviews upload
4. Admin approves/rejects
5. If approved: Policy becomes public
6. Notification sent to user

## Security Considerations

- Passwords hashed with bcrypt
- JWT tokens with expiry
- OTP verification for registration
- Role-based access control (RBAC)
- HTTPS in production
- Secure storage on mobile (Keychain/Keystore)
- Input validation with Pydantic
- CORS configuration
- Rate limiting (future enhancement)

## Performance Optimizations

- Async database operations (Motor)
- Connection pooling
- Redis caching for OTP and sessions
- FAISS indexing for embeddings
- Lazy loading of policies
- Pagination support

## Error Handling

- Comprehensive exception handling
- Structured error responses
- Validation error messages
- Detailed logging
- User-friendly error messages on mobile

## Testing

### Backend Testing (Future)
```bash
pytest tests/
```

### Mobile Testing (Future)
```bash
npm test
```

## Deployment

### Backend Deployment
- Uses Docker for containerization
- Deploy to AWS EC2, GCP, or Azure
- Use managed MongoDB (Atlas) in production
- Use managed Redis (Redis Cloud) in production
- Environment-specific configurations

### Mobile Deployment
- Build for iOS: `eas build --platform ios`
- Build for Android: `eas build --platform android`
- Deploy to App Store and Google Play

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Start MongoDB
mongod --dbpath /path/to/db
```

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

### Ollama Model Issues
```bash
# Check available models
ollama list

# Pull models
ollama pull gemma3:4b-it-q4_K_M
ollama pull llama3.2:3b-instruct-q4_K_M
```

## Contributing

1. Create a feature branch
2. Follow code style guidelines
3. Test thoroughly
4. Create a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.

---

**Last Updated**: March 2026
