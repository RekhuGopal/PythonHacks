import boto3


class PetShop:

    def __init__(self):
        client = boto3.resource('dynamodb')
        self.table = client.Table('Pets')

    def  Create_data(self , event):
        response = self.table.put_item(
            Item={
                'id': event['id'],
                'name': event['name'],
                'breed': event['breed'],
                'gender': event['gender'],
                'owner': event['owner'],
                'birthday': event['birthday']
            }
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': 'Record ' + event['id'] + ' added'
        }    

    def  Read_data(self , event):
        response = self.table.get_item(
            Key={
                'id': event['id']
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return {
                'statusCode': '404',
                'body': 'Not found'
            }

    def  Update_data(self , event):
        response = self.table.update_item(
            Key={'id': event['id']},
            ExpressionAttributeNames={
                '#N': 'name',
                '#B': 'breed',
                '#G': 'gender',
                '#O': 'owner',
                '#K': 'birthday'
            },
            ExpressionAttributeValues={
                ':n': event['name'],
                ':b':event['breed'],
                ':g': event['gender'],
                ':o': event['owner'],
                ':k': event['birthday'],
            },
            UpdateExpression='SET #N = :n, #B = :b, #G = :g, #O = :o, #K = :k',
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            'body': 'Record ' + event['id'] + ' updated'
        }

    def  Delete_data(self , event):
        response = self.table.delete_item(
            Key={
                'id': event['id']
            }
        )

        return {
                'statusCode': '200',
                'body': 'Deleted the item with id :' + event['id']
            }

def lambda_handler(event, context):
    if event:
        pet_Object =  PetShop()
        if event['tasktype']  == "create":
            create_result =  pet_Object.Create_data(event['data'])
            return create_result
        elif event['tasktype']  == "read":
            read_result =  pet_Object.Read_data(event['data'])
            return read_result
        elif event['tasktype']  == "update":
            update_result =  pet_Object.Update_data(event['data'])
            return update_result
        elif event['tasktype']  == "delete":
            delete_result =  pet_Object.Delete_data(event['data'])
            return delete_result
        else :
            return {
                'statusCode': '404',
                'body': 'Not found'
            }
