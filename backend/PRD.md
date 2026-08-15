# Backend Product Requirements Document
# Django OTP-Based User Login & Checkout API

## 1. Current Scope (MVP)

The MVP will implement:

### 1.1 User Registration
- **Endpoint**: `POST /api/users/register`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
- **Processing**:
  1. Validate email format and check uniqueness
  2. Create user with email as `USERNAME_FIELD`
  3. Generate 6-digit login code
  4. Hash code using bcrypt and store in database
  5. Return success response with user data and plain code for first-time display
- **Response**:
  ```json
  {
    "success": true,
    "user": {
      "id": 1,
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    },
    "code": "123456",
    "message": "Registration successful. 6-digit login code has been generated and stored securely."
  }
  ```

### 1.2 User Recognition
- **Endpoint**: `GET /api/users/recognize?email=xyz`
- **Processing**:
  1. Single database query to check email existence (optimization: `.first()` instead of `exists()` + `get()`)
  2. Return `registered: true/false` and user ID if registered
- **Response (Registered)**:
  ```json
  {
    "success": true,
    "user": { "id": 1 },
    "registered": true
  }
  ```
- **Response (Unregistered)**:
  ```json
  {
    "success": true,
    "registered": false
  }
  ```

### 1.3 OTP Verification
- **Endpoint**: `POST /api/auth/verify`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "code": "123456"
  }
  ```
- **Processing**:
  1. Validate email exists in database
  2. Compare provided code against bcrypt hash stored in DB
  3. Return authenticated user data on success
- **Success Response**:
  ```json
  {
    "success": true,
    "user": {
      "id": 1,
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe"
    }
  }
  ```
- **Failure Response**:
  ```json
  {
    "success": false,
    "message": "Invalid login code"
  }
  ```

### 1.4 Checkout System
- **Endpoint**: `POST /api/checkout/create`
- **Request Body** (Guest):
  ```json
  {
    "email": "guest@example.com",
    "phone": "9876543210",
    "shippingAddress": "123 Main Street"
  }
  ```
- **Request Body** (Authenticated): Same format, user associated
- **Processing**:
  1. Validate email format
  2. Check for existing checkout with idempotency key (if provided) for idempotent behavior
  3. Create checkout with `user_id = NULL` for guest or authenticated user ID
  3. Save to PostgreSQL database
- **Success Response**:
  ```json
  {
    "success": true,
    "message": "Checkout information saved successfully",
    "checkout_id": 1,
    "user_id": null,
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Idempotent Duplicate**:
  ```json
  {
    "success": true,
    "message": "Checkout information retrieved successfully (idempotent)",
    "checkout_id": 1,
    "user_id": null,
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```

### 1.5 Authentication Flow
- **Stateless**: No session/JWT management implemented
- **Login code**: Hashed bcrypt storage, displayed once during registration
- **Verification**: Code comparison against hash in DB

## 3. Future Scope (Post-MVP)
- Email ownership verification via RabbitMQ
- Verification tokens and email workers
- Resend verification emails
- Advanced analytics and monitoring

## 4. API Routes Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/register` | POST | User registration with code generation |
| `/api/users/recognize` | GET | Check if email is registered |
| `/api/auth/verify` | POST | OTP code verification |
| `/api/checkout/create` | POST | Checkout creation (authenticated/guest) |

## 5. Technical Stack
- **Framework**: Django 6.1 + Django REST Framework
- **Database**: PostgreSQL (local or Neon AWS)
- **Auth**: Bcrypt-hashed login codes (no JWT/session)
- **Env**: python-dotenv for configuration
- **Security**: Bcrypt hashing, UUID idempotency keys

## 5. Environment Configuration
The `.env` file should contain:
```
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=npg_0Ev1CchJSIjP
DB_HOST=ep-sweet-credit-a1aepsb3-pooler.ap-southeast-1.aws.neon.tech
DB_PORT=5432
DB_SSLMODE=require
SECRET_KEY=boltapp-hiring
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 6. Current Implementation Status

| Feature | Status |
|---------|--------|
| User registration with bcrypt-hashed codes | ✅ Complete |
| User recognition (single query optimization) | ✅ Complete |
| OTP verification with hash comparison | ✅ Complete |
| Checkout system (authenticated + guest) | ✅ Complete |
| Idempotency key support | ✅ Complete |
| JWT/session management | ❌ Removed (as requested) |
| PostgreSQL migration (idempotency_key) | ✅ Applied |

---

## 5. Development Prompt History

The project prompts used during development are documented in `prompt.md` with 13 sections covering:
- Initial Django setup and project scaffolding
- PRD analysis (32 sections)
- 8-phase execution planning
- Phase 2: User Model & Registration API enhancements (bcrypt, query optimization)
- Phase 3: Authentication & OTP Verification
- Phase 4: Checkout System implementation
- Idempotency support details
- Current project status and readiness for future phases