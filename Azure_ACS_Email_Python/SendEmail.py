from azure.communication.email import EmailClient
from azure.core.credentials import AzureKeyCredential

credential = AzureKeyCredential("<Azure Communication Service Key>")
endpoint = "<Azure Communication Service Endpoint>"
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
                "address": "sdfsgd@gmail.com",
                "displayName": "Cloud Quick Labs"
            }
        ]
    },
    "senderAddress": "DoNotReply@29fa5839-e089-4cfb-93b5-dfc003e6df03.azurecomm.net"
}

poller = EmailClient.begin_send(client, message)
result = poller.result()
print(result)