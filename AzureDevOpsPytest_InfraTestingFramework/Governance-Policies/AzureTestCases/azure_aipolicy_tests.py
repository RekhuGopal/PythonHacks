def azure_check_if_ai_services_can_be_created_in_allowed_rg( DeploymentWhatIf, DeploymentWhatIfProperties, resource_client, resource_group, location, service_name):
    try:
        deployment_name = "whatIfDeployment"

        template = {
            "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
            "contentVersion": "1.0.0.0",
            "resources": [
                {
                    "type": "Microsoft.CognitiveServices/accounts",
                    "apiVersion": "2022-12-01",
                    "name": service_name,
                    "location": location,
                    "sku": {"name": "S0", "tier": "Standard"},
                    "kind": "AIServices",
                    "properties": {
                        "networkAcls": {
                            "defaultAction": "Deny",
                            "virtualNetworks": [],
                            "ipRules": []
                        }
                    }
                }
            ]
        }

        deployment_properties = DeploymentWhatIfProperties(
            mode="Incremental",
            template=template
        )

        what_if_operation = resource_client.deployments.begin_what_if(
            resource_group_name=resource_group,
            deployment_name=deployment_name,
            parameters=DeploymentWhatIf(properties=deployment_properties)
        )

        what_if_result = what_if_operation.result()

        if what_if_result.status == "Failed":
            return False

        if what_if_result.changes:
            for change in what_if_result.changes:
                if change.change_type == "Create":
                    return True 

        return False

    except Exception as e:
        print(f"Exception occurred in test Azure AI service creation: {e}")
        return False