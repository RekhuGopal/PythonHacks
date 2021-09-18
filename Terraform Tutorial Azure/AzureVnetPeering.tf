# variable location - array
variable "location" {
  default = [
    "uksouth",
    "southeastasia",
  ]
}

# variable vnet address space - array
variable "vnet_address_space" {
  default = [
    "10.0.0.0/16",
    "10.1.0.0/16",
  ]
}

# create Azure Resource group
resource "azurerm_resource_group" "vnet" {
  count    = length(var.location)
  name     = "rg-global-vnet-peering-${count.index}"
  location = element(var.location, count.index)
}

# create Azure vnet per location
resource "azurerm_virtual_network" "vnet" {
  count               = length(var.location)
  name                = "vnet-${count.index}"
  resource_group_name = element(azurerm_resource_group.vnet.*.name, count.index)
  address_space       = [element(var.vnet_address_space, count.index)]
  location            = element(azurerm_resource_group.vnet.*.location, count.index)
}

# Cretae Azure vnet subnet per vnet
resource "azurerm_subnet" "nva" {
  count                = length(var.location)
  name                 = "nva"
  resource_group_name  = element(azurerm_resource_group.vnet.*.name, count.index)
  virtual_network_name = element(azurerm_virtual_network.vnet.*.name, count.index)
  address_prefix = cidrsubnet(
    element(
      azurerm_virtual_network.vnet[count.index].address_space,
      count.index,
    ),
    13,
    0,
  ) # /29
}

# enable global peering between the two virtual network
resource "azurerm_virtual_network_peering" "peering" {
  count                        = length(var.location)
  name                         = "peering-to-${element(azurerm_virtual_network.vnet.*.name, 1 - count.index)}"
  resource_group_name          = element(azurerm_resource_group.vnet.*.name, count.index)
  virtual_network_name         = element(azurerm_virtual_network.vnet.*.name, count.index)
  remote_virtual_network_id    = element(azurerm_virtual_network.vnet.*.id, 1 - count.index)
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true

  # `allow_gateway_transit` must be set to false for vnet Global Peering
  allow_gateway_transit = false
}