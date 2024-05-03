from datetime import datetime, timedelta
from github import Github
import os
import json

github_token = os.environ.get('GITHUB_TOKEN')

# GitHub API token or username/password authentication
g = Github(github_token)

base_repo_path = os.path.dirname(os.getenv('GITHUB_WORKSPACE'))
print(f"base_repo_path is {base_repo_path}:")
#config_file_path = os.path.join(base_repo_path, 'config', 'configs.json')
config_file_path = os.environ.get('CONFIG_FILE')
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
        
        print(f"Branch details for repository {repo_name}:")    
        # Get all branches of the repository
        branches = repo.get_branches()
        
        # Fetch events from the repository within the past day
        events = repo.get_events()

        # Iterate through each branch
        for branch in branches:
            # Get branch protection status
            branch_protection = repo.get_branch_protection(branch.name)
            protection_status = "Protected" if branch_protection.protected else "Not Protected"
            
            # Get branch creator's username and creation datetime
            commit = repo.get_commit(branch.commit.sha)
            creator = commit.commit.author.name
            creation_datetime = format_datetime(commit.commit.author.date)
            
            # Get GitHub team name (if applicable)
            team_name = "N/A"  # Replace with actual implementation to fetch team name
            
            # Print branch details
            print(f"Branch Name: {branch.name}")
            print(f"Status: {protection_status}")
            print(f"Creator's Username: {creator}")
            print(f"GitHub Team Name: {team_name}")
            print(f"Creation Datetime: {creation_datetime}")
            print()

        print(f"Events for repository {repo_name}:")
        # Iterate through events
        for event in events:
            print(f"{event.created_at}: {event.type} by {event.actor.login}")
    
    except Exception as e:
        print(f"Error fetching events for repository {repo_name}: {e}")
