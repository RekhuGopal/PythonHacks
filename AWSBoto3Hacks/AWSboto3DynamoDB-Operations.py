import boto3
from botocore.exceptions import ClientError
from pprint import pprint
from decimal import Decimal


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
                "S": "{}".format(rating),
            }
        }
    )
    return response

##Get a record in from DynamoDB table
def get_movie(title, year):
    table = client.Table('Movies')

    try:
        response = table.get_item(Key={'year': year, 'title': title})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

## Update a record in DynamoDB table
def update_movie(title, year, rating, plot, actors):
    table = client.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a",
        ExpressionAttributeValues={
            ':r': Decimal(rating),
            ':p': plot,
            ':a': actors
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

## Increment an Atomic Counter in DynamoDB table
def increase_rating(title, year, rating_increase):

    table = client.Table('Movies')

    response = table.update_item(
        Key={
            'year': year,
            'title': title
        },
        UpdateExpression="set info.rating = info.rating + :val",
        ExpressionAttributeValues={
            ':val': Decimal(rating_increase)
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

## Update an Item (Conditionally) in DynamoDB table
def remove_actors(title, year, actor_count):
    table = client.Table('Movies')

    try:
        response = table.update_item(
            Key={
                'year': year,
                'title': title
            },
            UpdateExpression="remove info.actors[0]",
            ConditionExpression="size(info.actors) > :num",
            ExpressionAttributeValues={':num': actor_count},
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response

## Delete an Item in DynamoDB table
def delete_underrated_movie(title, year, rating):
    table = client.Table('Movies')

    try:
        response = table.delete_item(
            Key={
                'year': year,
                'title': title
            },
            ConditionExpression="info.rating <= :val",
            ExpressionAttributeValues={
                ":val": Decimal(rating)
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
    #movie_table = create_movie_table()
    #print("Table status:{}".format(movie_table))

    ## Insert in to DynamoDB
    movie_resp = put_movie("The Big New Movie", 2015,"Nothing happens at all.", 0)
    print("Put movie succeeded:")
    pprint(movie_resp, sort_dicts=False)

'''
    ## Get an item from DynamoDB
    movie = get_movie("The Big New Movie", 2015,)
    if movie:
        print("Get movie succeeded:")
        pprint(movie, sort_dicts=False)

    ## Update and item in  DynamoDB
    update_response = update_movie( "The Big New Movie", 2015, 5.5, "Everything happens all at once.",["Larry", "Moe", "Curly"])
    print("Update movie succeeded:")
    pprint(update_response, sort_dicts=False)

    ## Increment an Atomic Counter in DynamoDB
    update_response = increase_rating("The Big New Movie", 2015, 1)
    print("Update movie succeeded:")
    pprint(update_response, sort_dicts=False)

    ## Update an Item (Conditionally) in DynamoDB
    print("Attempting conditional update (expecting failure)...")
    update_response = remove_actors("The Big New Movie", 2015, 3)
    if update_response:
        print("Update movie succeeded:")
        pprint(update_response, sort_dicts=False)

    ## Delete an Item in DynamoDB table
    print("Attempting a conditional delete...")
    delete_response = delete_underrated_movie("The Big New Movie", 2015, 5)
    if delete_response:
        print("Delete movie succeeded:")
        pprint(delete_response, sort_dicts=False)

'''