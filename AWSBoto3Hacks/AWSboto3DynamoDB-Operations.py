import boto3
from botocore.exceptions import ClientError
from pprint import pprint
from decimal import Decimal
import time


client = boto3.client('dynamodb')

#Create DynamoDB table
def create_movie_table():
    table = client.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

##Create record in a DynamoDB table
def put_movie(title, year, plot, rating):
    response = client.put_item(
       TableName='Movies',
       Item={
            'year': {
                'N': "{}".format(year),
            },
            'title': {
                'S': "{}".format(title),
            },
            'plot': {
                "S": "{}".format(plot),
            },
            'rating': {
                "N": "{}".format(rating),
            }
        }
    )
    return response

##Get a record in from DynamoDB table
def get_movie(title, year):
    try:
        response = client.get_item(       
                TableName='Movies',
                Key={
                        'year': {
                                'N': "{}".format(year),
                        },
                        'title': {
                                'S': "{}".format(title),
                        }
                    }
                )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

## Update a record in DynamoDB table
def update_movie(title, year, rating, plot, actors):
    response = client.update_item(
        TableName='Movies',
        Key={
            'year': {
                    'N': "{}".format(year),
            },
            'title': {
                    'S': "{}".format(title),
            }
        },
        ExpressionAttributeNames={
            '#R': 'rating',
            '#P': 'plot',
            '#A': 'actors'
        },
        ExpressionAttributeValues={
            ':r': {
                'N': "{}".format(rating),
            },
            ':p': {
                'S': "{}".format(plot),
            },
            ':a': {
                'SS': actors,
            }
        },
        UpdateExpression='SET #R = :r, #P = :p, #A = :a',
        ReturnValues="UPDATED_NEW"
    )
    return response

## Increment an Atomic Counter in DynamoDB table
def increase_rating(title, year, rating_increase):
    response = client.update_item(
        TableName='Movies',
        Key={
            'year': {
                    'N': "{}".format(year),
            },
            'title': {
                    'S': "{}".format(title),
            }
        },
        ExpressionAttributeNames={
            '#R': 'rating'
        },
        ExpressionAttributeValues={
            ':r': {
                'N': "{}".format(Decimal(rating_increase)),
            }
        },
        UpdateExpression='SET #R = #R + :r',
        ReturnValues="UPDATED_NEW"
    )
    return response

## Delete an Item in DynamoDB table
def delete_underrated_movie(title, year, rating):
    try:
        response = client.delete_item(
            TableName='Movies',
            Key={
                'year': {
                    'N': "{}".format(year),
                },
                'title': {
                    'S': "{}".format(title),
                }
            },
            ConditionExpression="rating <= :a",
            ExpressionAttributeValues={
                ':a': {
                    'N': "{}".format(rating),
                }
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response 

if __name__ == '__main__':

    ## Create DynamoDB
    movie_table = create_movie_table()
    print("Create DynamoDB succeeded............")
    print("Table status:{}".format(movie_table))

    time.sleep(30)
    
    ## Insert in to DynamoDB
    movie_resp = put_movie("The Big New Movie", 2015,"Nothing happens at all.", 0)
    print("Insert in to DynamoDB succeeded............")
    pprint(movie_resp, sort_dicts=False)

    
    ## Get an item from DynamoDB
    movie = get_movie("The Big New Movie", 2015,)
    if movie:
       print("Get an item from DynamoDB succeeded............")
       pprint(movie, sort_dicts=False)

    
    ## Update and item in  DynamoDB
    update_response = update_movie( "The Big New Movie", 2015, 5.5, "Everything happens all at once.",["Larry", "Moe", "Curly"])
    print("Update and item in  DynamoDB succeeded............")
    pprint(update_response, sort_dicts=False)
 
    
    ## Increment an Atomic Counter in DynamoDB
    update_response = increase_rating("The Big New Movie", 2015, 1)
    print("Increment an Atomic Counter in DynamoDB succeeded............")
    pprint(update_response, sort_dicts=False)

    
    ## Delete an Item in DynamoDB table
    delete_response = delete_underrated_movie("The Big New Movie", 2015, 7.5)
    if delete_response:
        print("Delete an Item in DynamoDB table.........................")
        pprint(delete_response, sort_dicts=False)
