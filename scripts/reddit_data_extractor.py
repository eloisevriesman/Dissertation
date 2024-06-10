# Script that fetches top 10 hot posts & all the comments from a list of subreddits and saves them in a new folder

import requests
import json
import os
import praw

def fetch_post_and_comments(subreddit_name, post_id, reddit, main_folder):
    """
    Fetches a post's title and its comments, saving it to a json in the correct category folder

    subreddit_name (str): The name of the subreddit.
    post_id (str): The ID of the post to be fetched.
    reddit (praw.Reddit): The Reddit instance for API access.
    main_folder (str): The name of the folder to save the file in
    """
    post = reddit.submission(id=post_id)

    # Fetch post title
    post_title = post.title

    def process_comment(comment, depth=0):

        # Data collected from each comment
        comment_data = {
            'depth': depth, # If it is a reply or not
            'author': comment.author.name if comment.author else '[deleted]',
            'body': comment.body, # The content
            'score': comment.score # Upvotes - Downvotes
        }

        # Recursively iterates through replies to a comment and filters out more buttons
        replies = [process_comment(reply, depth + 1) for reply in comment.replies if not isinstance(reply, praw.models.MoreComments)]
        
        # If there is a reply it adds it to the comment data as a reply
        if replies:
            comment_data['replies'] = replies
        return comment_data

    # Handles "more comments" buttons
    post.comments.replace_more(limit=None)
    comments_data = [process_comment(comment) for comment in post.comments]

    post_data = {'title': post_title, 'comments': comments_data}

    # Svaves file inside a subreddit-specific folder, inside the main category folder
    subreddit_folder = os.path.join(main_folder, f'{subreddit_name}_data')
    os.makedirs(subreddit_folder, exist_ok=True)
    json_filename = os.path.join(subreddit_folder, f'{subreddit_name}_post_{post_id}_data.json')
    with open(json_filename, 'w') as file:
        json.dump(post_data, file, indent=4)

# Authenticate and creates a Reddit instance
def create_reddit_instance():
    client_id = '_4E-MD4pvjwWtkh50dqsNg'
    client_secret = 'zIDAEXgFCI4wObQr0lzCZAFHA54MEg'
    user_agent = 'MyAPI/0.0.1'
    with open('pw.txt', 'r') as file:
        password = file.read()
    username = 'Smooth-Advisor-61'

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username
    )
    return reddit

def process_subreddit(subreddit_name, reddit, main_folder):
    """
    Processes the top 10 hot posts from a specified subreddit.

    Parameters:
    subreddit_name (str): The name of the subreddit.
    reddit (praw.Reddit): The Reddit API instance.
    main_folder (str): The main folder name where all subreddit data will be stored.
    """
    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=10)

    # Makes subfolder for subreddit to save posts in
    folder_name = os.path.join(main_folder, f'{subreddit_name}_data')
    os.makedirs(folder_name, exist_ok=True)

    # Gets post titles and comments
    for post in hot_posts:
        fetch_post_and_comments(subreddit_name, post.id, reddit, main_folder)

def main(config_file):
    """
    Main function to read configuration file and process each subreddit.

    Parameters:
    config_file (str): The path to the subreddit information text file.
    """
    reddit = create_reddit_instance()

    with open(config_file, 'r') as file:
        lines = file.readlines()
        main_folder = lines[0].strip()  # Main folder called first line of file
        os.makedirs(main_folder, exist_ok=True)  # Create main folder

        for subreddit_name in lines[1:]:  # Process each subreddit in the text file
            process_subreddit(subreddit_name.strip(), reddit, main_folder)

if __name__ == "__main__":
    config_file = 'subreddits/random.txt'
    main(config_file)