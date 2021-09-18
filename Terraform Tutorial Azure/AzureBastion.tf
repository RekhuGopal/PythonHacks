# Create Azure RG
resource "azurerm_resource_group" "ABS" {
  name     = "cloudquickpocs-Bastion-resources"
  location = "West Europe"
}

# Create Azure Vnet
resource "azurerm_virtual_network" "ABS" {
  name                = "bastiondemovnet"
  address_space       = ["192.168.1.0/24"]
  location            = azurerm_resource_group.ABS.location
  resource_group_name = azurerm_resource_group.ABS.name
}

# Create Azure subnet
resource "azurerm_subnet" "ABS" {
  name                 = "AzureBastionSubnet"
  resource_group_name  = azurerm_resource_group.ABS.name
  virtual_network_name = azurerm_virtual_network.ABS.name
  address_prefixes     = ["192.168.1.224/27"]
}

# Create Azure public IP
resource "azurerm_public_ip" "ABS" {
  name                = "bastiondemovnetpip"
  location            = azurerm_resource_group.ABS.location
  resource_group_name = azurerm_resource_group.ABS.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Create Azure bastion
resource "azurerm_bastion_host" "ABS" {
  name                = "cqpocsbastionfordemo"
  location            = azurerm_resource_group.ABS.location
  resource_group_name = azurerm_resource_group.ABS.name

  ip_configuration {
    name                 = "configuration"
    subnet_id            = azurerm_subnet.ABS.id
    public_ip_address_id = azurerm_public_ip.ABS.id
  }
}