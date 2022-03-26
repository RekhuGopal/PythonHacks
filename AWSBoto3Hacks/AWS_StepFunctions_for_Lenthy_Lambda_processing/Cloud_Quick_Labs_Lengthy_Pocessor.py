# Set up logging
from datetime import date
import calendar

maxiterationcount = 3
def processing(event):
    my_date = date.today()
    dayname = calendar.day_name[my_date.weekday()]
    if event['iterationcount'] <= maxiterationcount:
        print("Iterations not completed yet... and count is : ", event['iterationcount'])
        if dayname == 'Saturday':
            print("It is saturday today...")
            event['IsComplete'] = False
        else:
            print("It not saturday today...")
            event['IsComplete'] = True
        return event
    else :
        print("Iterations completed now... and count is : ", event['iterationcount'])
        print("In else it is saturday today...")
        event['IsComplete'] = True
        return event
# Define Lambda function
def lambda_handler(event, context):
    if 'iterationcount' in event.keys():
        print("In if lambda handler now..")
        event['iterationcount'] += 1
        return processing(event)
    else :
        print("In else lambda handler now..")
        event['iterationcount'] = 1
        return processing(event)
