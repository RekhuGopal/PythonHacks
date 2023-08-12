import json
import base64
import os

def lambda_handler(event, context):
    print("event collected is {}".format(event))
    for record in event['Records'] :
        sample_string_bytes = base64.b64decode(record['kinesis']['data'])
        sample_string = sample_string_bytes.decode("ascii")
        print(f"Decoded string: {sample_string}")
        with open("sample.json", "w") as outfile:
            json.dump(sample_string, outfile)
        print("Inside function to create the dynamic .json file...")
        s3_file_name =  event['ProvisionedProduct']['AccountNumber'] + "/parameters.json"
        print("s3 bucket path to store account parameter.json file would be  {}".format(s3_file_name))
        local_file_path = "/tmp/payload.json"
        print("file path:{}".format(local_file_path))
        with open(local_file_path, 'w') as fp:
            json.dump(event, fp)
        print("event is stored in local json file")
        self.s3_client.meta.client.upload_file(local_file_path,self.githubaction_parameter_bucket, s3_file_name)
        print("file uploaded successfully..")
        os.remove(local_file_path)
        print("File deleted after upload to s3 bucket")
