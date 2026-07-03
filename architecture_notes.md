# ContextOS Project — Architecture Notes
Last updated: June 29, 2026

## Current Status
Backend is stable. Frontend needs Redis bug fix before Friday.

## WHERE I LEFT OFF (Last Session)
- Was debugging the OAuth2 timeout in auth.py
- Got to line 87 — the callback handler needs a timeout increase
- Also started looking at Redis connection pooling in database.js
- DID NOT finish the circuit breaker implementation
- Next immediate task: Fix Redis concurrent connection bug

## Key Decisions Made

### Redis over PostgreSQL for caching
- PostgreSQL: 400ms average read latency
- Redis: Under 15ms average read latency  
- Decision is final. Do not revisit.

### OAuth2 over JWT for authentication
- JWT caused stale sessions and had no revocation support
- OAuth2 migration completed June 20
- Token refresh endpoint still has the 30s timeout bug

### MongoDB for user preferences
- SQL schema changes were blocking deployments
- MongoDB gives flexibility for rapidly changing preference schema
- Implementation is pending

## Open Bugs (Priority Order)
1. CRITICAL: Redis drops connections above 10,000 concurrent users
2. HIGH: OAuth2 callback times out after 30 seconds
3. MEDIUM: getUserPreferences() not yet implemented
4. LOW: Unclosed aiohttp client sessions in test suite

## Architecture Stack
- Frontend: React + TypeScript
- Backend: Python FastAPI
- Cache: Redis 7.2
- Database: PostgreSQL 15 + MongoDB 6
- Auth: OAuth2 with Google provider
- Deployment: Docker + Kubernetes