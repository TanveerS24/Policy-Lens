# Healthcare Policy Intelligence Platform - Implementation Guide

## Overview

This guide provides step-by-step instructions for completing the Healthcare Policy Intelligence Platform implementation.

## Project Status

### ✅ Completed
- Backend project structure and configuration
- Database models and schemas
- Authentication system (JWT + OTP)
- API route structure
- RAG service infrastructure
- Mobile app navigation and Redux store
- Authentication screens for mobile
- UI component library

### 🔄 In Progress
- Mobile screen implementations
- PDF processing pipeline
- LLM integration

### TODO
- Email service for OTP
- Advanced testing
- Deployment configuration
- Documentation completion

## Immediate Next Steps

### 1. Backend Setup (Prerequisite)

Before implementing features, ensure all dependencies are installed and services are running:

```bash
# Backend setup
cd backend
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Ensure MongoDB is running
mongod --dbpath ./data/db &

# Ensure Redis is running
redis-server &

# Start Ollama server
ollama serve &

# Verify models are pulled
ollama pull gemma3:4b-it-q4_K_M
ollama pull llama3.2:3b-instruct-q4_K_M

# Start the backend
python -m uvicorn app.main:app --reload
```

### 2. Complete PDF Processing Pipeline

**File**: `backend/app/services/pdf_service.py`

Enhance the PDF extraction to:
- Extract text with better chunking strategy (recursive character splitting)
- Preserve document structure
- Handle metadata extraction
- Generate embeddings

```python
# Example enhancement:
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text_recursive(text, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(text)
```

### 3. Integrate Ollama Services

**Files**:
- `backend/app/services/ollama_service.py`
- `backend/app/services/summary_service.py`
- `backend/app/services/eligibility_service.py`
- `backend/app/services/rag_service.py`

**Tasks**:
1. Test Ollama connectivity
2. Verify model outputs
3. Implement prompt engineering for better results
4. Add error handling for model timeouts

```python
# Test Ollama connection
async with OllamaClient() as client:
    ready = await client.check_model("gemma3:4b-it-q4_K_M")
    assert ready, "Gemma3 model not available"
```

### 4. Implement RAG Vector Store

**Files**:
- `backend/app/vector_store/` (create this directory)
- Update `backend/app/services/rag_service.py`

**Tasks**:
1. Generate embeddings for policy text chunks
2. Store in FAISS index
3. Implement similarity search
4. Cache embeddings in MongoDB

```python
# Create vector store wrapper
from faiss import IndexFlatL2
import pickle

class FAISSVectorStore:
    def __init__(self):
        self.index = IndexFlatL2(384)  # Vector dimension
        self.vectors = []
        self.metadata = []
    
    def add_vectors(self, vectors, metadata):
        # Add to index
        pass
    
    def search(self, query_vector, k=5):
        # Search similar vectors
        pass
```

### 5. Complete Upload Processing Pipeline

**File**: `backend/app/routers/upload_routes.py`

Implement the full flow:
1. Extract PDF text
2. Generate summary using Gemma3
3. Extract eligibility criteria
4. Create embeddings
5. Store in database

```python
@router.post("/pdf")
async def upload_pdf(file, authorization):
    # 1. Save file
    # 2. Extract text
    text = PDFExtractor.extract_text(file_path)
    
    # 3. Generate summary
    summary_service = SummaryService()
    summary = await summary_service.generate_summary(text)
    
    # 4. Extract eligibility
    eligibility = await summary_service.extract_eligibility_rules(text)
    
    # 5. Create embeddings
    chunks = PDFExtractor.chunk_text(text)
    embeddings = [embedder.embed(chunk) for chunk in chunks]
    
    # 6. Save to database
    upload_doc = {
        "text": text,
        "summary": summary,
        "eligibility": eligibility,
        "chunks": chunks,
        "embeddings": embeddings,
    }
    await db["uploads"].insert_one(upload_doc)
```

### 6. Email Service Implementation

**Create**: `backend/app/services/email_service.py`

```python
import smtplib
from email.mime.text import MIMEText

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
    
    async def send_otp(self, email: str, otp: str):
        # Build email
        message = f"""
        Your OTP for Healthcare Policy Platform: {otp}
        Valid for 10 minutes.
        """
        
        # Send using SMTP
        pass
```

### 7. Mobile Screen Implementation

Complete the placeholder screens:

**Priority Screens**:
1. `PoliciesScreen` - Browse and filter policies
2. `PolicyDetailsScreen` - Show policy details, eligibility check, Q&A
3. `UploadScreen` - PDF upload with progress
4. `MyUploadsScreen` - Manage user uploads
5. `ProfileScreen` - User profile and settings
6. `AdminDashboardScreen` - Admin statistics
7. `AdminUploadsScreen` - Review pending uploads

**Example Structure** (PoliciesScreen):

