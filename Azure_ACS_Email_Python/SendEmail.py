from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential

credential = AzureKeyCredential("ii/YlHlUasc+0RVWm7BCVHUQ5OBM5TWiOv7V0cfqIwTOM7PCV4IUa6GfR0+WnoqoV++F0HkbRYdFunp/34GPSA==")
endpoint = "https://demo-acs-cloudquicklabs.unitedstates.communication.azure.com/"
client = EmailClient(endpoint, credential)

message = {
    "content": {
        "subject": "This is python SDK code based email",
        "plainText": "This is message from body... Blah Blah Blah",
        "html": "<html><h1>This is message from body... Blah Blah Blah</h1></html>"
    },
    "recipients": {
        "to": [
            {
                "address": "vrchinnarathod@gmail.com",
                "displayName": "Cloud Quick Labs"
            }
        ]
    },
    "senderAddress": "DoNotReply@29fa5839-e089-4cfb-93b5-dfc003e6df03.azurecomm.net"
}

poller = EmailClient.begin_send(client, message)
result = poller.result()
print(result)