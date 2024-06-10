# This script gets the name and id's of the top 10 hot posts in the specified subreddit
# This json gets saved into the 'subreddit'_data folder
# The json is called: 'subreddit'_top_10_hot_post_titles'

import requests
import json
import os

# Subreddit - change to the desired community
subreddit = 'music' 

# Your credentials
CLIENT_ID = '_4E-MD4pvjwWtkh50dqsNg'
SECRET_ID = 'zIDAEXgFCI4wObQr0lzCZAFHA54MEg'

# Authenticate
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_ID)
with open('pw.txt', 'r') as file:
    pwd = file.read()
data = {
    'grant_type': 'password',
    'username': 'Smooth-Advisor-61',
    'password': pwd
}
headers = {'User-Agent': 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

# Fetches top 10 hot posts from the specified subreddit
hot_posts_res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot', headers=headers, params={'limit': '10'})

# Parse post titles and IDs
posts_info = [{'title': post['data']['title'], 'id': post['data']['id']} for post in hot_posts_res.json()['data']['children']]

# Folder to save JSON files, named after the subreddit
folder_name = f'{subreddit}_data'
os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist

# Saving Data in a formatted JSON in a subfolder
json_filename = os.path.join(folder_name, f'{subreddit}_top_10_hot_post_titles.json')
with open(json_filename, 'w') as file:
    json.dump(posts_info, file, indent=4)
