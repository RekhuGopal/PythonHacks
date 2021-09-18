### Policy Definition
resource "azurerm_policy_definition" "AZPLCYD00001" {
  name                  = "Base-AllowedRegions-00001"
  policy_type           = "Custom"
  mode                  = "Indexed"
  display_name          = "Validate the allowed regions for Azure resources"
  
  lifecycle {
	ignore_changes = [metadata]
  }
  
  metadata = file("C:/Users/Rekhu.Chinnarathod/Desktop/PersonalDocs/PersonalDocuments/Rekhu/AzurePoC/Policy/Metadata.json")
  
  policy_rule = file("C:/Users/Rekhu.Chinnarathod/Desktop/PersonalDocs/PersonalDocuments/Rekhu/AzurePoC/Policy/PolicyRule.json")

  parameters = file("C:/Users/Rekhu.Chinnarathod/Desktop/PersonalDocs/PersonalDocuments/Rekhu/AzurePoC/Policy/Parameters.json")
}

### Policy Assignment
resource "azurerm_policy_assignment" "AZPLCYA00001" {
  name                 = "Base-AllowedRegionPolicyAssignment-00001"
  scope                = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  policy_definition_id =  azurerm_policy_definition.AZPLCYD00001.id
  display_name         = "Validate the allowed regions for Azure resource creation"
  description          = "This policy ensures that only allowed locations are used to create the resource in azure platform"

  parameters = <<PARAMETERS
  {
    "allowedLocations": {
      "value": [
            "South India",
            "West India",
            "East US",
            "West US",
			"SouthEast Asia",
			"East Asia"
          ]
    }
  }
  PARAMETERS
}