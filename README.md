# Deliverease Crypto API

A production-ready REST API for cryptocurrency data built with FastAPI, featuring JWT authentication, comprehensive testing, and Docker support.

## Features

- ✅ **FastAPI Framework** - Modern, fast Python web framework
- ✅ **JWT Authentication** - Secure API endpoints with JWT tokens
- ✅ **CoinGecko Integration** - Real-time cryptocurrency market data
- ✅ **Multi-Currency Support** - INR, CAD, and USD pricing
- ✅ **Pagination** - Efficient data handling with configurable pagination
- ✅ **Comprehensive Testing** - 90% test coverage with 100+ tests (exceeds 80%+ requirement)
- ✅ **Docker Support** - Production and development Docker configurations
- ✅ **API Documentation** - Auto-generated Swagger/OpenAPI docs
- ✅ **Health Checks** - Service monitoring and health endpoints
- ✅ **Clean Architecture** - Well-organized, maintainable codebase
- ✅ **Environment Configuration** - Easy deployment with .env files

## Project Structure

```
deliverease_crypto_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_manager.py      # JWT token management
│   │   └── dependencies.py     # Authentication dependencies
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── coins.py            # Coins endpoints
│   │   ├── categories.py       # Categories endpoints
│   │   ├── health.py           # Health check endpoints
│   │   └── auth.py             # Authentication endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── coingecko_service.py    # CoinGecko API integration
│   │   └── health_service.py       # Health check service
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pagination.py       # Pagination utilities
│   │   ├── logger.py           # Logging configuration
│   │   └── http_client.py      # HTTP client wrapper
│   └── config/
│       ├── __init__.py
│       └── settings.py         # Configuration management
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_auth.py            # Authentication tests
│   ├── test_pagination.py      # Pagination tests
│   ├── test_config.py          # Configuration tests
│   ├── test_endpoints.py       # Endpoint tests
│   └── test_services.py        # Service tests
├── .env                        # Environment variables (git ignored)
├── .env.example               # Environment template
├── Dockerfile                 # Production Docker image
├── Dockerfile.dev             # Development Docker image
├── docker-compose.yml         # Production Docker Compose
├── docker-compose.dev.yml     # Development Docker Compose
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- pip or conda

### Local Development

1. **Clone the repository**
   ```bash
   cd deliverease_crypto_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set your JWT_SECRET_KEY and other settings
   ```

5. **Run the application**
   ```bash
   python app/main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Development

1. **Build and run with Docker Compose**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Access the development API**
   - API: http://localhost:8000

### Docker Production

1. **Build and deploy**
   ```bash
   docker-compose up --build -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f api
   ```

3. **Stop services**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Public Endpoints (No Authentication Required)

#### Health Check
```
GET /health
```
Returns application and service health status.

**Response:**
```json
{
  "status": "healthy",
  "app": {
    "name": "Deliverease Crypto API",
    "version": "1.0.0",
    "timestamp": "2024-01-01T12:00:00"
  },
  "services": {
    "coingecko": {
      "status": "healthy",
      "service": "CoinGecko API",
      "timestamp": "2024-01-01T12:00:00"
    }
  }
}
```

#### Version Info
```
GET /version
```
Returns API version information.

**Response:**
```json
{
  "app_name": "Deliverease Crypto API",
  "version": "1.0.0",
  "debug": false,
  "api_version": "v1",
  "documentation": "/docs"
}
```

#### Authentication Login
```
POST /v1/auth/login
```
Generate JWT token for API access.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Protected Endpoints (JWT Authentication Required)

#### List Coins
```
GET /v1/coins?page_num=1&per_page=10
```
List all cryptocurrency coins with pagination.

**Query Parameters:**
- `page_num` (integer, default: 1) - Page number
- `per_page` (integer, default: 10, max: 100) - Items per page
- `order` (string, default: "market_cap_desc") - Sort order

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "data": [
    {
      "id": "bitcoin",
      "name": "Bitcoin",
      "symbol": "BTC",
      "market_cap_rank": 1,
      "current_price": {
        "usd": 50000,
        "inr": 4150000,
        "cad": 67500
      },
      "market_cap": 1000000000000,
      "market_cap_change_24h": 5.2
    }
  ],
  "total": 12500,
  "page_num": 1,
  "per_page": 10,
  "total_pages": 1250
}
```

#### List Categories
```
GET /v1/categories
```
List all cryptocurrency categories.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "category_id": "decentralized-exchange",
    "name": "Decentralized Exchange",
    "market_cap_1h_change": -1.5,
    "market_cap_24h_change": 3.2,
    "market_cap_7d_change": 8.1,
    "market_cap": 45000000000
  }
]
```

#### Filter Coins
```
GET /v1/coins/filter?id=bitcoin
GET /v1/coins/filter?category=decentralized-exchange
```
Filter coins by ID or category.

**Query Parameters:**
- `id` (string) - Coin ID (e.g., "bitcoin", "ethereum")
- `category` (string) - Category ID (e.g., "decentralized-exchange")

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "bitcoin",
  "name": "Bitcoin",
  "symbol": "BTC",
  "description": {...},
  "market_data": {...},
  "links": {...}
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. **Obtain a Token**
   ```bash
   curl -X POST "http://localhost:8000/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123"}'
   ```

