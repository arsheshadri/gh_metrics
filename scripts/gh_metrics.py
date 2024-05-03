from datetime import datetime, timedelta
from github import Github
import os
import json

github_token = os.environ.get('GITHUB_TOKEN')

# GitHub API token or username/password authentication
g = Github(github_token)

base_repo_path = os.getenv('GITHUB_WORKSPACE')
print(f"base_repo_path is {base_repo_path}:")
config_file_path = os.path.join(base_repo_path, 'config', 'config.json')
print(f"config_file_path is {config_file_path}:")

with open(config_file_path) as f:
    config = json.load(f)
    repo_names = config['repo_names']

# Get current date and time
now = datetime.utcnow()

# Calculate datetime object for one day ago
one_day_ago = now - timedelta(days=1)

# Convert datetime objects to GitHub API timestamps
since = one_day_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
until = now.strftime('%Y-%m-%dT%H:%M:%SZ')

# Iterate through each repository
for repo_name in repo_names:
    try:
        # Get the repository object
        repo = g.get_repo(repo_name)
        
        # Fetch events from the repository within the past day
        events = repo.get_events(since=since, until=until)
        
        print(f"Events for repository {repo_name}:")
        
        # Iterate through events
        for event in events:
            print(f"{event.created_at}: {event.type} by {event.actor.login}")
    
    except Exception as e:
        print(f"Error fetching events for repository {repo_name}: {e}")
