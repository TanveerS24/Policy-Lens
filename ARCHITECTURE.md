# System Architecture

## Overview

The Healthcare Policy Intelligence Platform is a full-stack application designed to help users understand and check eligibility for healthcare policies using AI and RAG (Retrieval Augmented Generation).

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     MOBILE APPLICATION                          │
│                    (React Native + Expo)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │Auth Screens  │  │Policy Browse │  │Upload Screen│          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                 │
│                            │                                     │
│              ┌─────────────▼─────────────┐                       │
│              │   Redux Store Management  │                       │
│              │  (Auth, Policies, Uploads)│                       │
│              └─────────────┬─────────────┘                       │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                    HTTP/JSON │ Axios
                             │
┌────────────────────────────▼─────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│                    (On port 8000)                                │
│  ┌──────────────────────────────────────────────────┐           │
│  │              FastAPI App (main.py)               │           │
│  │  ┌──────────────┐  ┌──────────────┐             │           │
│  │  │   Auth API   │  │ Policies API │             │           │
│  │  ├──────────────┤  ├──────────────┤             │           │
│  │  │- Register   │  │- List        │             │           │
│  │  │- OTP Verify │  │- Get Detail  │             │           │
│  │  │- Login      │  │- Search      │             │           │
│  │  │- Refresh    │  │- Ask Q&A     │             │           │
│  │  └──────────────┘  └──────────────┘             │           │
│  │  ┌──────────────┐  ┌──────────────┐             │           │
│  │  │ Uploads API  │  │  Admin API   │             │           │
│  │  ├──────────────┤  ├──────────────┤             │           │
│  │  │- Upload PDF  │  │- Create      │             │           │
│  │  │- Get My      │  │- Approve     │             │           │
│  │  │- Publish     │  │- Reject      │             │           │
│  │  │- Delete      │  │- Manage      │             │           │
│  │  └──────────────┘  └──────────────┘             │           │
│  └──────────┬───────────────────────────────────────┘           │
│             │                                                    │
│  ┌──────────▼──────────────────────────────────────┐           │
│  │           Services Layer                        │           │
│  │  ┌──────────────────────────────────────────┐  │           │
│  │  │ PDF Service          → Extract text      │  │           │
│  │  │ Summary Service      → Generate summary  │  │           │
│  │  │ Eligibility Service  → Check eligibility│  │           │
│  │  │ RAG Service          → Answer Q&A       │  │           │
│  │  │ Ollama Service       → LLM integration  │  │           │
│  │  │ Notification Service → Send updates     │  │           │
│  │  └──────────────────────────────────────────┘  │           │
│  │                    ▲                            │           │
│  │                    │                            │           │
│  │  ┌────────────────┴─────────────┐             │           │
│  │  │   Models & Data Management   │             │           │
│  │  │  ┌──────────────────────┐   │             │           │
│  │  │  │ Pydantic Schemas     │   │             │           │
│  │  │  │ Token Management     │   │             │           │
│  │  │  │ Password Hashing     │   │             │           │
│  │  │  └──────────────────────┘   │             │           │
│  │  └────────────────────────────┘             │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                  │
└──────────────────────┬───────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ MongoDB │  │  Redis  │  │ Ollama  │
   │ (Data)  │  │(Cache)  │  │ (LLM)   │
   └─────────┘  └─────────┘  └─────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                      FAISS
                 (Vector Index)
```

## System Components

### 1. Mobile Application (Frontend)

**Technology**: React Native + Expo

**Key Features**:
- Cross-platform (iOS/Android)
- Offline capability with AsyncStorage
- Redux for state management
- Bottom tab navigation
- Stack navigation for details

**Screens**:
- Authentication (Login, Register, OTP)
- Client (Home, Policies, Upload, MyUploads, Profile)
- Admin (Dashboard, Policies, Uploads)

**Redux Store**:
```
store/
├── authSlice - User auth state
├── policiesSlice - Policies and eligibility
└── uploadsSlice - User uploads
```

### 2. FastAPI Backend

**Technology**: FastAPI, Pydantic, Motor (Async MongoDB)

**Architecture**:
```
FastAPI
├── Routes (HTTP endpoints)
├── Services (Business logic)
├── Models (Data structures)
├── Schemas (Validation)
├── Database (MongoDB connection)
└── Utils (Helpers, security)
```

**Request Flow**:
```
HTTP Request
    ↓
Route Handler
    ↓
Validation (Pydantic Schema)
    ↓
Authentication Check (JWT)
    ↓
Service Layer (Business Logic)
    ↓
Database Query (Motor)
    ↓
Response
```

### 3. Database Layer

**MongoDB Collections**:
```
policy_lens/
├── users
│   ├── _id
│   ├── email (unique)
│   ├── password_hash
│   ├── name, age, gender, state
│   ├── role (admin/client)
│   └── timestamps
│
├── policies
│   ├── _id
│   ├── title (unique)
│   ├── summary, eligibility_criteria
│   ├── covered_benefits, important_notes
│   ├── category, state
│   ├── created_by (user_id)
│   ├── embeddings (vector array)
│   └── timestamps
│
├── uploads
│   ├── _id
│   ├── user_id
│   ├── pdf_path, pdf_filename
│   ├── summary, eligibility
│   ├── status (pending/approved/rejected)
│   ├── rejection_reason
│   └── timestamps
│
└── notifications
    ├── _id
    ├── user_id (or null for broadcast)
    ├── title, message, type
    ├── is_read
    └── created_at
