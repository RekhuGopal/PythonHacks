import requests
import json

#http://man.hubwiz.com/docset/Terraform.docset/Contents/Resources/Documents/docs/enterprise/api/workspaces.html
## CREATE
'''
print("Creating the TFC workspace dynamically...")
url = 'https://app.terraform.io/api/v2/organizations/ecp-shell-titan/workspaces'
TOKEN = 'bX6gDEYZqUY5Eg.atlasv1.ZRZRwRHzTUCxLwmDqgac8fER0nmM3BRXgG1BGrCWDFLFlguMJDQWGwANU00ZxGl9PAM'
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
payload={
    'data': {
      'attributes': {
      'name': 'workspace-6'
    },
    'type': 'workspaces'
  }
}
TFCCreateresponse = requests.request("POST", url, headers=headers, data=json.dumps(payload))
if  TFCCreateresponse.status_code == 201:
    print("retrieved the response..")
    print(TFCCreateresponse)

else:
    print(TFCCreateresponse)
    print("Did not get the required response")
'''
'''
## UPDATE

print("Updating the TFC workspace dynamically...")

TOKEN = 'bX6gDEYZqUY5Eg.atlasv1.ZRZRwRHzTUCxLwmDqgac8fER0nmM3BRXgG1BGrCWDFLFlguMJDQWGwANU00ZxGl9PAM'
Work_SpaceName = 'workspace-7'
url = 'https://app.terraform.io/api/v2/organizations/ecp-shell-titan/workspaces/'+Work_SpaceName
headers = {'Authorization': 'Bearer '+TOKEN,
           'Content-Type': 'application/vnd.api+json'
          }
payload={
    'data': {
      'attributes': {
      'name': 'workspace-8'
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
TOKEN = 'bX6gDEYZqUY5Eg.atlasv1.ZRZRwRHzTUCxLwmDqgac8fER0nmM3BRXgG1BGrCWDFLFlguMJDQWGwANU00ZxGl9PAM'
Work_SpaceName = 'workspace-3'
url = 'https://app.terraform.io/api/v2/organizations/ecp-shell-titan/workspaces/'+Work_SpaceName
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
TOKEN = 'bX6gDEYZqUY5Eg.atlasv1.ZRZRwRHzTUCxLwmDqgac8fER0nmM3BRXgG1BGrCWDFLFlguMJDQWGwANU00ZxGl9PAM'
Work_SpaceName = 'workspace-1'
url = 'https://app.terraform.io/api/v2/organizations/ecp-shell-titan/workspaces/'+Work_SpaceName
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
TOKEN = 'bX6gDEYZqUY5Eg.atlasv1.ZRZRwRHzTUCxLwmDqgac8fER0nmM3BRXgG1BGrCWDFLFlguMJDQWGwANU00ZxGl9PAM'
url = 'https://app.terraform.io/api/v2/organizations/ecp-shell-titan/workspaces'
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
TOKEN = 'zeWz2yyhsCkzrw.atlasv1.YrB3VlBy3wgvS2sPEhokouCeETZdacbmHYmMRGtQCSlNokFjCBkLQgIcEoS2CR64oz8'
Work_Id = 'ws-VphPC7zVuiKFc6xq'
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

##UNLOCK Workspaces
print("Lock the TFC workspace dynamically...")
TOKEN = 'zeWz2yyhsCkzrw.atlasv1.YrB3VlBy3wgvS2sPEhokouCeETZdacbmHYmMRGtQCSlNokFjCBkLQgIcEoS2CR64oz8'
Work_Id = 'ws-VphPC7zVuiKFc6xq'
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
