#!/usr/bin/python3
"""
Reddit API Client - Subscriber Count Retrieval

Module: 0-subs.py
Purpose: Query Reddit API to fetch subreddit subscriber counts with robust error handling

Key Design Patterns:
    - Defensive programming with graceful degradation
    - Proper HTTP header configuration for API compliance
    - Comprehensive error handling for network and API failures
    
API Endpoint: https://www.reddit.com/r/{subreddit}/about.json
Requirements: requests library (HTTP client)

Production Considerations:
    - Rate limiting: Reddit allows ~60 requests/minute for unauthenticated clients
    - Error handling: Returns 0 instead of raising exceptions for invalid input
    - User-Agent: Custom header required by Reddit API (prevents 429 errors)
"""


def number_of_subscribers(subreddit):
    """
    Retrieve the subscriber count for a given subreddit.
    
    Args:
        subreddit (str): Name of the subreddit (e.g., 'python', 'programming')
        
    Returns:
        int: Number of subscribers, or 0 if:
            - Subreddit doesn't exist (404)
            - Network error occurs
            - Response is malformed JSON
            - Required data fields are missing
            
    Implementation Notes:
        - Uses allow_redirects=False to detect invalid subreddits
          (Reddit redirects invalid subs to search page)
        - Custom User-Agent prevents rate limiting (Reddit requirement)
        - Nested data validation prevents AttributeError on missing fields
        
    Example:
        >>> number_of_subscribers('python')
        1234567
        >>> number_of_subscribers('invalidsubreddit999')
        0
    """
    from requests import get

    # Construct API endpoint URL
    # Reddit's about.json provides subreddit metadata including subscriber count
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    # Custom User-Agent header - REQUIRED by Reddit API
    # Without this, requests may be rate limited or blocked
    # Format: <platform>:<app ID>:<version> (by /u/<reddit username>)
    headers = {'user-agent': 'my-app/0.0.1'}

    # Make HTTP GET request
    # allow_redirects=False: Invalid subreddits redirect to search, we want to detect this
    r = get(url, headers=headers, allow_redirects=False)

    # Check HTTP status code
    # 200: Success, subreddit exists
    # 404: Subreddit not found
    # 302: Redirect (invalid subreddit, caught by allow_redirects=False)
    # 429: Rate limited (need to slow down requests)
    if r.status_code != 200:
        return 0

    # Parse JSON response with error handling
    # Malformed responses or network issues can cause JSON decode errors
    try:
        js = r.json()

    except ValueError:
        # JSON parsing failed - malformed response or non-JSON content
        return 0

    # Extract 'data' object from response
    # Reddit API wraps actual data in a 'data' envelope
    data = js.get("data")

    # Defensive null checking - validate data exists before accessing nested fields
    # Prevents KeyError or AttributeError if API response structure changes
    if data:
        sub_count = data.get("subscribers")
        if sub_count:
            return sub_count

    # Default return: if any validation fails, return 0
    # Graceful degradation - caller doesn't need to handle exceptions
    return 0