2. **Use the Token**
   ```bash
   curl -X GET "http://localhost:8000/v1/coins" \
     -H "Authorization: Bearer <token>"
   ```

## Configuration

Configuration is managed through environment variables in the `.env` file:

```env
# Application
APP_NAME=Deliverease Crypto API
APP_VERSION=1.0.0
DEBUG=False
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CoinGecko API
COINGECKO_API_URL=https://api.coingecko.com/api/v3
COINGECKO_API_KEY=  # Optional API key for higher rate limits

# Pagination
DEFAULT_PAGE_NUM=1
DEFAULT_PER_PAGE=10
MAX_PER_PAGE=100

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Health Check
HEALTH_CHECK_TIMEOUT=5
```

## Testing

Run the comprehensive test suite with 100+ tests achieving 90% coverage:

```bash
# Run all tests
pytest

# Run with coverage report (term + HTML)
pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v

# Run tests with verbose output
pytest -v

# Run with coverage and show missing lines
pytest --cov=app --cov-report=term-missing
```

### Test Coverage

| Module | Coverage | Status |
|--------|----------|--------|
| `app/routers/coins.py` | 100% | ✅ Perfect |
| `app/routers/categories.py` | 100% | ✅ Perfect |
| `app/routers/auth.py` | 100% | ✅ Perfect |
| `app/auth/jwt_manager.py` | 100% | ✅ Perfect |
| `app/utils/pagination.py` | 100% | ✅ Perfect |
| `app/services/health_service.py` | 96% | ✅ Excellent |
| `app/config/settings.py` | 97% | ✅ Excellent |
| `app/services/coingecko_service.py` | 80% | ✅ Good |
| `app/routers/health.py` | 84% | ✅ Good |
| **OVERALL** | **90%** | ✅ **Exceeds 80%+ Requirement** |

### Test Statistics

- **Total Tests:** 100+
- **Pass Rate:** 100%
- **Coverage:** 90% (341/377 statements)
- **Critical Endpoints:** 100% covered
- **Async Operations:** Fully mocked and tested
- **Error Handling:** All exception paths tested
- **Parameter Validation:** All boundary cases tested

### Coverage Report

Generate detailed HTML coverage report:

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

**Coverage:** The project achieves 90% test coverage across all modules, exceeding the 80%+ requirement.

## Development

### Code Quality

```bash
# Format code with Black
black app/ tests/

# Check linting with Flake8
flake8 app/ tests/

# Sort imports with isort
isort app/ tests/

# Type checking with mypy
mypy app/
```

### Running Development Server

```bash
# With hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Docker
docker-compose -f docker-compose.dev.yml up --build
```

## API Documentation

Once running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

## Deployment

### Production Docker

1. **Build the image**
   ```bash
   docker build -t deliverease-crypto-api:1.0.0 .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

3. **Verify health**
   ```bash
   curl http://localhost:8000/health
   ```

### Environment for Production

Update `.env` file with production settings:

```env
DEBUG=False
LOG_LEVEL=INFO
JWT_SECRET_KEY=<strong-random-key-min-32-chars>
COINGECKO_API_KEY=<your-api-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

## Error Handling

The API returns standard HTTP status codes and error messages:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common status codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Architecture

### Clean Architecture Principles

The project follows clean architecture with clear separation of concerns:

- **Routers** - HTTP endpoint handlers
- **Services** - Business logic and external API integration
- **Auth** - Authentication and JWT management
- **Utils** - Helper functions and pagination
- **Config** - Configuration management

### Design Patterns

- **Dependency Injection** - FastAPI's `Depends()`
- **Service Pattern** - Business logic encapsulation
- **Repository Pattern** - Data access abstraction
- **Middleware Pattern** - Authentication middleware
- **Singleton Pattern** - Configuration and logger instances

## Performance

- **Async/Await** - Non-blocking I/O operations
- **Pagination** - Efficient data retrieval
- **Caching** - Settings caching
- **Connection Pooling** - HTTP client pooling

## Security

- **JWT Authentication** - Secure token-based auth
- **CORS Configuration** - Cross-origin request control
- **Environment Variables** - Sensitive data management
- **Non-root Docker User** - Container security
- **Input Validation** - Request validation with Pydantic
- **HTTPS Ready** - Support for HTTPS deployment

## Monitoring

Health check endpoints for continuous monitoring:

```bash
# Check application health
curl http://localhost:8000/health

# Check version
curl http://localhost:8000/version
```

Docker health checks are configured with:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or .env
PORT=8001
```

### JWT Token Expired
Generate a new token:
```bash
curl -X POST "http://localhost:8000/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### CoinGecko API Rate Limits
- Free tier: 10-50 calls/minute
- Consider using a pro API key in production
- Set `COINGECKO_API_KEY` in `.env`

## Contributing

1. Follow PEP-8 style guide
2. Add tests for new features
3. Maintain 80%+ coverage
4. Update documentation
5. Use descriptive commit messages

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue or contact the development team.

## Changelog

### Version 1.0.0 (2024-01-01)
- Initial release
- JWT authentication
- CoinGecko integration
- Multi-currency support
- Comprehensive testing
- Docker deployment support
- Full API documentation
