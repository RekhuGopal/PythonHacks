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
