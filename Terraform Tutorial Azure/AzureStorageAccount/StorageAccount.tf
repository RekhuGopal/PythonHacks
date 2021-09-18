resource "azurerm_resource_group" "example" {
  name     = "QuickPOCs-RG"
  location = "West Europe"
}

resource "azurerm_storage_account" "example" {
  name                     = "quickpocstgaccnt0001"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "example" {
  name                  = "secretefiles"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "example" {
  name                   = "StrgAccnttfcode.tf"
  storage_account_name   = azurerm_storage_account.example.name
  storage_container_name = azurerm_storage_container.example.name
  type                   = "Block"
  source                 = "C:/Users/Rekhu.Chinnarathod/Desktop/PersonalDocs/PersonalDocuments/Rekhu/AzurePoC/StorageAccount/StrgAccnttfcode.tf"
}