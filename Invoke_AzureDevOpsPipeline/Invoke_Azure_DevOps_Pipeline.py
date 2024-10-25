import requests
from requests.auth import HTTPBasicAuth

# Define constants
ORG_NAME = "CloudQuickLabs"
PROJECT_NAME = "CloudQuickLabsADO"
PIPELINE_ID = "3"
REPO_NAME = "AzureDemoPipelineAutomation"
BRANCH_NAME = "main"
PAT = "<YOUR PAT TOKEN>"
PARAMETERS = {
    "environment": "prod",
    "buildVersion": "2.1.0"
}
# Azure DevOps REST API URL for triggering a pipeline
URL = f"https://dev.azure.com/{ORG_NAME}/{PROJECT_NAME}/_apis/pipelines/{PIPELINE_ID}/runs?api-version=6.0-preview.1"

def trigger_pipeline(branch_name, repo_name, parameters):
    headers = {
        "Content-Type": "application/json"
    }
    
    # Payload with branch, repository, and parameters
    payload = {
        "resources": {
            "repositories": {
                "self": {
                    "refName": f"refs/heads/{branch_name}",
                    "repository": repo_name
                }
            }
        },
        "templateParameters": parameters
    }
    
    # Send the POST request to trigger the pipeline
    response = requests.post(
        URL,
        auth=HTTPBasicAuth('', PAT),
        headers=headers,
        json=payload
    )

    # Check response status
    if response.status_code in [200, 201]:
        print("Pipeline triggered successfully.")
        print("Run ID:", response.json()["id"])
        return response.json()["id"]
    else:
        print("Failed to trigger pipeline.")
        print("Status Code:", response.status_code)
        try:
            print("Response:", response.json())
        except ValueError:
            print("Response Text:", response.text)

def check_pipeline_status(run_id):
    # Azure DevOps REST API URL for checking the pipeline run status
    status_url = f"https://dev.azure.com/{ORG_NAME}/{PROJECT_NAME}/_apis/pipelines/{PIPELINE_ID}/runs/{run_id}?api-version=6.0-preview.1"
    
    # Send the GET request to retrieve the pipeline run status
    response = requests.get(
        status_url,
        auth=HTTPBasicAuth('', PAT)
    )

    # Check response status
    if response.status_code == 200:
        run_info = response.json()
        print("Pipeline Run ID:", run_info["id"])
        print("Status:", run_info["state"])  # Possible values: inProgress, succeeded, failed, etc.
        print("Result:", run_info.get("result", "Not available"))  # Shows success, failure, etc. if completed
    else:
        print("Failed to retrieve pipeline status.")
        print("Status Code:", response.status_code)
        try:
            print("Response:", response.json())
        except ValueError:
            print("Response Text:", response.text)

#run_id = trigger_pipeline(BRANCH_NAME, REPO_NAME, PARAMETERS)  # Replace with actual branch and repository name

check_pipeline_status(11)

