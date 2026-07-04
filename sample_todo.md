# Developer Notes - Sprint 24

## What I was working on last
- Refactored middleware layer in auth_service
- Left off at auth.py line 87 - error handler cleanup
- Need to fix JWT bug before Friday deployment

## Architecture Decisions Made
1. Redis for caching - PostgreSQL was too slow for session store
2. OAuth2 with JWT for API auth - decided over session-based auth
3. MongoDB planned for user preferences - schema flexibility needed

## Open Bugs (Priority Ordered)
1. [CRITICAL] JWT refresh endpoint not working - tried sliding window and forced re-login, both failed
2. [MEDIUM] WebSocket connections dropping after 5 minutes
3. [LOW] Rate limiter too aggressive on /api/search

## Blockers
- Awaiting DevOps to provision Redis cluster in staging
- Code review pending for middleware refactor (PR #142)
