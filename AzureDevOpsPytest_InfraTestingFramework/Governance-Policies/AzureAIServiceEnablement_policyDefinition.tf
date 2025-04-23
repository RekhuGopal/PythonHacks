resource "azurerm_policy_definition" "AZ-AS-GPD-00001" {
  name         = "AZ-AS-GPD-${var.General.ENV.ShortName}-00001"
  policy_type  = "Custom"
  mode         = "Indexed"
  description  = "List of allowed resource groups for Azure AI services."
  display_name = "Azure AI Service Allowed RGs"

  metadata    = file("${path.module}/json/GPD00001_AzureAIServiceEnablement/Metadata.json")
  policy_rule = file("${path.module}/json/GPD00001_AzureAIServiceEnablement/PolicyRule.json")
  parameters  = file("${path.module}/json/GPD00001_AzureAIServiceEnablement/Parameters.json")
}
