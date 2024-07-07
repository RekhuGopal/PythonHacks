import boto3

client = boto3.client('resource-explorer-2')

#AWS resource explorer view ARN ( Default use when not provided)
view_arn = "arn:aws:resource-explorer-2:us-west-2:357171621133:view/all-resources/2a87ad65-7bf3-4be5-984f-864c935e6a3b"

# Query string to filter resources without a specific tag key
query_string = '-tag.key:Lab'  

# Initialize list to store resource ARNs
list_of_resource_ids = []

# Paginate through results to retrieve all resources
paginator = client.get_paginator('search')
response_iterator = paginator.paginate(
    QueryString=query_string,
    ViewArn=view_arn
)

for page in response_iterator:
    resources = page['Resources']
    list_of_resource_ids.extend([item['Arn'] for item in resources])

# Remove duplicates if needed (though unlikely for ARNs)
unique_list = list(set(list_of_resource_ids))
print(len(unique_list))
Not_Tagged_List =  []

# Function to tag resources
def tag_resources_by_region(resource_groups):
    for region, resource_list in resource_groups.items():
        if region:
            tag_resources_client = boto3.client('resourcegroupstaggingapi', region_name=region)
            batches = [resource_list[i:i + 20] for i in range(0, len(resource_list), 20)]
            
            for batch in batches:
                tag_response = tag_resources_client.untag_resources(
                    ResourceARNList=batch,
                    TagKeys=['Lab']
                )
                if tag_response['FailedResourcesMap']:
                   Not_Tagged_List.extend(list(tag_response['FailedResourcesMap'].keys()))
        else:
            tag_resources_client = boto3.client('resourcegroupstaggingapi', region_name="us-east-1")
            batches = [resource_list[i:i + 20] for i in range(0, len(resource_list), 20)]
            
            for batch in batches:
                tag_response = tag_resources_client.untag_resources(
                    ResourceARNList=batch,
                    TagKeys=['Lab']
                )
                if tag_response['FailedResourcesMap']:
                   Not_Tagged_List.extend(list(tag_response['FailedResourcesMap'].keys()))


# Group resources by region
resource_groups = {}

for arn in unique_list:
    if ':' in arn:
        region = arn.split(':')[3]
        if region not in resource_groups:
            resource_groups[region] = []
        resource_groups[region].append(arn)

# Tag resources in batches by region
tag_resources_by_region(resource_groups)


print(len(Not_Tagged_List))
print(Not_Tagged_List)

