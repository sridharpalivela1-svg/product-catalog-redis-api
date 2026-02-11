# Product Catalog API with Redis Caching

High-performance backend API built using FastAPI, PostgreSQL, and Redis.

## 🚀 Features

- Product CRUD API
- Redis cache-aside pattern
- Cache hit / miss logic
- TTL-based cache expiration
- Automatic cache invalidation on update/delete
- Graceful fallback if Redis is unavailable
- Dockerized architecture
- Automated tests with pytest

---

## 🏗 Architecture

Client
   ↓
FastAPI Service
   ↓
Redis (Cache Layer)
   ↓
PostgreSQL (Primary Database)

---

## 🧠 Caching Strategy

Cache-Aside Pattern:

1. Check Redis first
2. If cache hit → return cached data
3. If cache miss → fetch from DB
4. Store in Redis with TTL
5. Return response

Cache invalidation occurs on:
- PUT /products/{id}
- DELETE /products/{id}

---

## ⚙️ Setup & Run

### 1️⃣ Clone repository

git clone https://github.com/sridharpalivela1-svg/product-catalog-redis-api
cd product-catalog-redis-api

### 2️⃣ Copy environment file

cp .env.example .env

### 3️⃣ Start services

docker-compose up --build

API will run on:

http://localhost:8080

Swagger docs:

http://localhost:8080/docs

---

## 🧪 Run Tests

docker-compose run api pytest

---

## 🐳 Docker

Services:
- FastAPI API
- PostgreSQL 15
- Redis 7

All services start using:

docker-compose up

---

## 📦 Tech Stack

- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy
- Docker
- Pytest

---

## 📈 Performance Benefits

- Reduced database load
- Faster response time for repeated requests
- Configurable TTL for freshness
- Safe fallback if cache fails

---

## 🎯 Production Readiness

- Multi-stage Docker build
- Environment variable configuration
- Proper HTTP status codes
- Input validation
- Error handling
- Automated tests