```

### 4. AI/ML Services

#### PDF Service
- Extracts text from PDF using PyMuPDF
- Chunks text for better processing
- Preserves document structure
- Extracts metadata

#### Ollama Service
- Connects to local Ollama server
- Manages model selection
- Handles generation requests
- Error handling and timeouts

#### Summary Service
- Uses Gemma3 for summarization
- Generates:
  - Policy title and description
  - Comprehensive summary
  - Eligibility criteria extraction
  - Covered benefits list

#### Eligibility Service
- Uses Llama3.2 for reasoning
- Takes user profile and policy criteria
- Returns:
  - Eligibility decision (true/false)
  - Explanation
  - Missing requirements
  - Confidence score

#### RAG Service
- Implements Retrieval Augmented Generation
- Simple embeddings for text similarity
- Retrieves relevant policy chunks
- Uses Llama3.2 to answer questions based on context

### 5. Infrastructure Services

#### Redis
- OTP storage and expiry
- Session management
- Caching layer
- Rate limiting (future)

#### FAISS
- Vector database for embeddings
- Efficient similarity search
- In-memory for fast retrieval

#### Authentication
- JWT tokens (access + refresh)
- Bcrypt password hashing
- OTP verification
- Role-based access control

## Data Flows

### Authentication Flow

```
User Input (Email, Password)
    ↓
Register Endpoint
    ↓
Check email not duplicate
    ↓
Hash password
    ↓
Generate OTP
    ↓
Store in Redis with TTL
    ↓
Send OTP (Email)
    ↓
User Verifies OTP
    ↓
Create user in MongoDB
    ↓
Generate JWT tokens
    ↓
Return tokens
    ↓
Client stores tokens (AsyncStorage)
    ↓
Authenticated State
```

### Policy Upload and Processing

```
User Selects PDF
    ↓
POST /uploads/pdf
    ↓
Validate file type/size
    ↓
Save to server
    ↓
Extract text (PyMuPDF)
    ↓
Chunk text
    ↓
Generate summary (Gemma3)
    ↓
Extract eligibility (Gemma3)
    ↓
Create embeddings
    ↓
Store in MongoDB (status: pending)
    ↓
Admin Reviews
    ↓
Approve/Reject
    ↓
If Approved:
    - Create policy record
    - Index in FAISS
    - Send notification
    ↓
Policy Live
```

### Eligibility Check Flow

```
User Views Policy
    ↓
Click "Check Eligibility"
    ↓
Query user profile from DB
    ↓
GET policy details
    ↓
Call Eligibility Service
    ↓
Llama3.2 analyzes:
    - User profile (age, state, income, etc.)
    - Policy criteria (requirements, inclusions)
    ↓
Generate decision with reasoning
    ↓
Return result to user
    ↓
Display eligibility status
```

### Policy Question Answering (RAG)

```
User Types Question
    ↓
POST /policies/ask
    ↓
Retrieve policy chunks (FAISS)
    ↓
Get top 3 similar chunks
    ↓
Build prompt with context
    ↓
Call Llama3.2
    ↓
Generate answer based on context
    ↓
Return answer with confidence
    ↓
Display to user
```

## Security Architecture

### Authentication
- **Registration**: Email + password with OTP verification
- **Login**: Email/password authentication
- **Tokens**: JWT with separate access and refresh tokens
- **Token Expiry**: 
  - Access: 30 minutes
  - Refresh: 7 days

### Authorization
- **Role-Based Access Control (RBAC)**
  - Client: Limited to own data
  - Admin: Full system access

### Data Protection
- **In Transit**: HTTPS/TLS (in production)
- **At Rest**: Database credentials in .env
- **Password**: Bcrypt hashing (salt + rounds)

### Input Validation
- **Pydantic**: All API inputs validated
- **Type Checking**: Python type hints
- **PDF Validation**: File type and size checks

## Performance Considerations

### Database Optimization
- Indexed queries on email, policy title, user_id
- Connection pooling with Motor
- Pagination for list endpoints

### Caching Strategy
- Redis for OTP (with TTL)
- Client-side caching (AsyncStorage)
- Future: Response caching

### LLM Optimization
- Smaller models (3B-4B parameters)
- Prompt caching
- Batch processing for uploads

### Mobile Optimization
- Lazy loading screens
- Image lazy loading
- Network request batching
- Pagination on lists

## Scalability

### Horizontal Scaling
- Stateless backend (no session affinity)
- Load balancer in front
- Database replicas for read scaling

### Vertical Scaling
- Increase server resources
- Optimize queries
- Better caching

### Future Considerations
- Microservices architecture
- Message queues (Celery/RabbitMQ)
- Search engine (Elasticsearch)
- CDN for static assets

## Error Handling

### Backend
- HTTPException with proper status codes
- Try-catch blocks with logging
- Validation error messages
- Database error handling

### Mobile
- Network error detection
- Retry logic
- User-friendly error messages
- Fallback states

## Monitoring and Logging

### Backend Logging
- File and console handlers
- Different log levels
- Request/response logging
- Error stack traces

### Performance Monitoring
- Query execution time
- API response times
- Database connection pool stats

### Future
- Application Performance Monitoring (APM)
- Error tracking (Sentry)
- Analytics dashboard

## Deployment Architecture

### Development
- Local services (MongoDB, Redis, Ollama)
- Hot reload for backend
- Expo Go for mobile

### Production
- Docker containers
- Kubernetes orchestration (optional)
- Managed Databases (MongoDB Atlas, Redis Cloud)
- CDN for static files
- SSL certificates

---

**Architecture Version**: 1.0  
**Last Updated**: March 2026
