resource "azurerm_subscription_policy_assignment" "AZ-AS-GPA-00001" {
  name                 = "AZ-AS-PLA-${var.General.ENV.ShortName}-N-CR-00001"
  subscription_id      = "/subscriptions/${var.General.ENV.Id}"
  policy_definition_id = azurerm_policy_definition.AZ-AS-GPD-00001.id
  description          = "List of allowed resource groups for Azure AI services."
  display_name         = "Azure AI Service Allowed RGs"

  parameters           = jsonencode(var.Policies.AZ-AS-GPD-00001)

}