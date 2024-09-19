import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

# Load the variables from .env file
# Usage of .env file is to keep my credentials safe from public access
load_dotenv()

# JIRA API credentials
JIRA_URL = os.getenv('JIRA_URL')
API_KEY = os.getenv('API_KEY')
EMAIL = os.getenv('EMAIL')
PASS = os.getenv('PASS')

# JIRA API endpoint to fetch tasks assigned
JIRA_SEARCH_URL = f'{JIRA_URL}/rest/api/3/search'

"""
get_jira_tasks()

Fetch tasks from JIRA that are assigned to the current user and unresolved.
Uses JIRA Query Language (JQL) to filter tasks based on these criteria.
    
Returns:
    list: A list of tasks assigned to the current user.
"""
def get_jira_tasks():

    # Define the query parameters
    query = {
        'jql': 'assignee=currentUser()',  # JQL query for all tasks assigned to you
        'fields': ['summary', 'status']  # Fields to retrieve from each task
    }
    
    # Request JIRA API to fetch tasks
    response = requests.get(
        JIRA_SEARCH_URL,
        params=query,
        auth=HTTPBasicAuth(EMAIL, PASS), # Authenticate with email and API Key
        headers={'Content-Type': 'application/json'}
    )

    # Check if the API call was unsuccessful 
    # 200 means ok
    # Print error message and return empty list if unsuccssful
    if response.status_code == 200:
        tasks = response.json()['issues'] # Pars the response to get list of tasks
        return tasks
    else: 
        print(f'Failed to fetch tasks. Status code: {response.status_code}') 
        print(response.text)
        return []

if __name__ == '__main__':
    tasks = get_jira_tasks() # Unresolved tasks

    # Check if any tasks returned
    if tasks:
        print("\n--- Your JIRA Tasks ---")
        for task in tasks:
            print(f'Task: {task["key"]} - {task["fields"]["summary"]}') # Print the task ID and summary
    else:
        print('No unresolved tasks found.')