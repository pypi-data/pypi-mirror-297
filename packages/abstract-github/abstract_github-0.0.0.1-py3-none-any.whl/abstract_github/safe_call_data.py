from .utils import *
from .rate_limiter import rate_limited_api_call
async def fetch_data_from_api(url):
    """
    Simulate an async function that fetches data from an API.
    Replace this with your actual API call logic.
    """
    await asyncio.sleep(1)  # Simulate network delay
    return {"dummy_data": f"Data from {url}"}


async def get_limited_call_safe(call_url,token=None):
    """
    This function safely calls the API and logs both successful responses and errors.
    """
    response_data = {}
    
    print(call_url)
    # Attempt to make the API call
    user_info =  rate_limited_api_call(call_url)

    if user_info:
        # Successful response, parse JSON
        response_data = user_info
        if response_data:
            try:
                response_data = response_data.json()
            except:
                response_data = response_data.text
        response_data = process_templated_urls(response_data)
        # Log the successful response
        log_response(call_url, response_data)
    try:
        print('hihihi')
    except Exception as e:
        # If any error occurs, log it and add error details to the response
        response_data = {
            "response": None,
            "error": True,
            "error_message": str(e)
        }
        log_error(call_url, e)

    return response_data

def process_templated_urls(obj):
    """
    Recursively processes nested dictionaries and lists to replace template parts in URLs.
    """
    if isinstance(obj, dict):
        # Process dictionary by iterating through key-value pairs
        for key, value in obj.items():
            if isinstance(value, str):
                # If a string contains a URL template, remove or replace it
                if '{' in value:
                    obj[key] = value.replace('{/sha}', '').replace('{/other_user}', '').replace('{/gist_id}', '')
            else:
                # If value is a nested dictionary or list, process it recursively
                obj[key] = process_templated_urls(value)
    elif isinstance(obj, list):
        # If the object is a list, process each element recursively
        for i, item in enumerate(obj):
            obj[i] = process_templated_urls(item)
    
    return obj
def log_response(call_url, response):
    """
    Logs the API response.
    """
    logging.info(f"API Call to {call_url} succeeded. Response: {json.dumps(response)}")

def log_error(call_url, error):
    """
    Logs any error that occurred during the API call.
    """
    logging.error(f"API Call to {call_url} failed. Error: {str(error)}")
