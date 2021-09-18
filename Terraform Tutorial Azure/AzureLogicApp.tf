## Azure RG
resource "azurerm_resource_group" "myrgcloudquickpocs" {
  name     = "cloudquickpocsrg001"
  location = "East US"
}

## Azure Logic App
resource "azurerm_logic_app_workflow" "cloudquickpocslogicapp" {
  name                = "cloudquickpoclogicapp1"
  location            = azurerm_resource_group.myrgcloudquickpocs.location
  resource_group_name = azurerm_resource_group.myrgcloudquickpocs.name
}

## A custom action in logic app
resource "azurerm_logic_app_action_custom" "cloudquickpocslogicappcustomaction" {
  name         = "cloudquickpoclogicapp1-Custom-action-1"
  logic_app_id = azurerm_logic_app_workflow.cloudquickpocslogicapp.id

  body = <<BODY
{
    "description": "A variable to configure the auto expiration age in days. Configured in negative number. Default is -30 (30 days old).",
    "inputs": {
        "variables": [
            {
                "name": "ExpirationAgeInDays",
                "type": "Integer",
                "value": -30
            }
        ]
    },
    "runAfter": {},
    "type": "InitializeVariable"
}
BODY

}