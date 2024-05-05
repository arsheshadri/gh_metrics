from datetime import datetime, timedelta
from github import Github
import os
import json
import snowflake.connector

github_token = os.environ.get('GITHUB_TOKEN')

# GitHub API token or username/password authentication
g = Github(github_token)

def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')

base_repo_path = os.path.dirname(os.getenv('GITHUB_WORKSPACE'))
print(f"base_repo_path is {base_repo_path}:")
#config_file_path = os.path.join(base_repo_path, 'config', 'configs.json')
config_file_path = os.environ.get('CONFIG_FILE')
print(f"config_file_path is {config_file_path}:")

conn = snowflake.connector.connect(
    user='SRANGANATH',
    password='Mongodb@2024',
    account='SNOWDATA',
    warehouse='DEFAULT_USER_WH',
    database='USER_SRANGANATH',
    schema='ANALYTICS_DEV'
)

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
        
        # Get all branches of the repository
        branches = repo.get_branches()
        
        # Fetch events from the repository within the past day
        events = repo.get_events()
        print(f"Branch details for repository {repo_name}:")    
        # Iterate through each branch
        for branch in branches:
           # Get branch creator's username and creation datetime
            commit = repo.get_commit(branch.commit.sha)
            creator = commit.commit.author.name
            creation_datetime = format_datetime(commit.commit.author.date)
            
            # Get branch status (assuming it's always active)
            branch_status = "Active"
            
            # Print branch details
            print(f"Branch Name: {branch.name}")
            print(f"Status: {branch_status}")
            print(f"Creator's Username: {creator}")
            print(f"Creation Datetime: {creation_datetime}")
            
            print("Connecting to Snowflake....")

            # Execute SQL to insert data into Snowflake table
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Github_feature_branches (User_name,Repo_name,Branch_name, Datetime_of_creation,Status) VALUES (%s, %s)", ({creator}, {repo_name},{branch.name},{creation_datetime},{branch_status}))
            cursor.close()
            
            # Commit the transaction
            conn.commit()
            
            # Close the connection
            conn.close()
            
        print(f"Events for repository {repo_name}:")
        # Iterate through events
        for event in events:
            print(f"{event.created_at}: {event.type} by {event.actor.login}")
    
    except Exception as e:
        print(f"Error fetching metrics for repository {repo_name}: {e}")
