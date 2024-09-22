import requests,asyncio,json,os
from abstract_utilities import *
base_url = "https://api.github.com/users/"

def get_github_from_user_name(username):
    return f'https://github.com/{username}'
def get_user_name_from_github_link(github_link):
    return make_list([subdir for subdir in github_link.split('github.com')[-1].split('/') if subdir] or None)[0]
def get_clean_string(string):
    return eatAll(string,['/','\n',' ','\t']).split('/')[-1]
