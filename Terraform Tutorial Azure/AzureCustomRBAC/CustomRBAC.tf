
#Create Custom RBAC using Terrafrom - CloudQuickPOCS
resource "azurerm_role_definition" "CloudQuickPOCCustomRBAC" {
  name        = "POC-Custom-RBAC"
  scope       = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  description = "Created for demo at CLoudQuickPOCs"

  permissions {
    actions = [
		"Microsoft.Support/*"
    ]
    not_actions = [

		]
  }

  assignable_scopes = [
	"/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  ]
}


#Assign Custom RBAC using Terrafrom - CloudQuickPOCS
resource "azurerm_role_assignment" "CloudQuickPOCCustomRBACAssignment" {
  scope              = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  role_definition_id = azurerm_role_definition.CloudQuickPOCCustomRBAC.role_definition_resource_id
  principal_id       = "ce85eae4-0769-4f77-b1b8-a253f34a6160"
}