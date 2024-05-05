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
    user='sranganath@phdata.io',
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

        # Fetch events from the repository within the past day
        print(f"Events for repository {repo_name}:")
        events = repo.get_events()
        for event in events:
            #print(f"{event.created_at}: {event.type} by {event.actor.login}")
            if event.payload.get("ref_type") == "branch":
                branch_name = event.payload.get("ref")
                print(f"Branch : {branch_name} , Event Type : {event.type} by {event.actor.login} at {event.created_at}")
            elif event.type == "PullRequestEvent":
                payload = event.payload
                pr_number = payload.get("number")
                pr_status = payload.get("action")
                pr_created_at = payload.get("created_at")
                source_branch = payload.get("pull_request").get("head").get("ref")
                target_branch = payload.get("pull_request").get("base").get("ref")
                print(f"Pull Request# {pr_number} {pr_action} from branch {source_branch} to branch {target_branch} at {pr_creation_time} is in {pr_status} state")
            # Execute SQL to insert data into Snowflake table
    #        cursor = conn.cursor()
   #         cursor.execute("INSERT INTO Github_feature_branches (User_name,Repo_name,Branch_name, Datetime_of_creation,Status) VALUES (%s,%s,%s,%s, %s)", (creator, repo_name,branch.name,creation_datetime,branch_status))
  #          cursor.close()
            
            # Commit the transaction
 #           conn.commit()
    
    except Exception as e:
        print(f"Error fetching metrics for repository {repo_name}: {e}")
conn.close()
