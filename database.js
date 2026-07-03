// ARCHITECTURAL DECISION: Redis as primary caching layer
// Date: June 15, 2026
// Decision maker: Rudra
// Reason: Reduced dashboard load time from 400ms to under 15ms
// Previous approach: Direct PostgreSQL reads — too slow under load

const redis = require('redis');

const client = redis.createClient({
    host: 'localhost',
    port: 6379
});

async function getUserDashboard(userId) {
    // BUG: Redis dropping connections when concurrent users exceed 10,000
    // Current Status: CRITICAL — blocks Friday launch
    // Tried: Basic connection pooling — didn't help
    // Next to try: Circuit breaker pattern + connection pool size increase
    // This MUST be fixed before deployment
    
    return await client.get(`dashboard:${userId}`);
}

// DECISION: MongoDB for user preferences (not PostgreSQL)
// Reason: Preferences schema changes frequently — SQL schema migrations
// were slowing down the team. MongoDB gives schema flexibility.
async function getUserPreferences(userId) {
    // Implementation pending — left off here last session
    // File: preferences-service.js also needs updating
}

module.exports = { getUserDashboard, getUserPreferences };