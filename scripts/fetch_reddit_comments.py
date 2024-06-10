# This script requires a subreddit name and post_id
# It gets all of the comments in the post and organises them based on their depth so its like how you read a reddit page normally
# It also includes the score
# The data is saved in a file called 'subreddit_name'_post_'post_id'_comments.json'

import praw
import json
import os

# Input the reddit name and post_id wanted
subreddit_name = 'politics'
post_id = '19dokvb'  

def process_comment(comment, depth=0):
    """ Recursively process a comment and its replies. """
    comment_data = {
        'depth': depth,
        'author': comment.author.name if comment.author else '[deleted]',
        'body': comment.body, 
        'score': comment.score # (upvotes - downvotes)
    }
    replies = []
    for reply in comment.replies:
        if isinstance(reply, praw.models.MoreComments):
            continue
        replies.append(process_comment(reply, depth + 1))
    if replies:
        comment_data['replies'] = replies
    return comment_data

# Reddit credentials and subreddit
client_id = '_4E-MD4pvjwWtkh50dqsNg'
client_secret = 'zIDAEXgFCI4wObQr0lzCZAFHA54MEg'
username = 'Smooth-Advisor-61'
with open('pw.txt', 'r') as file:
    password = file.read()
user_agent = 'script by /u/' + username

# Initialize PRAW with credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username
)

# Fetch the post
post = reddit.submission(id=post_id)
post.comments.replace_more(limit=None)

# Process each top-level comment and its replies
comments_data = [process_comment(comment) for comment in post.comments]

# Saving Data in a formatted JSON in a subfolder
folder_name = f'{subreddit_name}_data'
os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist
json_filename = os.path.join(folder_name, f'{subreddit_name}_post_{post_id}_comments.json')
with open(json_filename, 'w') as file:
    json.dump(comments_data, file, indent=4)
