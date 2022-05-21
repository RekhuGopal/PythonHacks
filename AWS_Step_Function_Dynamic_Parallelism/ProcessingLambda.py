import json

def lambda_handler(event, context):
    # TODO implement
    print(event)
    if 'payment' in event :
        if event['payment'] == 'check':
            ## Add you validation logic
            event.update({'payment': "Ok"})
            print(event)
            return event
    else:
        print("order processing complete ")
        return event
