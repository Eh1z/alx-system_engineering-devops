#!/usr/bin/python3
"""
Reddit API Client - Recursive Pagination Handler

Module: 2-recurse.py
Purpose: Recursively fetch ALL hot posts from a subreddit using pagination

Algorithm: Recursive traversal of paginated API responses
Complexity: O(n) where n is total number of posts
Space: O(n) for accumulating post titles

Key Concepts Demonstrated:
    - Recursive algorithm for API pagination
    - Stateless recursion with accumulator pattern
    - Continuation token handling (Reddit's 'after' parameter)
    - Base case: No more pages (after=None) or API error
    - Recursive case: Fetch next page with continuation token

Reddit Pagination Model:
    - Each response contains up to 100 posts (configurable via 'limit')
    - Response includes 'after' token for fetching next page
    - When 'after' is null, we've reached the end
    
Production Improvements Needed:
    - Add rate limiting / exponential backoff
    - Implement max recursion depth to prevent stack overflow
    - Add logging for debugging pagination issues
    - Consider converting to iterative approach for very large datasets
"""
from requests import get

# API configuration constants
REDDIT = "https://www.reddit.com/"
HEADERS = {'user-agent': 'my-app/0.0.1'}


def recurse(subreddit, hot_list=[], after=""):
    """
    Recursively retrieve all hot post titles from a subreddit.
    
    This function implements recursive pagination to fetch ALL posts,
    not just the first page. Uses Reddit's 'after' token for continuation.
    
    Args:
        subreddit (str): Name of the subreddit to query
        hot_list (list): Accumulator for post titles (modified in-place)
        after (str): Pagination token from previous response
                     - Empty string "" for first page
                     - Token string for subsequent pages
                     - None when no more pages exist
                     
    Returns:
        list: All hot post titles if successful
        None: If subreddit invalid, API error, or malformed response
        
    Recursion Strategy:
        Base case 1: after is None → return accumulated results
        Base case 2: API error (status != 200) → return None
        Recursive case: Fetch page, extract 'after', recurse with new token
        
    Why Recursion vs Iteration:
        ✓ Natural fit for "fetch until no more pages" pattern
        ✓ Cleaner code, easier to understand
        ✓ Stateless - each call is independent
        ✗ Stack overflow risk for extremely large subreddits (rare in practice)
        ✗ Can't easily add progress indicators
        
    Example:
        >>> recurse('python')
        ['Title 1', 'Title 2', ..., 'Title N']  # All posts
        >>> recurse('invalidsubreddit999')
        None
    """
    # Base case: No more pages to fetch
    # after=None signals we've reached the end of pagination
    if after is None:
        return hot_list

    # Construct API URL for hot posts endpoint
    url = REDDIT + "r/{}/hot/.json".format(subreddit)

    # Pagination parameters
    # limit: Maximum posts per request (100 is Reddit's max)
    # after: Continuation token for next page (empty string for first page)
    params = {
        'limit': 100,
        'after': after
    }

    # Execute HTTP GET request
    # allow_redirects=False: Detect invalid subreddits (they redirect to search)
    r = get(url, headers=HEADERS, params=params, allow_redirects=False)

    # Validate HTTP response
    # Non-200 status indicates error: invalid subreddit, rate limit, etc.
    if r.status_code != 200:
        return None

    # Parse JSON response with error handling
    try:
        js = r.json()

    except ValueError:
        # Malformed JSON response
        return None

    # Extract data from Reddit API response structure
    try:
        # Reddit API envelope: {data: {after: "token", children: [...]}}
        data = js.get("data")
        
        # Extract pagination token for next page
        # Will be None if this is the last page
        after = data.get("after")
        
        # Extract array of post objects
        children = data.get("children")
        
        # Accumulate post titles into hot_list
        # Each child contains metadata in nested 'data' object
        for child in children:
            post = child.get("data")
            hot_list.append(post.get("title"))

    except:
        # Catch-all for unexpected response structure
        # Could happen if Reddit API changes format
        # Production code should log specific exception
        return None

    # Recursive call with updated state
    # after: Continuation token (None if last page)
    # hot_list: Accumulated titles (modified in-place)
    # Base case will trigger when after=None
    return recurse(subreddit, hot_list, after)
