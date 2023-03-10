import requests
import json
TOKEN = '<API token>'
#http://man.hubwiz.com/docset/Terraform.docset/Contents/Resources/Documents/docs/enterprise/api/workspaces.html
'''
## CREATE

print("Creating the TFC workspace dynamically...")
url = 'https://app.terraform.io/api/v2/organizations/<your org>/workspaces'
TOKEN = '<API token>'
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
payload={
    'data': {
      'attributes': {
      'name': 'demoworkspace'
    },
    'type': 'workspaces'
  }
}
TFCCreateresponse = requests.request("POST", url, headers=headers, data=json.dumps(payload))
if  TFCCreateresponse.status_code == 201:
    print("retrieved the response..")
    print(TFCCreateresponse.content)

else:
    print(TFCCreateresponse.content)
    print("Did not get the required response")
'''
## UPDATE

'''
print("Updating the TFC workspace dynamically...")

#TOKEN = ''
Work_SpaceName = 'demoworkspace'
url = 'https://app.terraform.io/api/v2/organizations/<your org>/workspaces/'+Work_SpaceName
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
payload={
    'data': {
      'attributes': {
      'name': 'demoworkspace1'
    },
    'type': 'workspaces'
  }
}
TFCUpdateresponse = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))
if  TFCUpdateresponse.status_code == 200:
    print("Updated successfully..")
    print(TFCUpdateresponse)

else:
    print(TFCUpdateresponse)
    print("Did not get the required response")

'''
'''
## DELETE
print("Deleting the TFC workspace dynamically...")
#TOKEN = ''
Work_SpaceName = 'demoworkspace1'
url = 'https://app.terraform.io/api/v2/organizations/<your org>/workspaces/'+Work_SpaceName
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
TFCDeleteresponse = requests.request("DELETE", url, headers=headers)
if  TFCDeleteresponse.status_code == 204:
    print("Deleted successfully..")
    print(TFCDeleteresponse)

else:
    print(TFCDeleteresponse)
    print("Did not get the required response")
'''
'''
## READ
print("Read the TFC workspace dynamically...")
#TOKEN = ''
Work_SpaceName = 'AWSBackup'
url = 'https://app.terraform.io/api/v2/organizations/<your org>/workspaces/'+Work_SpaceName
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
TFCReadresponse = requests.request("GET", url, headers=headers)
if  TFCReadresponse.status_code == 200:
    print("Got read response successfully..")
    print(TFCReadresponse.content)

else:
    print(TFCReadresponse.content)
    print("Did not get the required response")
'''

'''
## LIST ALL
print("List all the TFC workspace dynamically...")
#TOKEN = ''
url = 'https://app.terraform.io/api/v2/organizations/<your org>/workspaces'
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
TFCListresponse = requests.request("GET", url, headers=headers)
if  TFCListresponse.status_code == 200:
    print("Got read response successfully..")
    print(TFCListresponse.content)

else:
    print(TFCListresponse.content)
    print("Did not get the required response")
'''
'''
## Lock Workspace ( Needs user access token)
print("Lock the TFC workspace dynamically...")
#TOKEN = ''
Work_Id = '<workspace id>'
url = 'https://app.terraform.io/api/v2/workspaces/'+Work_Id+'/actions/lock'
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
payload = {
  'reason': 'Locking workspace-1'
}
TFCLockResponse = requests.request("POST", url, headers=headers,data=json.dumps(payload))
print(TFCLockResponse)
if  TFCLockResponse.status_code == 200:
    print("Locked WS response successfully..")
    print(TFCLockResponse.content)

else:
    print(TFCLockResponse.content)
    print("Did not get the required response")
'''

'''
##UNLOCK Workspaces
print("Lock the TFC workspace dynamically...")
#TOKEN = ''
Work_Id = '<workspace id>'
url = 'https://app.terraform.io/api/v2/workspaces/'+Work_Id+'/actions/unlock'
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
TFCUNLockResponse = requests.request("POST", url, headers=headers)
print(TFCUNLockResponse)
if  TFCUNLockResponse.status_code == 200:
    print("UnLocked WS, response successfully..")
    print(TFCUNLockResponse.content)

else:
    print(TFCUNLockResponse.content)
    print("Did not get the required response")
'''