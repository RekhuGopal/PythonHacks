import json
import boto3
import string
import random

def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=2))

    try:
        # Extract key fields
        agent = event.get('agent')
        action_group = event.get('actionGroup')
        function = event.get('function')
        parameters = event.get('parameters', [])
        session_attributes = event.get('sessionAttributes', {})
        prompt_session_attributes = event.get('promptSessionAttributes', {})

        print(f"Action group: {action_group}")
        print(f"Function: {function}")
        print(f"Parameters: {parameters}")

        # Extract parameter value
        if not parameters:
            raise Exception("No parameters provided in the request.")
        
        param_value = parameters[0].get('value')
        print(f"Raw parameter value: {param_value}")

        # Parse JSON parameter
        if isinstance(param_value, str):
            payload = json.loads(param_value)
            print(f"Parsed JSON payload: {payload}")
        else:
            payload = param_value
            print(f"Parameter already a dictionary: {payload}")

        # Generate random filename
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".json"
        print(f"Generated filename: {filename}")

        # Upload to S3
        print("Uploading to S3...")
        boto3.client("s3").put_object(
            Bucket="databucketsourceside",
            Key=filename,
            Body=json.dumps(payload)
        )
        print("Upload successful.")

        # Prepare response body
        response_body = {
            'TEXT': {
                'body': f"Upload successful. File name: {filename}"
            }
        }

        function_response = {
            'actionGroup': action_group,
            'function': function,
            'functionResponse': {
                'responseBody': response_body
            }
        }

        final_response = {
            'messageVersion': '1.0',
            'response': function_response,
            'sessionAttributes': session_attributes,
            'promptSessionAttributes': prompt_session_attributes
        }

        print("Returning success response:")
        print(json.dumps(final_response, indent=2))
        return final_response

    except Exception as e:
        print(f"Exception: {str(e)}")
        response_body = {
            'TEXT': {
                'body': f"Upload failed: {str(e)}"
            }
        }

        function_response = {
            'actionGroup': event.get('actionGroup'),
            'function': event.get('function'),
            'functionResponse': {
                'responseBody': response_body
            }
        }

        error_response = {
            'messageVersion': '1.0',
            'response': function_response,
            'sessionAttributes': event.get('sessionAttributes', {}),
            'promptSessionAttributes': event.get('promptSessionAttributes', {})
        }

        print("Returning error response:")
        print(json.dumps(error_response, indent=2))
        return error_response