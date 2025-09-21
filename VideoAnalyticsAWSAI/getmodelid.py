import boto3

bedrock = boto3.client("bedrock", region_name="us-west-2")

response = bedrock.list_foundation_models()
for model in response["modelSummaries"]:
    print(model["modelId"], "-", model["modelName"], "-", model["providerName"])
