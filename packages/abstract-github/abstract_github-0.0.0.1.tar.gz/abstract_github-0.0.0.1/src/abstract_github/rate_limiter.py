import time
import requests
from requests.exceptions import HTTPError

# GitHub API rate limits
RATE_LIMIT_URL = "https://api.github.com/rate_limit"

def rate_limited_api_call(url, method='GET', headers=None, data=None, max_retries=5):
    """
    Make a rate-limited GitHub API call with retries and backoff on failure.
    
    Args:
    - url (str): API endpoint URL.
    - method (str): HTTP method ('GET', 'POST', 'PATCH', etc.).
    - headers (dict): Optional HTTP headers.
    - data (dict): Optional payload for POST/PATCH requests.
    - max_retries (int): Maximum number of retries on failure.
    
    Returns:
    - Response object (requests.Response) if successful, None otherwise.
    """
    retries = 0
    while retries <= max_retries:
        try:
            # Make the API request
            response = requests.request(method, url, headers=headers, json=data)
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Check if we are rate-limited
            remaining = int(response.headers.get('X-RateLimit-Remaining', 1))
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
            
            if remaining == 0:
                # Calculate the wait time until the rate limit resets
                sleep_time = max(0, reset_time - time.time())
                print(f"Rate limit exceeded. Waiting for {sleep_time} seconds...")
                time.sleep(sleep_time)
                continue  # Retry after waiting
            
            return response  # If request was successful

        except HTTPError as http_err:
            # Handle rate limit error (403 status)
            if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
                reset_time = int(response.headers['X-RateLimit-Reset'])
                sleep_time = max(0, reset_time - time.time())
                print(f"Rate limit hit, retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
                retries += 1
            else:
                print(f"HTTP error occurred: {http_err}")
                return None
        
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None
        
        # Exponential backoff for retries
        retries += 1
        backoff_time = 2 ** retries
        print(f"Retrying in {backoff_time} seconds...")
        time.sleep(backoff_time)
    
    print("Max retries exceeded.")
    return None


