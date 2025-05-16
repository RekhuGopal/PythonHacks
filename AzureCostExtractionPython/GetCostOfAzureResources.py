from azure.mgmt.costmanagement.models import QueryDefinition
from azure.identity import DefaultAzureCredential
from azure.mgmt.costmanagement import CostManagementClient
from datetime import datetime, timezone
import time
import random

# Replace with the management group ID and other required values

resource_ids = [
    '/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/costoptimizationsas/providers/Microsoft.Storage/storageAccounts/costoptimizationsas',
    '/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/costoptimizationsas/providers/Microsoft.Storage/storageAccounts/test43254ewrtewtw'
] 

# Initialize Azure credentials and cost management client
credential = DefaultAzureCredential()
cost_client = CostManagementClient(credential)

end_date = datetime.now(timezone.utc).date()
start_date = end_date.replace(day=1)
start_date_str = datetime(start_date.year, start_date.month, 1, tzinfo=timezone.utc).isoformat()
print(start_date_str)
end_date_str = datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone.utc).isoformat()
print(end_date_str)

query_scope ='/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff'
day_of_month = 16

def AZ_Per_Day_Cost(QueryDefinition, time, random, cost_client, resource_ids, query_scope, start_date_str, end_date_str, day_of_month):
    retry_delay = 1
    attempt = 0
    max_retries=5
    az_costlist = []
    while attempt < max_retries:
        try:
            query_definition = QueryDefinition(
                type='Usage',
                timeframe='Custom',
                time_period={
                    'from': start_date_str,
                    'to': end_date_str
                },
                dataset={
                    'granularity': 'Monthly',
                    'filter': {
                        'dimensions': {
                            'name': 'resourceId',
                            'operator': 'In',
                            'values': resource_ids
                        }
                    },
                    'grouping': [  # Group by resourceId
                        {
                            'name': 'resourceId',
                            'type': 'Dimension'
                        }
                    ],
                    'aggregation': {
                        'totalCost': {
                            'name': 'Cost',
                            'function': 'Sum'
                        }
                    }
                }
            )
            response = cost_client.query.usage(
                scope=query_scope,
                parameters=query_definition
            )
            dict_result = response.as_dict()
            if 'rows' in dict_result:
                for row in dict_result['rows']:
                    az_costlist.append({'id' : row[2] , 'cost' : row[0]/day_of_month})
                if len(az_costlist) > 0:
                    az_costlist_ids = [ item['id'].lower() for item in az_costlist]
                    for id in resource_ids:
                        if id.lower() not in az_costlist_ids:
                            az_costlist.append({'id' : id.lower() , 'cost' : 0})
                            az_costlist_ids.append(id.lower())
                    return az_costlist
                else:
                    for resource_id in resource_ids:
                        az_costlist.append({'id': resource_id, 'cost': 0})
                    return az_costlist
            else:
                for resource_id in resource_ids:
                    az_costlist.append({'id': resource_id, 'cost': 0})
                return az_costlist
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt < max_retries:
                sleep_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                print("Max retry attempts reached. Aborting.")
                for resource_id in resource_ids:
                    az_costlist.append({'id': resource_id, 'cost': 0})
                return az_costlist

# Example usage
if __name__ == "__main__":
    result = AZ_Per_Day_Cost(QueryDefinition, time, random, cost_client, resource_ids, query_scope, start_date_str, end_date_str, day_of_month)
    print(result)