```javascript
export const PoliciesScreen = () => {
  const [filters, setFilters] = useState({});
  const dispatch = useDispatch();
  const { list, loading } = useSelector(state => state.policies);

  useEffect(() => {
    dispatch(fetchPolicies(filters));
  }, [filters]);

  return (
    <View>
      {/* Filter UI */}
      <FilterPanel />
      
      {/* Policy List */}
      <FlatList
        data={list}
        renderItem={PolicyCard}
        onEndReached={loadMore}
      />
    </View>
  );
};
```

### 8. Testing

**Backend Tests** - Create `backend/tests/`:

```python
# tests/test_auth.py
def test_user_registration():
    pass

def test_otp_verification():
    pass

def test_jwt_token_creation():
    pass

# tests/test_policies.py
def test_policy_creation():
    pass

def test_eligibility_check():
    pass
```

**Mobile Tests** - Create `mobile/__tests__/`:

```javascript
// __tests__/AuthStore.test.js
describe('Auth Store', () => {
  test('should handle login', () => {
    // Test login flow
  });
});
```

### 9. Database Migrations

**Create**: `backend/alembic/versions/001_initial.py`

If using SQL database later, configure Alembic migrations.

### 10. API Documentation

**Update Swagger/OpenAPI**:
- Add detailed descriptions
- Include example requests/responses
- Document error cases

```python
@router.post("/policies/check-eligibility/me")
async def check_eligibility(request: EligibilityCheckForMe):
    """
    Check if current user is eligible for policy
    
    Args:
        request: EligibilityCheckForMe with policy_id
    
    Returns:
        EligibilityResponse with eligibility result
    
    Raises:
        HTTPException: 401 if not authenticated, 404 if policy not found
    """
```

## Architecture Deep Dive

### Authentication Flow

```
User Registration
    ↓
Generate OTP → Send Email
    ↓
User Verifies OTP
    ↓
Create User in DB → Hash Password
    ↓
Generate JWT Tokens
    ↓
Return Access + Refresh Tokens
```

### Policy Upload and Approval Flow

```
User Uploads PDF
    ↓
Extract Text (PyMuPDF)
    ↓
Generate Summary (Gemma3)
    ↓
Extract Eligibility (Gemma3)
    ↓
Create Embeddings
    ↓
Store in Database (status: pending)
    ↓
Admin Reviews
    ↓
Admin Approves → Create Policy in DB
                → Notify User
    ↓
Policy Live
```

### RAG Pipeline

```
User Question
    ↓
Retrieve Relevant Chunks (FAISS)
    ↓
Build Context
    ↓
Call Llama3.2 with Context
    ↓
Generate Answer
    ↓
Return with Confidence Score
```

## Performance Considerations

### Database Optimization
- Ensure indexes on frequently queried fields
- Use connection pooling
- Implement query caching with Redis

### LLM Optimization
- Cache embeddings
- Batch process uploads
- Use smaller models for simple tasks
- Implement request queuing

### Mobile Optimization
- Lazy load screens
- Implement pagination
- Cache API responses
- Use image optimization

## Security Checklist

- [ ] Change JWT_SECRET in production
- [ ] Implement rate limiting on auth endpoints
- [ ] Add HTTPS/TLS
- [ ] Validate all user inputs
- [ ] Sanitize PDF uploads
- [ ] Use secure password hashing
- [ ] Implement CORS properly
- [ ] Add API key validation
- [ ] Audit logging

## Deployment Steps

### Docker Setup

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

### Environment Variables for Production

```
ENVIRONMENT=production
DEBUG=False
MONGO_URI=mongodb+srv://...
JWT_SECRET=<strong-random-key>
REDIS_URL=redis://...
OLLAMA_URL=http://ollama:11434
```

### Mobile Deployment

```bash
# Build Android
eas build --platform android

# Build iOS
eas build --platform ios

# Submit to stores
eas submit --platform android
eas submit --platform ios
```

## Troubleshooting

### Common Issues

1. **Ollama Model Not Found**
   - Solution: Run `ollama pull model_name`

2. **MongoDB Connection Timeout**
   - Solution: Check MongoDB is running, verify connection string

3. **Redis Connection Failed**
   - Solution: Check Redis server is running and accessible

4. **JWT Token Invalid**
   - Solution: Verify JWT_SECRET is consistent, check token expiry

5. **Mobile API Calls Failing**
   - Solution: Verify API_URL, check CORS configuration

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor (Async MongoDB)](https://motor.readthedocs.io/)
- [Ollama Documentation](https://ollama.ai)
- [React Native Documentation](https://reactnative.dev/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [LangChain Python](https://python.langchain.com/)

## Support & Questions

For implementation questions or issues:
1. Check the README.md for setup
2. Review test files for usage examples
3. Check API docs at `/api/docs`
4. Create GitHub issues for bugs

---

**Last Updated**: March 2026
