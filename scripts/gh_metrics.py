from datetime import datetime, timedelta
from github import Github
import os
import json

# GitHub API token or username/password authentication
g = Github("your_access_token")

# List of repository names
repo_names = ["owner1/repo1", "owner2/repo2"]  # Add as many repositories as needed

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
