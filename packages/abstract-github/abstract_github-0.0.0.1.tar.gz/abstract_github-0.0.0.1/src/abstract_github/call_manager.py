from .safe_call_data import get_limited_call_safe,os,safe_dump_to_file,safe_read_from_json
from .utils import get_user_name_from_github_link
class completeCallsManager:
    def __init__(self):
    
        self.completed_list_path = os.path.join(os.getcwd(),'completed_list.json')
        self.completed_list = self.load_completed_list()
    def load_completed_list(self):
        if not os.path.isfile(self.completed_list_path):
            safe_dump_to_file(data={},file_path= self.completed_list_path)
        self.completed_list = safe_read_from_json( self.completed_list_path)
        return self.completed_list
    async def call_data_check(self,username,data_type):
        # Initialize user data if not already in completed_list
        data={}
        if self.completed_list.get(username) is None:
            self.completed_list[username] = {"user_info": None, "repo_info": None}
        # Check if data for this key exists in the completed_list_path
        if self.completed_list.get(str(username), {}).get(str(data_type)) is None:
            url = f"https://api.github.com/users/{username}"

            # Modify the URL if we are fetching repo info
            if data_type == 'repo_info':
                url = f"{url}/repos"
            
            # Fetch the data asynchronously (assuming this is an asynchronous function)
            data = await get_limited_call_safe(url)
            if data and isinstance(data,dict):
                self.completed_list[username][data_type] = True
            # Save the data in the completed_list
            # Persist the updated completed_list to the JSON file
            safe_dump_to_file(data=self.completed_list, file_path=self.completed_list_path)

        return data
