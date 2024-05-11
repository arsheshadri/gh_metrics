from datetime import datetime, timedelta
from github import Github
from get_github_org_repos import get_organization_repositories
import os
import json

def main():
    org_name = os.environ.get('GITHUB_ORG_NAME')
    access_token = os.environ.get('GITHUB_TOKEN')
  
    if not org_name or not access_token:
      print("Missing organization name or access token.")
      return None
    
    print(f"Retrieving Repositories for Organization - { org_name }")
    repositories = get_organization_repositories(org_name, access_token)
    if repositories:
        print("Repositories in the organization:")
        for repo in repositories:
            print(repo["name"])
    else:
        print("Failed to fetch repositories.")

if __name__ == "__main__":
    main()
