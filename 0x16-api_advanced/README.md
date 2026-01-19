# Advanced API Integration with Reddit

## Problem Statement

Modern applications frequently need to consume external APIs efficiently, handling pagination, rate limiting, error conditions, and large datasets. This project demonstrates robust API client implementation patterns through interaction with Reddit's REST API.

## Solution Overview

Implementation of a Python-based Reddit API client featuring:
- **Recursive data retrieval** for handling paginated responses
- **Robust error handling** for network and API failures
- **Data aggregation** across multiple API calls
- **Rate limit awareness** with proper headers

## Implementation Details

### 1. Subscriber Count Retrieval (`0-subs.py`)

**Function:** `number_of_subscribers(subreddit)`

**Problem:** Fetch subscriber count for any subreddit with proper error handling.

**Key Design Decisions:**

```python
# Custom User-Agent to comply with API requirements
headers = {'user-agent': 'my-app/0.0.1'}

# Disable redirects to detect invalid subreddits
r = get(url, headers=headers, allow_redirects=False)

# Graceful degradation: return 0 for any failure
if r.status_code != 200:
    return 0
```

**Error Handling Strategy:**
- Invalid subreddit → Returns 0 (not exception)
- Network failure → Returns 0
- Malformed JSON → Returns 0
- Missing data fields → Returns 0

**Why this approach:** API consumers shouldn't crash on invalid input. Defensive programming with graceful degradation.

### 2. Top Posts Extraction (`1-top_ten.py`)

**Function:** `top_ten(subreddit)`

**Problem:** Retrieve and display top 10 hot posts from a subreddit.

**Implementation Highlights:**
- Uses Reddit's `/r/{subreddit}/hot.json` endpoint
- Limits results to 10 with query parameters
- Handles both API errors and empty results
- Proper None checking prevents AttributeError

**Production Considerations:**
- Currently prints to stdout (OK for CLI tools)
- Could return structured data for programmatic use
- Could add caching to reduce API calls

### 3. Recursive Pagination (`2-recurse.py`)

**Function:** `recurse(subreddit, hot_list=[], after=None)`

**Problem:** Retrieve ALL posts from a subreddit, regardless of count, handling Reddit's pagination.

**Algorithm Design:**

```python
def recurse(subreddit, hot_list=[], after=None):
    # Base case: API error or no more pages
    if response fails:
        return None
    
    # Extract pagination token
    after = data.get('after')
    
    # Recursive case: fetch next page
    if after:
        return recurse(subreddit, hot_list, after)
    else:
        return hot_list
```

**Why Recursion:**
- **Cleaner than iteration** for paginated APIs
- **Natural fit** for "fetch until no more pages" pattern
- **Stateless** - each call is independent

**Trade-offs:**

| Approach | Pros | Cons |
|----------|------|------|
| **Recursion** (chosen) | Clean code, natural pagination handling | Stack overflow risk for huge datasets |
| **Iteration with loop** | Constant stack space, explicit control | More verbose, mutable state |
| **Generator function** | Memory efficient, lazy evaluation | More complex, harder to debug |

**Selected recursion** because:
1. Reddit limits results per request (pagination depth is manageable)
2. Code clarity outweighs theoretical stack concerns
3. Easier to understand and maintain

### 4. Keyword Counting with Sorting (`100-count.py`)

**Function:** `count_words(subreddit, word_list)`

**Problem:** Count occurrences of keywords across ALL posts in a subreddit, handling:
- Case-insensitive matching
- Multiple occurrences per title
- Sorting by count (descending) then alphabetically

**Algorithm Complexity:**
- **Time:** O(n*m) where n = posts, m = keywords per title
- **Space:** O(k) where k = unique keywords

**Advanced Features:**
- Recursive pagination (reuses `recurse` pattern)
- Dictionary aggregation for word counts
- Custom sorting with multiple keys
- Case normalization

**Edge Cases Handled:**
- Empty subreddits
- Invalid subreddits
- Keywords not found
- Duplicate keywords in word_list

## API Design Patterns Demonstrated

### 1. Defensive Programming
```python
# Never trust external data
try:
    js = r.json()
except ValueError:
    return 0

# Always validate nested data access
data = js.get("data")
if data:
    sub_count = data.get("subscribers")
    if sub_count:
        return sub_count
```

### 2. Proper HTTP Headers
```python
# Reddit requires custom User-Agent
headers = {'user-agent': 'my-app/0.0.1'}

# Prevents 429 (Too Many Requests) responses
# Shows respect for API provider guidelines
```

### 3. Pagination Handling
```python
# Extract pagination token
after = data.get('after')

# Recursive call with continuation token
if after:
    params = {'after': after, 'limit': 100}
    recurse(subreddit, hot_list, after)
```

### 4. Error Propagation
```python
# Clear contract: None means error, list means success
if response_fails:
    return None
else:
    return hot_list
```

## Technical Considerations

### Rate Limiting
**Current:** Relies on Reddit's default rate limits (60 requests/minute)

**Improvement opportunities:**
- Implement exponential backoff for 429 responses
- Add configurable delay between requests
- Cache responses to reduce API calls
- Monitor rate limit headers in responses

### Authentication
**Current:** Unauthenticated (public endpoints only)

**For production:**
- OAuth 2.0 authentication for higher rate limits
- Secure credential storage (environment variables)
- Token refresh logic
- User-specific data access

### Scalability
**Current limitations:**
- Synchronous requests (blocking)
- No connection pooling
- Limited error recovery

**Scaling strategies:**
- Async I/O with `aiohttp` for concurrent requests
- Connection pooling with `requests.Session()`
- Retry logic with exponential backoff
- Circuit breaker pattern for failing APIs

## Testing Strategy

**Manual testing:**
```bash
# Valid subreddit
python3 0-subs.py programming  # Should return subscriber count

# Invalid subreddit
python3 0-subs.py invalidsubredditname999  # Should return 0

# Large dataset pagination
python3 2-recurse.py programming  # Should fetch all posts
```

**Production testing needs:**
- Unit tests with mocked HTTP responses
- Integration tests with test subreddit
- Performance tests for pagination efficiency
- Error injection tests (network failures, malformed JSON)

## Key Learnings

1. **API clients must handle all failure modes** - Network, HTTP errors, malformed data
2. **Pagination requires careful state management** - Tokens, hasNext flags, cursor patterns
3. **Recursion suits naturally paginated data** - But consider stack limits
4. **User-Agent headers matter** - Many APIs require or prefer them
5. **Type safety helps** - Defensive None checks prevent runtime errors

## Production Improvements

**High Priority:**
1. Add comprehensive error logging
2. Implement retry logic with exponential backoff
3. Add rate limit handling (sleep when approaching limits)
4. Return structured objects instead of raw data
5. Add type hints for better IDE support

**Medium Priority:**
1. Async/await for concurrent requests
2. Response caching (Redis/memcached)
3. Metrics collection (request count, latency, errors)
4. OAuth authentication support
5. Unit test coverage

**Low Priority:**
1. CLI argument parsing for easier use
2. Output formatting options (JSON, CSV)
3. Streaming responses for very large datasets
4. WebSocket support for real-time updates

## Related Concepts

- **REST API design principles** - Resource-based URLs, HTTP methods
- **Pagination patterns** - Cursor-based, offset-based, link headers
- **Error handling strategies** - Fail fast vs graceful degradation
- **Rate limiting** - Token bucket, sliding window
- **API authentication** - OAuth 2.0, API keys, JWTs

---

*This project demonstrates production-ready API client development with attention to error handling, pagination, and data processing patterns essential for reliable integrations.*
