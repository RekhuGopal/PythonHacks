# ARM provider block
provider "azurerm" {
  version = "=2.0.0"
  features {}
}
# Terraform backend configuration block -precreated
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-cloudquickpocs"
    storage_account_name = "ccpsazuretf0001"
    container_name       = "ccpterraformstatefile"
    key                  = "ccpsterraform.tfstate"
  }
}
# RG creation 
resource "azurerm_resource_group" "RG-githubaction-azure" {
  name     = "rg-githubaction-cloudquickpocs"
  location = "northeurope"
}

# Create storage account-1.
resource "azurerm_storage_account" "example" {
  name                     = "quickpocstgaccnt0002"
  resource_group_name      = azurerm_resource_group.RG-githubaction-azure.name
  location                 = azurerm_resource_group.RG-githubaction-azure.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Create Azure storage account-2.
resource "azurerm_storage_account" "example2" {
  name                     = "quickpocstgaccnt0003"
  resource_group_name      = azurerm_resource_group.RG-githubaction-azure.name
  location                 = azurerm_resource_group.RG-githubaction-azure.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}