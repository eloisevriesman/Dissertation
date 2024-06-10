import praw
import os
import json

def create_reddit_instance():
    client_id = '_4E-MD4pvjwWtkh50dqsNg'
    client_secret = 'zIDAEXgFCI4wObQr0lzCZAFHA54MEg'
    user_agent = 'MyAPI/0.0.2'
    password = 'tartih-meqwi3-dezfiQ'
    username = 'Smooth-Advisor-61'
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username
    )
    return reddit

def subreddit_moderators(reddit, subreddit_name):
    # Get the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Retrieve the list of moderators d
    moderators = [mod.name for mod in subreddit.moderator()]

    # Create dictionary of moderators
    moderators = {subreddit_name: moderators}

    return moderators

def main():
    subreddits_dir = './scripts/subreddits'
    # Initialize PRAW with your credentials
    reddit = create_reddit_instance()

    # Dictionary to store all moderators
    all_moderators = {}

    # Iterate through txt files in the directory to get all subreddits
    for file in os.listdir(subreddits_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(subreddits_dir, file)
            with open(file_path, 'r') as f:
                subreddits = f.readlines()
                subreddits = [subreddit.strip() for subreddit in subreddits][1:]

                for subreddit_name in subreddits:
                    moderators = subreddit_moderators(reddit, subreddit_name)
                    all_moderators.update(moderators)

    # Save the dictionary to a JSON file
    with open('moderators.json', 'w') as f:
        json.dump(all_moderators, f, indent=4)

if __name__ == '__main__':
    main()