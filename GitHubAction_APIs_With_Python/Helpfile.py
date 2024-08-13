import json
import boto3
import requests
from botocore.exceptions import ClientError
import base64
from datetime import datetime

class GitAPIAutomations():
    def __init__(self):
        try: 
            self.session_client = boto3.session.Session()
            self.secretManager_client = self.session_client.client('secretsmanager', region_name="us-west-2")
            self.githubOwner = "<GitHub Owner>"
            self.repoName = "<Repo Name>"
        except Exception as exception:
            print(str(exception))

    def Invoke_github_action(self):
        try:   
            print("Invoking GitHub Actions dynamically...")
            github_action_data = json.loads(self.Get_secret("GitHubPATTOKEN"))
            if github_action_data:
                url = "https://api.github.com/repos/"+self.githubOwner+"/"+self.repoName+"/dispatches"
                headers = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": "Bearer "+github_action_data['GitHubPATTOKEN'],
                    "X-GitHub-Api-Version": "2022-11-28"
                }

                customevent = {
                    "parameter1" : "Sunday",
                    "parameter1" : "22",
                }
                
                print("custom event ", customevent)

                data = {
                    "event_type": "CalledWorkflow",
                    "client_payload": customevent
                }

                ResponseValue=requests.post(url,json=data,headers=headers)
                if  ResponseValue.status_code == 204:
                    print("retrieved the response..")
                    print(ResponseValue)
                    return True
                else:
                    print(ResponseValue)
                    print("Did not get the required response") 
                    return False  
            else:
                print("failed at getting required secrets from AWS secret manager..")  
                return False      
        except Exception as e:
            print("Error occurred in invoke_github_action: ", str(e))
            return False

    def Get_All_List_Of_Runs(self, today_date):
        try:   
            github_action_data = json.loads(self.Get_secret("GitHubPATTOKEN"))
            if github_action_data:
                url = "https://api.github.com/repos/"+self.githubOwner+"/"+self.repoName+"/actions/workflows/calledworkflow.yml/runs"

                # Define headers with the authorization token
                headers = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": "Bearer "+github_action_data['GitHubPATTOKEN'],
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                
                # Collect runs for all statuses
                all_runs = []
                
                page_number = 1
                while True:
                    url = f'{url}?created=>={today_date}&page={page_number}&per_page=100'
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        runs = json.loads(response.text)
                        if not runs['workflow_runs']:
                            break
                        all_runs.extend(runs['workflow_runs'])
                        page_number += 1
                    else:
                        print(f'Failed to get workflow run: {response.status_code} for status {today_date}')
                        return False 
            else:
                print("failed at getting required secrets from AWS secret manager..")  
                return False      
        except Exception as e:
            print("Error occurred in Get_List_Of_Runs: ", str(e))
            return False
        return  all_runs

    def Get_secret(self, secret_name):
            try:
                get_secret_value_response = self.secretManager_client.get_secret_value( SecretId=secret_name)
            except ClientError as e:
                if e.response['Error']['Code'] == 'DecryptionFailureException':
                    raise e
                elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                    raise e
                elif e.response['Error']['Code'] == 'InvalidParameterException':
                    raise e
                elif e.response['Error']['Code'] == 'InvalidRequestException':
                    raise e
                elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                    raise e
            else:
                if 'SecretString' in get_secret_value_response:
                    secret = get_secret_value_response['SecretString']
                    return secret
                else:
                    decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                    return decoded_binary_secret

if __name__ == "__main__":
    TestObject = GitAPIAutomations ()
    try:  
        today_date = datetime.now().strftime('%Y-%m-%d')
        print(TestObject.Invoke_github_action())
        print("Cloud Quick Labs Demo..")
    except Exception as exception:
        print(exception)