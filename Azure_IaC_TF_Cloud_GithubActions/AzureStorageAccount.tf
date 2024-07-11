resource "azurerm_resource_group" "demo" {
  name     = "example-resources"
  location = "southcentralus"
}

## Demo now1
resource "azurerm_storage_account" "StorageAccountDemo" {
  name                     = "satestant200012"
  resource_group_name      = azurerm_resource_group.demo.name
  location                 = azurerm_resource_group.demo.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    video = "azure"
    channel = "CloudQuickLabs"
  }
}