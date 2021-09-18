## Retrive the Buitl Policy ID for assignment
data "azurerm_policy_definition" "builtinsubscriptiontagpolicy" {
  display_name = "Add or replace a tag on subscriptions"
}

output "id" {
  value = data.azurerm_policy_definition.builtinsubscriptiontagpolicy.id
}

### Policy Assignment
resource "azurerm_policy_assignment" "assigntagonsubscription" {
  name                 = "Assign-BusinessTag-00001"
  scope                = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  policy_definition_id = data.azurerm_policy_definition.builtinsubscriptiontagpolicy.id
  display_name         = "Assign Business Tag On Azure Subscription"
  description          = "This policy ensures that businesstag is always present in the subscriptions"
  location             = "centralus"
  identity {
    type               = "SystemAssigned"
  }
  parameters = <<PARAMETERS
  {
    "tagName": {
      "value": "BusinessName"
    },
	"tagValue": {
      "value": "AgroTech"
    }
  }
  PARAMETERS
}

## "Tag Contributor" role assignment to policy managed identity
resource "azurerm_role_assignment" "roleManagedidentitytagassignment" {
  scope                = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  role_definition_name = "Tag Contributor"
  principal_id         = azurerm_policy_assignment.assigntagonsubscription.identity[0].principal_id
  
  provisioner "local-exec" {
    command = "Start-Sleep -s 120"
    interpreter = ["PowerShell", "-Command"]
  }
}

## Policy remediate.
resource "azurerm_policy_remediation" "remediatetagassignmentpolicy" {
  name                 = "addtagsviapolicyremediation"
  scope                = "/subscriptions/49d3ec60-54b5-41c0-b240-c0cc7980a4f4"
  policy_assignment_id = azurerm_policy_assignment.assigntagonsubscription.id
  resource_discovery_mode = "ReEvaluateCompliance"
  depends_on          = [azurerm_role_assignment.roleManagedidentitytagassignment]
}