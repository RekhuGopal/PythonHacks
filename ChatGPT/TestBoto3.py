resource "azurerm_storage_account" "my_storage_account" {
  name                     = "mystorageaccount"
  resource_group_name      = azurerm_resource_group.my_resource_group.name
  location                 = azurerm_resource_group.my_resource_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_virtual_network_peering" "my_vnet_peering" {
  name                = "my-vnet-peering"
  resource_group_name = azurerm_resource_group.my_resource_group.name
  virtual_network_name = azurerm_virtual_network.my_virtual_network.name
  peer_virtual_network_id = azurerm_virtual_network.peer_virtual_network.id
  allow_forwarded_traffic = true
  allow_virtual_network_access = true
  allow_gateway_transit = true
}
