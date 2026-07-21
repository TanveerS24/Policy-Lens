  # DentalSchemes India

  A mobile-first + web admin platform for aggregating dental health schemes across India.

  ## Features

  - **Scheme Aggregation**: Browse and search dental health schemes (state + national)
  - **Eligibility Checking**: AI-powered eligibility engine with rule-based checking
  - **Document Upload**: Upload policy documents (PDF, images) for AI analysis
  - **AI Summarization**: Get AI-generated summaries of policy coverage, exclusions, waiting periods
  - **Authentication**: Secure JWT-based authentication with OTP verification
  - **Admin Panel**: Full-featured admin dashboard for managing schemes and users
  - **Role-Based Access Control**: Three admin levels (super_admin, content_admin, support_admin)
  - **Admin Management**: Super admins can create, manage, and delete other admin accounts
  - **Token Auto-Refresh**: Automatic access token refresh before expiry

  ## Architecture

  ### Backend (FastAPI + Python)
  - REST API with JWT authentication (HS256)
  - Role-based access control (RBAC) for admin endpoints
  - Token refresh mechanism with automatic renewal
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
  # Copy environment file
  cp .env.example .env

  # Start all services
  docker-compose up -d

  # Create initial super admin (first time only)
  docker exec -it dentalschemes-backend python scripts/create_super_admin.py --email "admin@dentalschemes.in" --password "admin123" --name "Super Admin"

  # View logs
  docker-compose logs -f

  # Stop services
  docker-compose down
  ```

  ### Access the Application
  - **Admin Panel**: http://localhost:5173
  - **Backend API**: http://localhost:8000/api/v1
  - **API Documentation**: http://localhost:8000/docs

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

  ### Authentication (Public)
  - `POST /api/v1/auth/request-otp` - Request OTP
  - `POST /api/v1/auth/verify-otp` - Verify OTP
  - `POST /api/v1/auth/register` - Register user
  - `POST /api/v1/auth/login` - Login
  - `POST /api/v1/auth/refresh` - Refresh token

  ### Schemes (Public)
  - `GET /api/v1/schemes` - List schemes
  - `GET /api/v1/schemes/:id` - Get scheme details
  - `POST /api/v1/schemes/:id/eligibility` - Check eligibility

  ### Documents (Authenticated)
  - `GET /api/v1/documents` - List documents
  - `POST /api/v1/documents/upload` - Upload document
  - `GET /api/v1/documents/:id/summary` - Get AI summary

  ### Admin (Requires Admin Authentication)

  #### Authentication
  - `POST /api/v1/admin/login` - Admin login
  - `POST /api/v1/admin/refresh` - Refresh access token

  #### Dashboard & Analytics
  - `GET /api/v1/admin/dashboard` - Dashboard stats

  #### Scheme Management (super_admin, content_admin)
  - `GET /api/v1/admin/schemes` - List all schemes
  - `POST /api/v1/admin/schemes` - Create new scheme
  - `PUT /api/v1/admin/schemes/:id` - Update scheme
  - `DELETE /api/v1/admin/schemes/:id` - Delete scheme

  #### User Management (super_admin, support_admin)
  - `GET /api/v1/admin/users` - List users
  - `GET /api/v1/admin/users/:id` - Get user details

  #### Admin Management (super_admin only)
  - `GET /api/v1/admin/admins` - List all admins
  - `POST /api/v1/admin/admins` - Create new admin
  - `DELETE /api/v1/admin/admins/:id` - Delete admin account
  - `DELETE /api/v1/admin/me` - Delete own account

  #### Audit Logs (super_admin, support_admin)
  - `GET /api/v1/admin/audit-logs` - View audit logs

  ## Admin Roles & Permissions

  | Role | Description | Permissions |
  |------|-------------|-------------|
  | **super_admin** | Full system access | Can create/manage other admins, manage all schemes, view audit logs, manage users |
  | **content_admin** | Content management | Can create, edit, and delete schemes. Cannot manage admins or users |
  | **support_admin** | User support | Can view users and audit logs. Cannot manage schemes or admins |

  ### Default Super Admin
  The first admin must be created using the provided script:
  ```bash
  docker exec -it dentalschemes-backend python scripts/create_super_admin.py \
    --email "admin@example.com" \
    --password "securepassword123" \
    --name "Super Admin"
  ```

  **Note**: This script can only be run when no admins exist in the database.

  ## Environment Variables

  ### Backend (.env)
  ```
  # Database
  DATABASE_URL=postgresql://postgres:postgres@localhost:5432/dentalschemes
  REDIS_URL=redis://localhost:6379/0

  # JWT Configuration
  JWT_SECRET_KEY=your-secret-key-change-in-production
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=60
  REFRESH_TOKEN_EXPIRE_DAYS=30

  # API Keys (Optional)
  ANTHROPIC_API_KEY=your-anthropic-key
  SMS_API_KEY=your-sms-api-key

  # Security
  DEBUG=false
  MAX_LOGIN_ATTEMPTS=5
  LOCKOUT_DURATION_MINUTES=30
  ```

  ### Admin Frontend (.env)
  ```
  VITE_API_URL=http://localhost:8000/api/v1
  VITE_TOKEN_REFRESH_INTERVAL=300000
  ```

  ### Mobile (.env)
  ```
  EXPO_PUBLIC_API_URL=https://api.dentalschemes.in/api/v1
  ```

  ## Contributing

  1. Fork the repository
  2. Create a feature branch
  3. Make your changes
  4. Submit a pull request

  ## License

  MIT License - see LICENSE file for details
